import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# загружаем .env
load_dotenv()

# берём токен
TOKEN = os.getenv("BOT_TOKEN")


# -------- КОМАНДА /start --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋\n"
        "Я твой первый Telegram-бот."
    )


# -------- КОМАНДА /help --------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n"
        "/start\n"
        "/help\n"
        "/about"
    )


# -------- КОМАНДА /about --------

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я бот, которого создал Владимир 😎"
    )


# -------- ОТВЕТ НА ЛЮБОЙ ТЕКСТ --------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text.lower()

    # приветствие
    if "привет" in user_message:
        await update.message.reply_text(
            "Привет 😎"
        )

    # как делаы
    elif "как дела" in user_message:
        await update.message.reply_text(
            "У меня всё отлично 🚀"
        )

    # python
    elif "python" in user_message:
        await update.message.reply_text(
            "Python — лучший язык для старта 🔥"
        )

    # если ничего не найдено
    else:
        await update.message.reply_text(
            f"Ты написал: {user_message}"
        )

# -------- СОЗДАЁМ БОТА --------

app = Application.builder().token(TOKEN).build()

# команды
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))

# обычные сообщения
app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

# запуск
print("Бот запущен 🚀")

app.run_polling()