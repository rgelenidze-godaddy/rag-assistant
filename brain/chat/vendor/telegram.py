import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)

from brain.chat.vendor.base import ChatVendor

TEACHING = 1  # State identifier


class TelegramBot(ChatVendor):
    """
    Generic ChatVendor implementation for Telegram.

    This class acts as a bridge between the Telegram API and the
    core application logic. Passing messages to the core and back.
    """

    def __init__(self, brain_callback):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.app = ApplicationBuilder().token(self.token).build()
        self.brain_callback = brain_callback
        self._polling_task = None

    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_cmd))
        self.app.add_handler(CommandHandler("update_rag", self.update_rag_cmd))

        teach_handler = ConversationHandler(
            entry_points=[CommandHandler("teach", self.teach_cmd)],
            states={TEACHING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_teach_fact)]},
            fallbacks=[],
        )
        self.app.add_handler(teach_handler)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))

    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hi, I’m ASKIU — your university assistant. Ask me anything!")

    async def update_rag_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Updating RAG...")

        update_notification = self.brain_callback(None, action="UPDATE_RAG")

        await update.message.reply_text(update_notification)

    async def teach_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Please send me the fact you'd like me to learn.")
        return TEACHING


    async def process_teach_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text

        facts_notification = self.brain_callback(user_text, action="TEACH")

        await update.message.reply_text(facts_notification)

        return ConversationHandler.END

    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        message_ref = await update.message.reply_text("...")

        try:
            response = self.brain_callback(user_input)
            await message_ref.edit_text(response)
        except Exception as e:
            await message_ref.edit_text("Sorry, something went wrong. Please try again later.")
            print(f"Failed to edit message: {e}")

    async def start(self):
        self.register_handlers()
        await self.app.initialize()
        await self.app.start()
        self._polling_task = asyncio.create_task(self.app.updater.start_polling())

    async def stop(self):
        if self._polling_task:
            await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
