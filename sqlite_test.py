import sqlite3

# ==================================================
# Подключаемся к базе данных
# ==================================================

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# ==================================================
# Показываем всех пользователей
# ==================================================

cursor.execute("""
SELECT *
FROM users
""")

users = cursor.fetchall()

print("===== ВСЕ ПОЛЬЗОВАТЕЛИ =====")

for user in users:
    print(user)

# ==================================================
# Количество пользователей
# ==================================================

cursor.execute("""
SELECT COUNT(*)
FROM users
""")

count = cursor.fetchone()

print("\n===== ОБЩЕЕ КОЛИЧЕСТВО =====")

print(f"Всего пользователей: {count[0]}")

# ==================================================
# Статистика по профессиям
# ==================================================

cursor.execute("""
SELECT job, COUNT(*)
FROM users
GROUP BY job
""")

jobs = cursor.fetchall()

print("\n===== ПРОФЕССИИ =====")

for job in jobs:
    for job in jobs:
        print(f"{job[0]}: {job[1]}")

# ==================================================
# Статистика по городам
# ==================================================

cursor.execute("""
SELECT city, COUNT(*)
FROM users
GROUP BY city
""")

cities = cursor.fetchall()

print("\n===== ГОРОДА =====")

for city in cities:
    for city in cities:
        print(f"{city[0]}: {city[1]}")
# ==================================================
# Закрываем соединение
# ==================================================

connection.close()

print("\n✅ Работа завершена!")