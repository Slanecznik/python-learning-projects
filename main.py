# ========= ИМПОРТЫ =========

# работа со временем
from datetime import datetime

# загрузка переменных из .env
from dotenv import load_dotenv

# работа с переменными окружения
import os

# импорт объектов Telegram
from telegram import Update

# импорт инструментов Telegram-бота
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ========= ЗАГРУЖАЕМ .ENV =========

# загружаем секреты из файла .env
load_dotenv()

# получаем токен бота
TOKEN = os.getenv("BOT_TOKEN")

# ========= КОМАНДА /start =========

# async = функция может работать асинхронно
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # reply_text() отправляет сообщение пользователю
    await update.message.reply_text(
        "Привет! 👋\n"
        "Я твой Telegram-бот.\n\n"
        "Напиши /help"
    )

# ========= КОМАНДА /help =========

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📚 Команды бота:\n\n"
        "/start - запуск бота\n"
        "/help - список команд\n"
        "/about - информация\n"
        "/time - текущее время"
    )

# ========= КОМАНДА /about =========

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Это мой первый backend-проект.\n"
        "Бот написан на Python."
    )

# ========= КОМАНДА /time =========

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # получаем текущее время
    now = datetime.now()

    # форматируем время красиво
    current_time = now.strftime("%H:%M:%S")

    await update.message.reply_text(
        f"⏰ Сейчас время: {current_time}"
    )

# ========= СОЗДАЁМ ПРИЛОЖЕНИЕ =========

# создаём Telegram-приложение
app = Application.builder().token(TOKEN).build()

# ========= HANDLERS =========

# если человек написал /start
# вызывается функция start()
app.add_handler(
    CommandHandler("start", start)
)

# если человек написал /help
app.add_handler(
    CommandHandler("help", help_command)
)

# если человек написал /about
app.add_handler(
    CommandHandler("about", about)
)

# если человек написал /time
app.add_handler(
    CommandHandler("time", time_command)
)

# ========= ЗАПУСК БОТА =========

print("Бот запущен 🚀")

# запускаем бесконечную работу бота
app.run_polling()