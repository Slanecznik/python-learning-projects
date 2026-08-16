# ==================================================
#                 ИМПОРТЫ
# ==================================================

import sqlite3


# ==================================================
#             ПОЛУЧИТЬ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
# ==================================================

def get_all_users():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor для выполнения SQL-запросов
    cursor = connection.cursor()

    # Получаем всех пользователей
    cursor.execute("""
        SELECT name, job, city
        FROM users
        ORDER BY id
    """)

    # Получаем все найденные строки
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список пользователей
    users = []

    # Преобразуем строки SQLite в словари Python
    for row in rows:

        user = {
            "name": row[0],
            "job": row[1],
            "city": row[2]
        }

        users.append(user)

    # Возвращаем список пользователей
    return users


# ==================================================
#              ПОЛУЧИТЬ ПЕРВОГО ПОЛЬЗОВАТЕЛЯ
# ==================================================

def get_first_user():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Получаем первого пользователя
    cursor.execute("""
        SELECT name, job, city
        FROM users
        ORDER BY id
        LIMIT 1
    """)

    # Получаем одну строку
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

    # Если база пустая
    return None


# ==================================================
#              ОБЩЕЕ КОЛИЧЕСТВО ПОЛЬЗОВАТЕЛЕЙ
# ==================================================

def get_total_users():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Считаем все записи
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)

    # Получаем результат
    result = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    # Возвращаем количество пользователей
    return result[0]


# ==================================================
#             УНИКАЛЬНЫЕ ПРОФЕССИИ
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

    # Получаем все результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список профессий
    jobs = []

    # Преобразуем результаты в обычный список
    for row in rows:

        jobs.append(row[0])

    # Возвращаем список профессий
    return jobs


# ==================================================
#               УНИКАЛЬНЫЕ ГОРОДА
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

    # Получаем все результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список городов
    cities = []

    # Преобразуем результаты в обычный список
    for row in rows:

        cities.append(row[0])

    # Возвращаем список городов
    return cities


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

    # Возвращаем количество
    return result[0]


# ==================================================
#            КОЛИЧЕСТВО УНИКАЛЬНЫХ ГОРОДОВ
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

    # Возвращаем количество
    return result[0]


# ==================================================
#          СТАТИСТИКА ПО ПРОФЕССИЯМ
# ==================================================

def count_users_by_job():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Группируем пользователей по профессии
    cursor.execute("""
        SELECT job, COUNT(*)
        FROM users
        GROUP BY job
        ORDER BY job
    """)

    # Получаем результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём словарь статистики
    statistics = {}

    # Записываем профессию и количество пользователей
    for row in rows:

        statistics[row[0]] = row[1]

    # Возвращаем статистику
    return statistics


# ==================================================
#             СТАТИСТИКА ПО ГОРОДАМ
# ==================================================

def count_users_by_city():

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Группируем пользователей по городу
    cursor.execute("""
        SELECT city, COUNT(*)
        FROM users
        GROUP BY city
        ORDER BY city
    """)

    # Получаем результаты
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём словарь статистики
    statistics = {}

    # Записываем город и количество пользователей
    for row in rows:

        statistics[row[0]] = row[1]

    # Возвращаем статистику
    return statistics


# ==================================================
#              ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ
# ==================================================

def add_user(name, job, city):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Добавляем нового пользователя
    cursor.execute("""
        INSERT INTO users (name, job, city)
        VALUES (?, ?, ?)
    """, (name, job, city))

    # Сохраняем изменения
    connection.commit()

    # Закрываем соединение
    connection.close()


# ==================================================
#          ИЗМЕНИТЬ ПРОФЕССИЮ ПОЛЬЗОВАТЕЛЯ
# ==================================================

def update_user_job(name, new_job):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Изменяем профессию пользователя
    cursor.execute("""
        UPDATE users
        SET job = ?
        WHERE name = ?
    """, (new_job, name))

    # Сохраняем изменения
    connection.commit()

    # Запоминаем количество изменённых строк
    updated_rows = cursor.rowcount

    # Закрываем соединение
    connection.close()

    # Возвращаем количество изменённых записей
    return updated_rows


# ==================================================
#              УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ
# ==================================================

def delete_user(name):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Удаляем пользователя
    cursor.execute("""
        DELETE FROM users
        WHERE name = ?
    """, (name,))

    # Сохраняем изменения
    connection.commit()

    # Получаем количество удалённых строк
    deleted_rows = cursor.rowcount

    # Закрываем соединение
    connection.close()

    # Возвращаем количество удалённых записей
    return deleted_rows

# ==================================================
#              ПОИСК ПО ИМЕНИ
# ==================================================

def find_user_by_name(name):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Ищем пользователя по имени
    cursor.execute("""
        SELECT name, job, city
        FROM users
        WHERE LOWER(name) = LOWER(?)
        LIMIT 1
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

    # Если пользователь не найден
    return None


# ==================================================
#              ПОИСК ПО ГОРОДУ
# ==================================================

def find_users_by_city(city):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Ищем всех пользователей из города
    cursor.execute("""
        SELECT name, job, city
        FROM users
        WHERE LOWER(city) = LOWER(?)
        ORDER BY id
    """, (city,))

    # Получаем все записи
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список пользователей
    users = []

    # Преобразуем строки в словари
    for row in rows:

        users.append({
            "name": row[0],
            "job": row[1],
            "city": row[2]
        })

    # Возвращаем список
    return users


# ==================================================
#             ПОИСК ПО ПРОФЕССИИ
# ==================================================

def find_users_by_job(job):

    # Подключаемся к базе данных
    connection = sqlite3.connect("database.db")

    # Создаём cursor
    cursor = connection.cursor()

    # Ищем всех пользователей с этой профессией
    cursor.execute("""
        SELECT name, job, city
        FROM users
        WHERE LOWER(job) = LOWER(?)
        ORDER BY id
    """, (job,))

    # Получаем все записи
    rows = cursor.fetchall()

    # Закрываем соединение
    connection.close()

    # Создаём список пользователей
    users = []

    # Преобразуем строки в словари
    for row in rows:

        users.append({
            "name": row[0],
            "job": row[1],
            "city": row[2]
        })

    # Возвращаем список
    return users