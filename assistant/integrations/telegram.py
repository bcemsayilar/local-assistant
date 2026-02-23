"""Telegram bot integration for the local assistant."""

import logging
from typing import Set

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from assistant.config import TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS
from assistant.agent.loop import agent_loop
from assistant.memory.conversation import ConversationMemory
from assistant.memory.facts import FactMemory

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
        "/help - Bu mesaj\n\n"
        "Mesaj gonder, ben de yanitlayayim."
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


async def _delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Scheduled callback to delete a message."""
    data = context.job.data
    try:
        await context.bot.delete_message(chat_id=data["chat_id"], message_id=data["message_id"])
    except Exception as e:
        logger.warning(f"Mesaj silinemedi: {e}")


# Messages starting with these prefixes will be auto-deleted after sending
AUTO_DELETE_PREFIXES = ["rüya notu", "ruya notu"]
AUTO_DELETE_DELAY = 300  # 5 minutes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    if not is_allowed(update.effective_user.id):
        return

    user_id = update.effective_user.id
    user_text = update.message.text

    if not user_text:
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
    if any(msg_lower.startswith(p) for p in AUTO_DELETE_PREFIXES):
        chat_id = update.message.chat_id
        # Delete user's original message
        context.job_queue.run_once(
            _delete_message, AUTO_DELETE_DELAY,
            data={"chat_id": chat_id, "message_id": update.message.message_id},
        )
        # Delete bot's reply message(s)
        for bm in bot_messages:
            context.job_queue.run_once(
                _delete_message, AUTO_DELETE_DELAY,
                data={"chat_id": chat_id, "message_id": bm.message_id},
            )

    # Periodically extract facts (every 10 messages)
    msg_count = len(memory.get_history(user_id))
    if msg_count > 0 and msg_count % 10 == 0:
        try:
            conv_text = memory.get_recent_text(user_id, limit=10)
            facts = fact_memory.extract_facts(conv_text)
            fact_memory.save_facts(user_id, facts)
        except Exception as e:
            logger.error(f"Fact extraction error: {e}")


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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app
