"""Telegram bot integration for the local assistant."""

import logging
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from assistant.config import TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS
from assistant.integrations import claude_bridge as cb
from assistant import notes

logger = logging.getLogger(__name__)


def is_allowed(user_id: int) -> bool:
    """Check if user is in the allowed list (empty = allow all)."""
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    await update.message.reply_text("Merhaba. Yazdigin her sey Claude'a gider; ruya, gunluk ve spor ile baslayan mesajlar dogrudan nota yazilir. /help")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    await update.message.reply_text(
        "Notlar (model yok, kod yazar):\n"
        "ruya ... -> ruya notu (mesajlar 5 dk sonra silinir)\n"
        "gunluk ... -> bugunun gunluk notu\n"
        "spor 1 + satir satir 'hareket: setler' -> Program 1 tablosu, kalan metin not\n\n"
        "Gerisi (metin, gorsel, video, dosya, sesli not) Air'deki Claude oturumuna gider, buluta cikar.\n"
        "/yeni - Claude ile yeni oturum\n/help - Bu mesaj"
    )


async def send_long(update: Update, text: str):
    """Reply, splitting at Telegram's 4096 char limit."""
    sent = []
    for i in range(0, max(len(text), 1), 4096):
        sent.append(await update.message.reply_text(text[i:i + 4096]))
    return sent


async def run_claude(update: Update, prompt: str, voice: bool = False, fresh: bool = False):
    """Send one turn to Claude Code, keep the typing indicator alive while it works.

    voice=True also sends the answer as a voice note (the text still follows, for links and paths).
    """
    import asyncio
    user_id = update.effective_user.id
    task = asyncio.create_task(cb.ask_claude(user_id, prompt, fresh=fresh))
    while not task.done():
        try:
            await update.message.chat.send_action("typing")
        except Exception:
            pass
        await asyncio.wait({task}, timeout=4.5)
    answer = task.result()
    if voice:
        ogg = await cb.speak(answer)
        if ogg:
            try:
                with open(ogg, "rb") as f:
                    await update.message.reply_voice(f)
            except Exception as e:
                logger.error(f"voice reply failed: {e}")
    await send_long(update, answer)


async def cmd_yeni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    cb.reset_session(update.effective_user.id)
    await update.message.reply_text("Claude icin yeni oturum acildi.")


async def _delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Scheduled callback to delete a message."""
    data = context.job.data
    try:
        await context.bot.delete_message(chat_id=data["chat_id"], message_id=data["message_id"])
    except Exception as e:
        logger.warning(f"Mesaj silinemedi: {e}")


AUTO_DELETE_DELAY = 300  # 5 minutes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ruya / gunluk / spor ile baslayan mesaj nota yazilir, gerisi Claude'a gider."""
    if not is_allowed(update.effective_user.id):
        return
    text = update.message.text
    if not text:
        return

    saved = notes.route(text)
    if saved is not None:
        reply = await update.message.reply_text(saved["reply"])
        if saved["kind"] == "ruya":
            # ruya mesaji ve cevabi sohbette kalmasin
            for mid in (update.message.message_id, reply.message_id):
                context.job_queue.run_once(
                    _delete_message, AUTO_DELETE_DELAY,
                    data={"chat_id": update.message.chat_id, "message_id": mid},
                    job_kwargs={"misfire_grace_time": 86400},
                )
        return

    # Instagram post ya da reel linki -> tek seferlik hasat turu (konusma oturumuna yazilmaz)
    harvest = cb.harvest_prompt(text)
    if harvest is not None:
        await run_claude(update, harvest, fresh=True)
        return

    # "claude" oneki artik gerekmiyor ama yazilirsa atilir
    prompt = cb.strip_prefix(text)
    await run_claude(update, prompt if prompt is not None else text)


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photos, videos and documents go to Claude with their local file path."""
    if not is_allowed(update.effective_user.id):
        return
    msg = update.message
    caption = (msg.caption or "").strip()
    caption = cb.strip_prefix(caption) if cb.strip_prefix(caption) is not None else caption
    try:
        if msg.photo:
            obj, suffix, kind = msg.photo[-1], ".jpg", "gorsel"
        elif msg.video:
            obj, suffix, kind = msg.video, ".mp4", "video"
        elif msg.document:
            obj, kind = msg.document, "dosya"
            suffix = Path(msg.document.file_name or "file.bin").suffix or ".bin"
        else:
            return
        file = await context.bot.get_file(obj.file_id)
        local_path = cb.inbox_path(suffix)
        await file.download_to_drive(str(local_path))
    except Exception as e:
        logger.error(f"Media download error: {e}", exc_info=True)
        await msg.reply_text(f"Dosya indirilemedi: {e}")
        return
    prompt = f"Telegram'dan {kind} geldi, dosya: {local_path}\n"
    prompt += f"Mesaj: {caption}" if caption else "Mesaj yok; ne oldugunu incele, onemliyse uygun yere kaydet ve kisaca soyle."
    await run_claude(update, prompt)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Voice notes and audio: transcribe locally with whisper, then send to Claude."""
    if not is_allowed(update.effective_user.id):
        return
    msg = update.message
    obj = msg.voice or msg.audio
    try:
        file = await context.bot.get_file(obj.file_id)
        local_path = cb.inbox_path(".ogg" if msg.voice else (Path(getattr(obj, "file_name", "") or "a.m4a").suffix or ".m4a"))
        await file.download_to_drive(str(local_path))
    except Exception as e:
        await msg.reply_text(f"Ses indirilemedi: {e}")
        return
    await msg.chat.send_action("typing")
    text = await cb.transcribe(local_path)
    if text:
        prompt = f"Sesli not (whisper dokumu, hatali kelime olabilir):\n{text}\n\nSes dosyasi: {local_path}"
    else:
        prompt = f"Sesli not geldi ama yaziya dokulemedi (whisper yok). Dosya: {local_path}"
    # Voice in, voice out: only for voice notes, not for audio files sent for analysis
    if msg.voice:
        prompt += "\n\nCevabin sesli okunacak: kisa, konusma diliyle, liste ve kod yok."
    await run_claude(update, prompt, voice=bool(msg.voice))


def create_bot() -> Application:
    """Create and configure the Telegram bot."""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("yeni", cmd_yeni))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, handle_media))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))

    return app
