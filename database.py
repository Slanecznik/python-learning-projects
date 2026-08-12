import json
import sqlite3


def load_users():
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)

    return users


def save_users(users):
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=4
        )


# ==================================================
# Получить пользователей из SQLite
# ==================================================

def load_users_sqlite():
    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Выполняем SQL-запрос
    cursor.execute("""
            SELECT name, job, city
            FROM users
            """)

    # Получаем все записи
    rows = cursor.fetchall()

    # Создаём пустой список
    users = []

    # Преобразуем кортежи в словари
    for row in rows:
        user = {
            "name": row[0],
            "job": row[1],
            "city": row[2]
        }

        users.append(user)

    # Закрываем соединение
    connection.close()

    # Возвращаем список
    return users

# ==================================================
#              СТАТИСТИКА ПО ПРОФЕССИЯМ
# ==================================================

def count_users_by_job():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Получаем количество пользователей
    # по каждой профессии
    cursor.execute("""
    SELECT job, COUNT(*)
    FROM users
    GROUP BY job
    """)

    # Получаем все результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Превращаем результат в словарь
    statistics = {}

    for row in rows:

        statistics[row[0]] = row[1]

    return statistics


# ==================================================
#                СТАТИСТИКА ПО ГОРОДАМ
# ==================================================

def count_users_by_city():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Получаем количество пользователей
    # по каждому городу
    cursor.execute("""
    SELECT city, COUNT(*)
    FROM users
    GROUP BY city
    """)

    # Получаем все результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Превращаем результат в словарь
    statistics = {}

    for row in rows:

        statistics[row[0]] = row[1]

    return statistics

# ==================================================
#             ОБЩАЯ СТАТИСТИКА
# ==================================================

def get_total_users():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Считаем всех пользователей
    cursor.execute("""
    SELECT COUNT(*)
    FROM users
    """)

    # Получаем результат
    result = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    # Возвращаем число пользователей
    return result[0]


# ==================================================
#          КОЛИЧЕСТВО УНИКАЛЬНЫХ ПРОФЕССИЙ
# ==================================================

def get_unique_jobs_count():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Считаем уникальные профессии
    cursor.execute("""
    SELECT COUNT(DISTINCT job)
    FROM users
    """)

    # Получаем результат
    result = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    # Возвращаем количество профессий
    return result[0]


# ==================================================
#             КОЛИЧЕСТВО УНИКАЛЬНЫХ ГОРОДОВ
# ==================================================

def get_unique_cities_count():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Считаем уникальные города
    cursor.execute("""
    SELECT COUNT(DISTINCT city)
    FROM users
    """)

    # Получаем результат
    result = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    # Возвращаем количество городов
    return result[0]

# ==================================================
#              ПОЛУЧИТЬ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
# ==================================================

def get_all_users():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Получаем всех пользователей
    cursor.execute("""
    SELECT name, job, city
    FROM users
    ORDER BY id
    """)

    # Получаем все записи
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список пользователей
    users = []

    # Преобразуем строки SQLite в словари
    for row in rows:

        user = {
            "name": row[0],
            "job": row[1],
            "city": row[2]
        }

        users.append(user)

    # Возвращаем список
    return users

# ==================================================
#             ПОЛУЧИТЬ УНИКАЛЬНЫЕ ПРОФЕССИИ
# ==================================================

def get_unique_jobs():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Получаем уникальные профессии
    cursor.execute("""
    SELECT DISTINCT job
    FROM users
    ORDER BY job
    """)

    # Получаем результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Превращаем кортежи в обычный список
    jobs = []

    for row in rows:

        jobs.append(row[0])

    return jobs

# ==================================================
#               ПОЛУЧИТЬ УНИКАЛЬНЫЕ ГОРОДА
# ==================================================

def get_unique_cities():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Получаем уникальные города
    cursor.execute("""
    SELECT DISTINCT city
    FROM users
    ORDER BY city
    """)

    # Получаем результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список городов
    cities = []

    for row in rows:

        cities.append(row[0])

    return cities

# ==================================================
#              ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ
# ==================================================

def add_user(name, job, city):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Добавляем пользователя
    cursor.execute("""
    INSERT INTO users (name, job, city)
    VALUES (?, ?, ?)
    """, (name, job, city))

    # Сохраняем изменения
    connection.commit()

    # Закрываем соединение
    connection.close()