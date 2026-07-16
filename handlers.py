from telegram import Update
from telegram.ext import ContextTypes


# Здесь находятся команды,
# связанные с пользователем.


# ========= КОМАНДА /start =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем имя пользователя
    name = update.effective_user.first_name

    # Отправляем приветствие
    await update.message.reply_text(
        f"Привет, {name}! 👋\n\n"
        "Я твой Telegram-бот.\n"
        "Напиши /help"
    )


# ========= КОМАНДА /me =========

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем данные Telegram
    name = update.effective_user.first_name
    username = update.effective_user.username
    user_id = update.effective_user.id

    # Формируем сообщение
    message = (
        f"👤 Имя: {name}\n"
        f"📛 Username: @{username}\n"
        f"🆔 ID: {user_id}"
    )

    # Отправляем сообщение
    await update.message.reply_text(message)


# ========= КОМАНДА /myid =========

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем ID пользователя
    user_id = update.effective_user.id

    # Отправляем ID
    await update.message.reply_text(
        f"Твой Telegram ID: {user_id}"
    )