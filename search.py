from database import load_users_sqlite
import sqlite3
users_list = load_users_sqlite()


# ========= УНИВЕРСАЛЬНЫЙ ПОИСК =========

def find_by(field, value):

    for user in users_list:

        if user[field].lower() == value.lower():

            return user

    return None

# ========= УНИВЕРСАЛЬНЫЙ СЧЁТЧИК =========

def count_by(field):

    counter = {}

    for user in users_list:

        value = user[field]

        if value in counter:

            counter[value] += 1

        else:

            counter[value] = 1

    return counter

# ========= ПОИСК ПО ИМЕНИ =========

def find_user(name):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Ищем пользователя
    cursor.execute("""
    SELECT name, job, city
    FROM users
    WHERE name = ?
    """, (name,))

    # Получаем одну запись
    row = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    # Если пользователь найден
    if row:

        return {
            "name": row[0],
            "job": row[1],
            "city": row[2]
        }

    # Если не найден
    return None

# ==================================================
# Поиск пользователей по городу
# ==================================================

def find_city(city):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Выполняем SQL-запрос
    cursor.execute("""
    SELECT name, job, city
    FROM users
    WHERE city = ?
    """, (city,))

    # Получаем все найденные записи
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список пользователей
    users = []

    # Преобразуем кортежи в словари
    for row in rows:

        user = {
            "name": row[0],
            "job": row[1],
            "city": row[2]
        }

        users.append(user)

    # Возвращаем список
    return users


# ========= ПОИСК ПО ПРОФЕССИИ =========

def find_job(job):
    return find_by("job", job)

# ========= СОЗДАНИЕ СООБЩЕНИЯ =========

def make_stats_message(title, data):

    message = f"{title}\n\n"

    for key in data:

        message += f"{key}: {data[key]}\n"

    return message