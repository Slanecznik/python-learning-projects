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

from commands import about

# ========= ЗАГРУЖАЕМ .ENV =========

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

from users import users_list

from search import (
    find_user,
    find_city,
    find_job,
)

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
        ["/find", "поиск пользователя"],
        ["/cities", "список городов"],
        ["/findcity", "поиск по городу"],
        ["/stats", "статистика"],
        ["/uniquejobs", "профессии без повторов"],
        ["/hasjob", "проверить профессию"],
        ["/job", "показать профессию"],
        ["/jobstats", "статистика профессий"]
    ]

    message = "📚 Команды бота:\n\n"

    for command in commands:

        message += f"{command[0]} - {command[1]}\n"

    await update.message.reply_text(message)

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

    message = "👥 Пользователи:\n\n"

    for user in users_list:
        # добавляем имя и профессию
        message += f"{user['name']} — {user['job']}\n"

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
        # добавляем профессию
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

    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/find Владимир"
        )

        return

    search_name = context.args[0]

    user = find_user(search_name)

    if user:

        await update.message.reply_text(
            f"👤 {user['name']}\n"
            f"💼 {user['job']}\n"
            f"🏙 {user['city']}"
        )

    else:

        await update.message.reply_text(
            "❌ Пользователь не найден"
        )

# ========= КОМАНДА /job =========

async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # если имя не указано
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например: /job Владимир"
        )

        return

    # получаем имя после команды
    search_name = context.args[0]

    # перебираем пользователей
    # ищем пользователя
    user = find_user(search_name)

    # если нашли
    if user:

        await update.message.reply_text(
            f"💼 Профессия: {user['job']}"
        )

    # если не нашли
    else:

        await update.message.reply_text(
            "❌ Пользователь не найден"
        )

# ========= КОМАНДА /cities =========

async def cities(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # начинаем формировать сообщение
    message = "🏙 Города:\n\n"

    # перебираем пользователей
    for user in users_list:

        # добавляем город в сообщение
        message += f"• {user['city']}\n"

    # отправляем ответ
    await update.message.reply_text(message)

# ========= КОМАНДА /findcity =========

async def findcity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # если город не указан
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например: /findcity Лодзь"
        )

        return

    # берём город после команды
    search_city = context.args[0]

    # ищем пользователя по городу
    found_user = find_city(search_city)

    # если нашли
    if found_user:

        await update.message.reply_text(
            f"👤 {found_user['name']}\n"
            f"💼 {found_user['job']}\n"
            f"🏙 {found_user['city']}"
        )

    # если не нашли
    else:

        await update.message.reply_text(
            "Город не найден"
        )

# ========= КОМАНДА /stats =========

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # считаем пользователей
    users_count = len(users_list)

    # начинаем с нуля
    jobs_count = 0
    cities_count = 0

    # перебираем пользователей
    for user in users_list:

        # увеличиваем счётчик профессий
        jobs_count += 1

        # увеличиваем счётчик городов
        cities_count += 1

    # отправляем статистику
    await update.message.reply_text(
        f"📊 Статистика\n\n"
        f"👥 Пользователей: {users_count}\n"
        f"💼 Профессий: {jobs_count}\n"
        f"🏙 Городов: {cities_count}"
    )

# ========= КОМАНДА /uniquejobs =========

async def uniquejobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # создаём пустое множество
    jobs = set()

    # перебираем пользователей
    for user in users_list:

        # добавляем профессию
        jobs.add(user["job"])

    # начинаем сообщение
    message = "💼 Профессии:\n\n"

    # перебираем множество
    for job in jobs:

        # добавляем профессию в сообщение
        message += f"• {job}\n"

    # отправляем ответ
    await update.message.reply_text(message)

# ========= КОМАНДА /jobstats =========

async def jobstats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    jobs = {}

    for user in users_list:

        job = user["job"]

        if job in jobs:

            jobs[job] += 1

        else:

            jobs[job] = 1

    message = "📊 Статистика профессий\n\n"

    for job in jobs:

        message += f"{job}: {jobs[job]}\n"

    await update.message.reply_text(message)

# ========= КОМАНДА /hasjob =========

async def hasjob(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # если пользователь ничего не написал
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например: /hasjob Такси"
        )

        return

    # получаем профессию
    search_job = context.args[0]

    # ищем профессию
    user = find_job(search_job)

    # если нашли
    if user:

        await update.message.reply_text(
            "✅ Профессия найдена"
        )

    # если не нашли
    else:

        await update.message.reply_text(
            "❌ Такой профессии нет"
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
    CommandHandler("hasjob", hasjob)
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