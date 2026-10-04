"""Local Assistant - Main entry point."""

import asyncio
import logging
import signal
import sys

from assistant.config import TELEGRAM_BOT_TOKEN, WATCHED_DIRS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
# httpx logs every Telegram poll URL at INFO, which contains the bot token
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("assistant")


async def main():
    logger.info("Local Assistant baslatiliyor...")

    # Initialize memory
    from assistant.memory.conversation import ConversationMemory
    from assistant.memory.facts import FactMemory

    conv_memory = ConversationMemory()
    fact_memory = FactMemory()
    logger.info("Bellek sistemi hazir")

    # Initialize RAG
    retriever = None
    observer = None
    try:
        from assistant.rag.indexer import DocumentIndexer
        from assistant.rag.retriever import RAGRetriever
        from assistant.rag.watcher import start_watcher, initial_index

        indexer = DocumentIndexer()
        retriever = RAGRetriever()

        if WATCHED_DIRS:
            await initial_index(indexer)
            observer = start_watcher(indexer)
            logger.info("RAG ve dosya izleme aktif")
        else:
            logger.info("RAG hazir (izlenecek dizin tanimlanmamis)")
    except Exception as e:
        logger.warning(f"RAG baslatilamadi (devam ediliyor): {e}")

    # Initialize web search
    searcher = None
    try:
        from assistant.integrations.searxng import WebSearcher

        searcher = WebSearcher()
        logger.info("Web arama (SearxNG) hazir")
    except Exception as e:
        logger.warning(f"Web arama baslatilamadi: {e}")

    # Start Telegram bot
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN ayarlanmamis! .env dosyasini kontrol edin.")
        sys.exit(1)

    from assistant.integrations.telegram import create_bot

    app = create_bot(
        conv_memory=conv_memory,
        fact_mem=fact_memory,
        retriever=retriever,
        searcher=searcher,
    )

    logger.info("Telegram bot baslatiliyor...")

    # Graceful shutdown
    def shutdown(signum, frame):
        logger.info("Kapatiliyor...")
        if observer:
            observer.stop()
            observer.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Run bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    logger.info("Asistan hazir! Telegram'dan mesaj gonderin.")

    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Kapatiliyor...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        if observer:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    asyncio.run(main())
