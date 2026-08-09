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
