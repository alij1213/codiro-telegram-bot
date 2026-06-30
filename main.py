import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application
from handlers import (
    setup_command_handlers,
    setup_conversation_handlers,
    setup_chat_handlers,
)
from database import init_database

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "0"))


async def post_init(application: Application) -> None:
    init_database()
    logger.info("Database initialized")


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN not found in environment variables")
    
    if ADMIN_ID == 0:
        raise ValueError("ADMIN_ID not found in environment variables")
    
    if GROUP_CHAT_ID == 0:
        raise ValueError("GROUP_CHAT_ID not found in environment variables")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.post_init = post_init

    setup_command_handlers(application)
    setup_conversation_handlers(application)
    setup_chat_handlers(application)

    logger.info("Bot started")
    application.run_polling(allowed_updates=["message", "callback_query", "chat_join_request"])


if __name__ == "__main__":
    main()
