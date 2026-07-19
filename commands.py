from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import load_users
users_list = load_users()
# ========= КОМАНДА /about =========

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Это мой первый backend-проект.\n"
        "Бот написан на Python."
    )

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


# ========= КОМАНДА /users =========

# Показывает список пользователей
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Заголовок
    message = "👥 Пользователи:\n\n"

    # Перебираем список
    for user in users_list:
        # Добавляем пользователя
        message += f"{user['name']} — {user['job']}\n"

    # Отправляем сообщение
    await update.message.reply_text(message)


# ========= КОМАНДА /count =========

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users_count = len(users_list)

    await update.message.reply_text(
        f"Всего пользователей: {users_count}"
    )


# ========= КОМАНДА /jobs =========

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "💼 Профессии:\n\n"

    for user in users_list:
        message += f"• {user['job']}\n"

    await update.message.reply_text(message)


# ========= КОМАНДА /profiles =========

async def profiles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "📋 Профили:\n\n"

    for user in users_list:
        message += (
            f"👤 {user['name']}\n"
            f"💼 {user['job']}\n"
            f"🏙 {user['city']}\n\n"
        )

    await update.message.reply_text(message)


# ========= КОМАНДА /profile =========

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users_list[0]

    message = (
        f"👤 Имя: {user['name']}\n"
        f"💼 Работа: {user['job']}\n"
        f"🏙 Город: {user['city']}"
    )

    await update.message.reply_text(message)


def register_handlers(app):
    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("about", about)
    )

    app.add_handler(CommandHandler("whoami", whoami))

    app.add_handler(
        CommandHandler("find", find)
    )

    app.add_handler(
        CommandHandler("job", job)
    )

    app.add_handler(
        CommandHandler("cities", cities)
    )

    app.add_handler(
        CommandHandler("findcity", findcity)
    )

    app.add_handler(
        CommandHandler("stats", stats)
    )

    app.add_handler(
        CommandHandler("uniquejobs", uniquejobs)
    )

    app.add_handler(
        CommandHandler("jobstats", jobstats)
    )

    app.add_handler(
        CommandHandler("citystats", citystats)
    )

    app.add_handler(
        CommandHandler("hasjob", hasjob)
    )

    app.add_handler(
        CommandHandler("adduser", adduser)
    )

    app.add_handler(
        CommandHandler("deleteuser", deleteuser)
    )

    app.add_handler(
        CommandHandler("edituser", edituser)
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