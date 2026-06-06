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
    MessageHandler,
    ContextTypes,
    filters,
)

# ========= ЗАГРУЖАЕМ .ENV =========

# загружаем секреты из файла .env
load_dotenv()

# получаем токен бота
TOKEN = os.getenv("BOT_TOKEN")

# ========= КОМАНДА /start =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем имя пользователя из Telegram
    name = update.effective_user.first_name

    # Отправляем персональное приветствие
    await update.message.reply_text(
        f"Привет, {name}! 👋\n\n"
        "Я твой Telegram-бот.\n"
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

# ========= КОМАНДА /me =========

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем имя пользователя
    name = update.effective_user.first_name

    # Получаем username
    username = update.effective_user.username

    await update.message.reply_text(
        f"Имя: {name}\n"
        f"Username: @{username}"
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

# ========= ОБЫЧНЫЕ СООБЩЕНИЯ =========

# Эта функция вызывается,
# когда пользователь пишет обычное сообщение

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем текст пользователя
    user_text = update.message.text.lower()

    # Если в сообщении есть слово "привет"
    if "привет" in user_text:

        await update.message.reply_text(
            "Привет! 👋"
        )

    # Если в сообщении есть фраза "как дела"
    elif "как дела" in user_text:

        await update.message.reply_text(
            "Отлично 😎"
        )

    # Если в сообщении есть слово python
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


    # Если ничего не подошло
    else:

        await update.message.reply_text(
            "Я пока не знаю такой фразы 🤔"
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

app.add_handler(CommandHandler("me", me))

# если человек написал /time
app.add_handler(
    CommandHandler("time", time_command)
)

# Обрабатываем обычный текст

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_message
    )
)



# ========= ЗАПУСК БОТА =========

print("Бот запущен 🚀")

# запускаем бесконечную работу бота
app.run_polling()