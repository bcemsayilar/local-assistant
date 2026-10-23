"""Local Assistant - Telegram botu. Notlar kodla vault'a, gerisi Air'deki Claude oturumuna (2026-10-23 sadelestirme)."""

import asyncio
import logging

from assistant.config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
# httpx logs every Telegram poll URL at INFO, which contains the bot token
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("assistant")


async def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN ayarlanmamis, .env dosyasina bak.")

    from assistant.integrations.telegram import create_bot

    app = create_bot()
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("Bot hazir.")
    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        if isinstance(e, SystemExit) and e.code:
            raise
