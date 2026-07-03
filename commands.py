from telegram import Update
from telegram.ext import ContextTypes


# ========= КОМАНДА /about =========

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Это мой первый backend-проект.\n"
        "Бот написан на Python."
    )