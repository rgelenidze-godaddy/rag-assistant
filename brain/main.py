from fastapi import FastAPI
from contextlib import asynccontextmanager

from brain.chat.vendor.telegram import TelegramBot
from brain.core.callback import brain_callback_sync

from brain.embedding import instance as embedding_instance
from brain.vectorstore import connection as vectorstore_connection


@asynccontextmanager
async def lifespan(_: FastAPI):
    # --- Startup calls ---
    print("Initializing components...")

    # Initialize embedding and Vector Database Connections
    embedding_instance.initialize()

    vectorstore_connection.initialize()
    vectorstore_connection.declare_collections()

    # All setup, now start the bot
    telegram_bot_instance = TelegramBot(brain_callback_sync)
    await telegram_bot_instance.start()

    print("Components initialized!")

    yield  # Let FastAPI loop run

    # --- Shutdown calls ---
    await telegram_bot_instance.stop()


app = FastAPI(lifespan=lifespan)
