# ==================================================
# ИМПОРТЫ
# ==================================================

# os
# нужен для работы с переменными окружения (.env)
import os

# load_dotenv()
# загружает переменные из файла .env
from dotenv import load_dotenv

# Update
# объект с информацией о сообщении пользователя
from telegram import Update

# telegram.ext
# инструменты для создания логики бота
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# ==================================================
# ЗАГРУЖАЕМ .ENV
# ==================================================

# читаем файл .env
load_dotenv()

# получаем BOT_TOKEN из .env
TOKEN = os.getenv("BOT_TOKEN")


# ==================================================
# КОМАНДА /start
# ==================================================

# async
# асинхронная функция
# бот может одновременно работать со многими людьми

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # reply_text()
    # отправляет сообщение пользователю
    await update.message.reply_text(
        "Привет 👋\n"
        "Я твой Telegram-бот 😎"
    )


# ==================================================
# КОМАНДА /help
# ==================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Доступные команды:\n"
        "/start\n"
        "/help\n"
        "/about"
    )


# ==================================================
# КОМАНДА /about
# ==================================================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Меня создал Владимир 🔥"
    )


# ==================================================
# ФУНКЦИЯ АНАЛИЗА СООБЩЕНИЙ
# ==================================================

# handle_message()
# главная функция обработки текста

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # text
    # сообщение пользователя

    # lower()
    # переводит текст в маленькие буквы
    # чтобы "ПРИВЕТ" и "привет" работали одинаково

    user_message = update.message.text.lower()


    # ==================================================
    # ЛОГИКА БОТА
    # ==================================================

    # if
    # проверка условия

    if "привет" in user_message:

        await update.message.reply_text(
            "И тебе привет 😎"
        )


    # elif
    # дополнительная проверка

    elif "как дела" in user_message:

        await update.message.reply_text(
            "У меня всё отлично 🚀"
        )


    elif "python" in user_message:

        await update.message.reply_text(
            "Python отлично подходит для backend разработки 🔥"
        )


    elif "бот" in user_message:

        await update.message.reply_text(
            "Да, я настоящий Telegram-бот 😎"
        )


    # else
    # выполняется если условия выше не подошли

    else:

        await update.message.reply_text(
            f"Ты написал: {user_message}"
        )


# ==================================================
# СОЗДАЁМ ПРИЛОЖЕНИЕ
# ==================================================

# Application
# главный объект бота

# builder()
# создаёт приложение

# token(TOKEN)
# подключение к Telegram API

app = Application.builder().token(TOKEN).build()


# ==================================================
# ПОДКЛЮЧАЕМ КОМАНДЫ
# ==================================================

# CommandHandler
# ловит команды типа /start

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))


# ==================================================
# ОБРАБОТКА ОБЫЧНОГО ТЕКСТА
# ==================================================

# MessageHandler
# обрабатывает обычные сообщения

# filters.TEXT
# только текст

app.add_handler(MessageHandler(filters.TEXT, handle_message))


# ==================================================
# ЗАПУСК БОТА
# ==================================================

print("Бот запущен 🚀")

# run_polling()
# бесконечный цикл:
# бот постоянно спрашивает Telegram:
# "Есть новые сообщения?"

app.run_polling()