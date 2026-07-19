from commands import register_handlers

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

from database import (
    load_users,
    save_users,
)

users_list = load_users()

from search import (
    find_user,
    find_city,
    find_job,
    count_by,
    make_stats_message,
)

from commands import register_handlers
from commands import about

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
        ["/jobstats", "статистика профессий"],
        ["/citystats", "статистика городов"],
        ["/adduser", "добавить пользователя"],
        ["/deleteuser", "удалить пользователя"],
        ["/edituser", "изменить пользователя"],
    ]

    message = "📚 Команды бота:\n\n"

    for command in commands:

        message += f"{command[0]} - {command[1]}\n"

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

    jobs = count_by("job")

    message = make_stats_message(
        "📊 Статистика профессий",
        jobs
    )

    await update.message.reply_text(message)

# ========= КОМАНДА /citystats =========

async def citystats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cities = count_by("city")

    message = make_stats_message(
        "📊 Статистика городов",
        cities
    )

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

# ========= КОМАНДА /adduser =========

async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # проверяем количество аргументов
    if len(context.args) != 3:

        await update.message.reply_text(
            "Например:\n/adduser Сергей Таксист Познань"
        )

        return

    # получаем данные
    name = context.args[0]
    job = context.args[1]
    city = context.args[2]

    # создаём нового пользователя
    new_user = {
        "name": name,
        "job": job,
        "city": city
    }

    # добавляем в список
    users_list.append(new_user)

    save_users(users_list)

    await update.message.reply_text(
        f"✅ Пользователь {name} добавлен"
    )

# ========= КОМАНДА /deleteuser =========

async def deleteuser(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/deleteuser Иван"
        )

        return

    search_name = context.args[0]

    user = find_user(search_name)

    if user:

        users_list.remove(user)

        save_users(users_list)

        await update.message.reply_text(
            f"✅ Пользователь {search_name} удалён"
        )

    else:

        await update.message.reply_text(
            "❌ Пользователь не найден"
        )

# ========= КОМАНДА /edituser =========

async def edituser(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 3:

        await update.message.reply_text(
            "Например:\n/edituser Иван Python Минск"
        )

        return

    search_name = context.args[0]
    new_job = context.args[1]
    new_city = context.args[2]

    user = find_user(search_name)

    if user:

        user["job"] = new_job
        user["city"] = new_city

        save_users(users_list)

        await update.message.reply_text(
            f"✅ Пользователь {search_name} обновлён"
        )

    else:

        await update.message.reply_text(
            "❌ Пользователь не найден"
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



# ========= ЗАПУСК БОТА =========

print("Бот запущен 🚀")

app.run_polling()