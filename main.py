# ========= ИМПОРТЫ =========

from datetime import datetime
from dotenv import load_dotenv
import os

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ========= ЗАГРУЖАЕМ .ENV =========

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# ========= КОМАНДА /start =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    name = update.effective_user.first_name

    await update.message.reply_text(
        f"Привет, {name}! 👋\n\n"
        "Я твой Telegram-бот.\n"
        "Напиши /help"
    )

# ========= КОМАНДА /help =========

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    commands = [
        ["/start", "запуск бота"],
        ["/help", "список команд"],
        ["/about", "информация о проекте"],
        ["/time", "текущее время"],
        ["/me", "данные пользователя"],
        ["/myid", "Telegram ID"]
    ]

    message = "📚 Команды бота:\n\n"

    for command in commands:

        message += f"{command[0]} - {command[1]}\n"

    await update.message.reply_text(message)

# ========= КОМАНДА /about =========

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Это мой первый backend-проект.\n"
        "Бот написан на Python."
    )

# ========= КОМАНДА /me =========

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):

    name = update.effective_user.first_name
    username = update.effective_user.username
    user_id = update.effective_user.id

    message = (
        f"👤 Имя: {name}\n"
        f"📛 Username: @{username}\n"
        f"🆔 ID: {user_id}"
    )

    await update.message.reply_text(message)

# ========= КОМАНДА /myid =========

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        f"Твой Telegram ID: {user_id}"
    )

# ========= КОМАНДА /time =========

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    await update.message.reply_text(
        f"⏰ Сейчас время: {current_time}"
    )

# ========= ОБЫЧНЫЕ СООБЩЕНИЯ =========

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text.lower()

    if "привет" in user_text:

        await update.message.reply_text(
            "Привет! 👋"
        )

    elif "как дела" in user_text:

        await update.message.reply_text(
            "Отлично 😎"
        )

    elif "python" in user_text:

        await update.message.reply_text(
            "Лучший язык для старта 🔥"
        )

    elif "бот" in user_text:

        await update.message.reply_text(
            "Да, я Telegram-бот 🤖"
        )

    elif "такси" in user_text:

        await update.message.reply_text(
            "Владимир сейчас работает в такси 🚕"
        )

    elif "лодзь" in user_text:

        await update.message.reply_text(
            "Лодзь — город в Польше 🇵🇱"
        )

    else:

        await update.message.reply_text(
            "Я пока не знаю такой фразы 🤔"
        )

# ========= СОЗДАЁМ ПРИЛОЖЕНИЕ =========

app = Application.builder().token(TOKEN).build()

# ========= HANDLERS =========

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("help", help_command)
)

app.add_handler(
    CommandHandler("about", about)
)

app.add_handler(
    CommandHandler("me", me)
)

app.add_handler(
    CommandHandler("myid", myid)
)

app.add_handler(
    CommandHandler("time", time_command)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_message
    )
)

# ========= ЗАПУСК БОТА =========

print("Бот запущен 🚀")

app.run_polling()