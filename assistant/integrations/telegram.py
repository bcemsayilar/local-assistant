"""Telegram bot integration for the local assistant."""

import logging
from pathlib import Path
from typing import Set

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from assistant.config import TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS, MEDIA_CACHE_DIR
from assistant.agent.loop import agent_loop
from assistant.memory.conversation import ConversationMemory
from assistant.memory.facts import FactMemory
from assistant.integrations import claude_bridge as cb

logger = logging.getLogger(__name__)

# Shared instances (set during setup)
memory: ConversationMemory = None
fact_memory: FactMemory = None
rag_retriever = None
web_searcher = None


def is_allowed(user_id: int) -> bool:
    """Check if user is in the allowed list (empty = allow all)."""
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    await update.message.reply_text(
        "Merhaba! Ben lokal asistaninim. Tum veriler cihazda kalir.\n"
        "Bana bir seyler sor veya /help yaz."
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    await update.message.reply_text(
        "Komutlar:\n"
        "/start - Baslat\n"
        "/clear - Konusma gecmisini temizle\n"
        "/facts - Hakkinda bildiklerimi goster\n"
        "/index - Belgeleri yeniden indexle\n"
        "/yeni - Claude ile yeni oturum ac\n"
        "/help - Bu mesaj\n\n"
        "Duz mesaj lokal modele gider, cihazda kalir.\n"
        "'claude' ile baslayan mesaj, gorsel, video, dosya ve sesli not Claude'a gider (buluta cikar)."
    )


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    user_id = update.effective_user.id
    memory.clear_history(user_id)
    await update.message.reply_text("Konusma gecmisi temizlendi.")


async def cmd_facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    user_id = update.effective_user.id
    facts = fact_memory.get_facts(user_id)
    if facts:
        text = "Senin hakkinda bildiklerim:\n" + "\n".join(f"- {f}" for f in facts)
    else:
        text = "Henuz hakkinda bir bilgim yok."
    await update.message.reply_text(text)


async def cmd_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        return
    await update.message.reply_text("Belgeler yeniden indexleniyor...")
    try:
        from assistant.rag.indexer import DocumentIndexer
        from assistant.rag.watcher import initial_index

        indexer = DocumentIndexer()
        await initial_index(indexer)
        await update.message.reply_text("Indexleme tamamlandi.")
    except Exception as e:
        await update.message.reply_text(f"Indexleme hatasi: {e}")


async def send_long(update: Update, text: str):
    """Reply, splitting at Telegram's 4096 char limit."""
    sent = []
    for i in range(0, max(len(text), 1), 4096):
        sent.append(await update.message.reply_text(text[i:i + 4096]))
    return sent


async def run_claude(update: Update, prompt: str):
    """Send one turn to Claude Code, keep the typing indicator alive while it works."""
    import asyncio
    user_id = update.effective_user.id
    task = asyncio.create_task(cb.ask_claude(user_id, prompt))
    while not task.done():
        try:
            await update.message.chat.send_action("typing")
        except Exception:
            pass
        await asyncio.wait({task}, timeout=4.5)
    await send_long(update, task.result())


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


# Messages containing dream-related content will be auto-deleted after sending
AUTO_DELETE_KEYWORDS = ["rüya", "ruya"]
AUTO_DELETE_DELAY = 300  # 5 minutes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    if not is_allowed(update.effective_user.id):
        return

    user_id = update.effective_user.id
    user_text = update.message.text

    if not user_text:
        return

    # "claude ..." -> Claude Code, everything else stays local
    claude_prompt = cb.strip_prefix(user_text)
    if claude_prompt is not None:
        await run_claude(update, claude_prompt)
        return

    # Save user message
    memory.add_message(user_id, "user", user_text)

    # Get conversation history
    history = memory.get_history(user_id)

    # Add facts context if available
    facts_context = fact_memory.get_facts_prompt(user_id)

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        response = await agent_loop(
            user_message=user_text,
            history=history[:-1],  # Exclude the message we just added
            rag_retriever=rag_retriever,
            web_searcher=web_searcher,
        )
    except Exception as e:
        logger.error(f"Agent error: {e}")
        response = f"Bir hata olustu: {e}"

    # Save assistant response
    memory.add_message(user_id, "assistant", response)

    # Send response (split if too long)
    bot_messages = []
    if len(response) > 4096:
        for i in range(0, len(response), 4096):
            bot_msg = await update.message.reply_text(response[i:i + 4096])
            bot_messages.append(bot_msg)
    else:
        bot_msg = await update.message.reply_text(response)
        bot_messages.append(bot_msg)

    # Schedule auto-deletion for sensitive messages (dream notes etc.)
    msg_lower = user_text.lower().strip()
    if any(kw in msg_lower for kw in AUTO_DELETE_KEYWORDS):
        chat_id = update.message.chat_id
        # Delete user's original message
        context.job_queue.run_once(
            _delete_message, AUTO_DELETE_DELAY,
            data={"chat_id": chat_id, "message_id": update.message.message_id},
            job_kwargs={"misfire_grace_time": 86400},
        )
        # Delete bot's reply message(s)
        for bm in bot_messages:
            context.job_queue.run_once(
                _delete_message, AUTO_DELETE_DELAY,
                data={"chat_id": chat_id, "message_id": bm.message_id},
                job_kwargs={"misfire_grace_time": 86400},
            )

    # Periodically extract facts (every 10 messages) - run in background
    msg_count = len(memory.get_history(user_id))
    if msg_count > 0 and msg_count % 10 == 0:
        import asyncio
        async def _extract_facts_bg(uid, fm):
            try:
                conv_text = memory.get_recent_text(uid, limit=10)
                facts = await asyncio.to_thread(fm.extract_facts, conv_text)
                fm.save_facts(uid, facts)
            except Exception as e:
                logger.error(f"Fact extraction error: {e}")
        asyncio.create_task(_extract_facts_bg(user_id, fact_memory))


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
    await run_claude(update, prompt)


def create_bot(
    conv_memory: ConversationMemory,
    fact_mem: FactMemory,
    retriever=None,
    searcher=None,
) -> Application:
    """Create and configure the Telegram bot."""
    global memory, fact_memory, rag_retriever, web_searcher
    memory = conv_memory
    fact_memory = fact_mem
    rag_retriever = retriever
    web_searcher = searcher

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(CommandHandler("facts", cmd_facts))
    app.add_handler(CommandHandler("index", cmd_index))
    app.add_handler(CommandHandler("yeni", cmd_yeni))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, handle_media))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))

    return app
