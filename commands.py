# ==================================================
#                    ИМПОРТЫ
# ==================================================

from datetime import datetime

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from database import (
    load_users,
    save_users,
)

from search import (
    find_user,
    find_city,
    find_job,
    count_by,
    make_stats_message,
)


# ==================================================
#               ЗАГРУЖАЕМ ПОЛЬЗОВАТЕЛЕЙ
# ==================================================

# Загружаем список пользователей из JSON-файла
users_list = load_users()


# ==================================================
#                 ОСНОВНЫЕ КОМАНДЫ
# ==================================================


# --------------------------------------------------
# Команда /start
# --------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем имя пользователя
    name = update.effective_user.first_name

    # Отправляем приветствие
    await update.message.reply_text(
        f"Привет, {name}! 👋\n\n"
        "Я твой Telegram-бот.\n"
        "Напиши /help"
    )


# --------------------------------------------------
# Команда /help
# --------------------------------------------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    commands = [
        ["/start", "запуск бота"],
        ["/help", "список команд"],
        ["/about", "информация о проекте"],
        ["/time", "текущее время"],

        ["/me", "данные пользователя"],
        ["/myid", "Telegram ID"],
        ["/whoami", "мои данные Telegram"],

        ["/users", "список пользователей"],
        ["/count", "количество пользователей"],
        ["/jobs", "список профессий"],
        ["/profiles", "все профили"],
        ["/profile", "пример профиля"],
        ["/cities", "список городов"],

        ["/find", "поиск пользователя"],
        ["/findcity", "поиск по городу"],
        ["/job", "профессия пользователя"],
        ["/hasjob", "проверка профессии"],

        ["/stats", "общая статистика"],
        ["/jobstats", "статистика профессий"],
        ["/citystats", "статистика городов"],
        ["/uniquejobs", "профессии без повторов"],

        ["/adduser", "добавить пользователя"],
        ["/edituser", "изменить пользователя"],
        ["/deleteuser", "удалить пользователя"],
    ]

    message = "📚 Команды бота:\n\n"

    for command in commands:
        message += f"{command[0]} - {command[1]}\n"

    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /about
# --------------------------------------------------

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Это мой первый backend-проект.\n"
        "Бот написан на Python."
    )


# ==================================================
#            КОМАНДЫ TELEGRAM
# ==================================================


# --------------------------------------------------
# Команда /me
# --------------------------------------------------

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


# --------------------------------------------------
# Команда /myid
# --------------------------------------------------

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        f"Твой Telegram ID: {user_id}"
    )


# --------------------------------------------------
# Команда /whoami
# --------------------------------------------------

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = {
        "name": update.effective_user.first_name,
        "username": update.effective_user.username,
        "id": update.effective_user.id,
    }

    message = (
        f"👤 Имя: {user['name']}\n"
        f"📛 Username: @{user['username']}\n"
        f"🆔 ID: {user['id']}"
    )

    await update.message.reply_text(message)

# ==================================================
#          ПРОСМОТР ПОЛЬЗОВАТЕЛЕЙ
# ==================================================


# --------------------------------------------------
# Команда /users
# --------------------------------------------------

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Заголовок сообщения
    message = "👥 Пользователи:\n\n"

    # Перебираем всех пользователей
    for user in users_list:

        message += f"{user['name']} — {user['job']}\n"

    # Отправляем сообщение
    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /profile
# --------------------------------------------------

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Берём первого пользователя
    user = users_list[0]

    message = (
        f"👤 Имя: {user['name']}\n"
        f"💼 Работа: {user['job']}\n"
        f"🏙 Город: {user['city']}"
    )

    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /profiles
# --------------------------------------------------

async def profiles(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = "📋 Профили пользователей:\n\n"

    # Перебираем пользователей
    for user in users_list:

        message += (
            f"👤 {user['name']}\n"
            f"💼 {user['job']}\n"
            f"🏙 {user['city']}\n\n"
        )

    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /count
# --------------------------------------------------

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users_count = len(users_list)

    await update.message.reply_text(
        f"👥 Всего пользователей: {users_count}"
    )


# --------------------------------------------------
# Команда /jobs
# --------------------------------------------------

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = "💼 Профессии:\n\n"

    # Перебираем пользователей
    for user in users_list:

        message += f"• {user['job']}\n"

    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /cities
# --------------------------------------------------

async def cities(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = "🏙 Города:\n\n"

    # Перебираем пользователей
    for user in users_list:

        message += f"• {user['city']}\n"

    await update.message.reply_text(message)

# ==================================================
#                    ПОИСК
# ==================================================


# --------------------------------------------------
# Команда /find
# --------------------------------------------------

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем, указано ли имя
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/find Владимир"
        )

        return

    # Получаем имя
    search_name = context.args[0]

    # Ищем пользователя
    user = find_user(search_name)

    # Если нашли
    if user:

        await update.message.reply_text(
            f"👤 {user['name']}\n"
            f"💼 {user['job']}\n"
            f"🏙 {user['city']}"
        )

    # Если не нашли
    else:

        await update.message.reply_text(
            "❌ Пользователь не найден"
        )


# --------------------------------------------------
# Команда /findcity
# --------------------------------------------------

async def findcity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем, указан ли город
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/findcity Лодзь"
        )

        return

    # Получаем название города
    search_city = context.args[0]

    # Ищем пользователя
    found_user = find_city(search_city)

    # Если нашли
    if found_user:

        await update.message.reply_text(
            f"👤 {found_user['name']}\n"
            f"💼 {found_user['job']}\n"
            f"🏙 {found_user['city']}"
        )

    # Если не нашли
    else:

        await update.message.reply_text(
            "❌ Город не найден"
        )


# --------------------------------------------------
# Команда /job
# --------------------------------------------------

async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем, указано ли имя
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/job Владимир"
        )

        return

    # Получаем имя пользователя
    search_name = context.args[0]

    # Ищем пользователя
    user = find_user(search_name)

    # Если нашли
    if user:

        await update.message.reply_text(
            f"💼 Профессия: {user['job']}"
        )

    # Если не нашли
    else:

        await update.message.reply_text(
            "❌ Пользователь не найден"
        )


# --------------------------------------------------
# Команда /hasjob
# --------------------------------------------------

async def hasjob(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем, указана ли профессия
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/hasjob Таксист"
        )

        return

    # Получаем профессию
    search_job = context.args[0]

    # Ищем профессию
    user = find_job(search_job)

    # Если нашли
    if user:

        await update.message.reply_text(
            "✅ Профессия найдена"
        )

    # Если не нашли
    else:

        await update.message.reply_text(
            "❌ Такой профессии нет"
        )

# ==================================================
#                  СТАТИСТИКА
# ==================================================


# --------------------------------------------------
# Команда /stats
# --------------------------------------------------

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Количество пользователей
    users_count = len(users_list)

    # Начинаем счётчики
    jobs_count = 0
    cities_count = 0

    # Перебираем пользователей
    for user in users_list:

        jobs_count += 1
        cities_count += 1

    # Отправляем статистику
    await update.message.reply_text(
        f"📊 Статистика\n\n"
        f"👥 Пользователей: {users_count}\n"
        f"💼 Профессий: {jobs_count}\n"
        f"🏙 Городов: {cities_count}"
    )


# --------------------------------------------------
# Команда /jobstats
# --------------------------------------------------

async def jobstats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем статистику профессий
    jobs = count_by("job")

    # Формируем сообщение
    message = make_stats_message(
        "📊 Статистика профессий",
        jobs
    )

    # Отправляем сообщение
    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /citystats
# --------------------------------------------------

async def citystats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем статистику городов
    cities = count_by("city")

    # Формируем сообщение
    message = make_stats_message(
        "📊 Статистика городов",
        cities
    )

    # Отправляем сообщение
    await update.message.reply_text(message)


# --------------------------------------------------
# Команда /uniquejobs
# --------------------------------------------------

async def uniquejobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Создаём множество
    jobs = set()

    # Собираем уникальные профессии
    for user in users_list:

        jobs.add(user["job"])

    # Формируем сообщение
    message = "💼 Профессии без повторов:\n\n"

    # Добавляем профессии
    for job in jobs:

        message += f"• {job}\n"

    # Отправляем сообщение
    await update.message.reply_text(message)

# ==================================================
#              ИЗМЕНЕНИЕ ДАННЫХ
# ==================================================


# --------------------------------------------------
# Команда /adduser
# --------------------------------------------------

async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем количество аргументов
    if len(context.args) != 3:

        await update.message.reply_text(
            "Например:\n/adduser Сергей Таксист Познань"
        )

        return

    # Получаем данные пользователя
    name = context.args[0]
    job = context.args[1]
    city = context.args[2]

    # Создаём словарь нового пользователя
    new_user = {
        "name": name,
        "job": job,
        "city": city
    }

    # Добавляем пользователя
    users_list.append(new_user)

    # Сохраняем изменения
    save_users(users_list)

    # Отправляем сообщение
    await update.message.reply_text(
        f"✅ Пользователь {name} успешно добавлен."
    )


# --------------------------------------------------
# Команда /edituser
# --------------------------------------------------

async def edituser(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем количество аргументов
    if len(context.args) != 3:

        await update.message.reply_text(
            "Например:\n/edituser Иван Python Минск"
        )

        return

    # Получаем данные
    search_name = context.args[0]
    new_job = context.args[1]
    new_city = context.args[2]

    # Ищем пользователя
    user = find_user(search_name)

    # Если нашли
    if user:

        user["job"] = new_job
        user["city"] = new_city

        # Сохраняем изменения
        save_users(users_list)

        await update.message.reply_text(
            f"✅ Пользователь {search_name} успешно обновлён."
        )

    # Если не нашли
    else:

        await update.message.reply_text(
            "❌ Пользователь не найден."
        )


# --------------------------------------------------
# Команда /deleteuser
# --------------------------------------------------

async def deleteuser(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем наличие имени
    if len(context.args) == 0:

        await update.message.reply_text(
            "Например:\n/deleteuser Иван"
        )

        return

    # Получаем имя пользователя
    search_name = context.args[0]

    # Ищем пользователя
    user = find_user(search_name)

    # Если нашли
    if user:

        # Удаляем пользователя
        users_list.remove(user)

        # Сохраняем изменения
        save_users(users_list)

        await update.message.reply_text(
            f"✅ Пользователь {search_name} успешно удалён."
        )

    # Если не нашли
    else:

        await update.message.reply_text(
            "❌ Пользователь не найден."
        )

# ==================================================
#              СЛУЖЕБНЫЕ КОМАНДЫ
# ==================================================


# --------------------------------------------------
# Команда /time
# --------------------------------------------------

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем текущее время
    now = datetime.now()

    # Форматируем время
    current_time = now.strftime("%H:%M:%S")

    # Отправляем пользователю
    await update.message.reply_text(
        f"⏰ Сейчас время: {current_time}"
    )


# ==================================================
#             ОБЫЧНЫЕ СООБЩЕНИЯ
# ==================================================


# --------------------------------------------------
# Обработка обычных сообщений
# --------------------------------------------------

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем сообщение пользователя
    user_text = update.message.text.lower()

    if "привет" in user_text:

        await update.message.reply_text("Привет! 👋")

    elif "как дела" in user_text:

        await update.message.reply_text("Отлично 😎")

    elif "python" in user_text:

        await update.message.reply_text("Лучший язык для старта 🔥")

    elif "бот" in user_text:

        await update.message.reply_text("Да, я Telegram-бот 🤖")

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


# ==================================================
#          РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ
# ==================================================

def register_handlers(app):

    # ------------------------------
    # Основные команды
    # ------------------------------

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))

    # ------------------------------
    # Telegram
    # ------------------------------

    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("whoami", whoami))

    # ------------------------------
    # Просмотр пользователей
    # ------------------------------

    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("profiles", profiles))
    app.add_handler(CommandHandler("count", count))
    app.add_handler(CommandHandler("jobs", jobs))
    app.add_handler(CommandHandler("cities", cities))

    # ------------------------------
    # Поиск
    # ------------------------------

    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("findcity", findcity))
    app.add_handler(CommandHandler("job", job))
    app.add_handler(CommandHandler("hasjob", hasjob))

    # ------------------------------
    # Статистика
    # ------------------------------

    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("jobstats", jobstats))
    app.add_handler(CommandHandler("citystats", citystats))
    app.add_handler(CommandHandler("uniquejobs", uniquejobs))

    # ------------------------------
    # Изменение данных
    # ------------------------------

    app.add_handler(CommandHandler("adduser", adduser))
    app.add_handler(CommandHandler("edituser", edituser))
    app.add_handler(CommandHandler("deleteuser", deleteuser))

    # ------------------------------
    # Служебные команды
    # ------------------------------

    app.add_handler(CommandHandler("time", time_command))

    # ------------------------------
    # Обычные сообщения
    # ------------------------------

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_message
        )
    )