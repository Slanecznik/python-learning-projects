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
        ["/myid", "Telegram ID"],
        ["/users", "список пользователей"],
        ["/count", "количество пользователей"],
        ["/jobs", "список профессий"],
        ["/profiles", "профили пользователей"],
        ["/profile", "пример словаря"],
        ["/whoami", "мои данные Telegram"],
        ["/find", "поиск пользователя"]
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

# ========= КОМАНДА /users =========

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users_list = [
        ["Владимир", "Такси"],
        ["Анна", "Дизайнер"],
        ["Иван", "Программист"]
    ]

    message = "👥 Пользователи:\n\n"

    for user in users_list:

        message += f"{user[0]} — {user[1]}\n"

    await update.message.reply_text(message)

# ========= КОМАНДА /count =========

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users_list = [
        ["Владимир", "Такси"],
        ["Анна", "Дизайнер"],
        ["Иван", "Программист"]
    ]

    users_count = len(users_list)

    await update.message.reply_text(
        f"Всего пользователей: {users_count}"
    )

# ========= КОМАНДА /jobs =========

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users_list = [
        ["Владимир", "Такси"],
        ["Анна", "Дизайнер"],
        ["Иван", "Программист"]
    ]

    message = "💼 Профессии:\n\n"

    for user in users_list:

        message += f"• {user[1]}\n"

    await update.message.reply_text(message)

# ========= КОМАНДА /profiles =========

async def profiles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users_list = [
        {
            "name": "Владимир",
            "job": "Такси",
            "city": "Лодзь"
        },
        {
            "name": "Анна",
            "job": "Дизайнер",
            "city": "Варшава"
        },
        {
            "name": "Иван",
            "job": "Программист",
            "city": "Краков"
        }
    ]

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

    user = {
        "name": "Владимир",
        "job": "Такси",
        "city": "Лодзь"
    }

    message = (
        f"👤 Имя: {user['name']}\n"
        f"💼 Работа: {user['job']}\n"
        f"🏙 Город: {user['city']}"
    )

    await update.message.reply_text(message)

# ========= КОМАНДА /whoami =========

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = {
        "name": update.effective_user.first_name,
        "username": update.effective_user.username,
        "id": update.effective_user.id
    }

    message = (
        f"👤 Имя: {user['name']}\n"
        f"📛 Username: @{user['username']}\n"
        f"🆔 ID: {user['id']}"
    )

    await update.message.reply_text(message)

# ========= КОМАНДА /find =========

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # список пользователей
    users_list = [
        {
            "name": "Владимир",
            "job": "Такси",
            "city": "Лодзь"
        },
        {
            "name": "Анна",
            "job": "Дизайнер",
            "city": "Варшава"
        },
        {
            "name": "Иван",
            "job": "Программист",
            "city": "Краков"
        }
    ]

    # пользователь ничего не написал после команды
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например: /find Анна"
        )

        return

    # берём первое слово после команды
    search_name = context.args[0]

    # пока пользователь не найден
    found_user = None

    # перебираем всех пользователей
    for user in users_list:

        # сравниваем имя пользователя
        if user["name"] == search_name:

            found_user = user

    # если нашли пользователя
    if found_user:

        await update.message.reply_text(
            f"Найден:\n\n"
            f"👤 {found_user['name']}\n"
            f"💼 {found_user['job']}\n"
            f"🏙 {found_user['city']}"
        )

    # если не нашли
    else:

        await update.message.reply_text(
            "Пользователь не найден"
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
    CommandHandler("users", users)
)

app.add_handler(
    CommandHandler("count", count)
)

app.add_handler(
    CommandHandler("jobs", jobs)
)

app.add_handler(
    CommandHandler("profiles", profiles)
)

app.add_handler(
    CommandHandler("profile", profile)
)

app.add_handler(CommandHandler("whoami", whoami))

app.add_handler(
    CommandHandler("find", find)
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