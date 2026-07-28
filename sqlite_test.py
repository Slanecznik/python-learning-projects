import sqlite3

# ==================================================
# Подключаемся к базе данных
# ==================================================

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# ==================================================
# Добавляем пользователей
# ==================================================

cursor.execute("""
INSERT INTO users (name, job, city)
VALUES ('Владимир', 'Таксист', 'Лодзь')
""")

cursor.execute("""
INSERT INTO users (name, job, city)
VALUES ('Анна', 'Дизайнер', 'Варшава')
""")

cursor.execute("""
INSERT INTO users (name, job, city)
VALUES ('Иван', 'Python Developer', 'Краков')
""")

connection.commit()

# ==================================================
# Сортировка по имени
# ==================================================

cursor.execute("""
SELECT *
FROM users
ORDER BY name
""")

users = cursor.fetchall()

print("===== СОРТИРОВКА ПО ИМЕНИ =====")

for user in users:
    print(user)

# ==================================================
# Сортировка по профессии
# ==================================================

cursor.execute("""
SELECT *
FROM users
ORDER BY job
""")

users = cursor.fetchall()

print("\n===== СОРТИРОВКА ПО ПРОФЕССИИ =====")

for user in users:
    print(user)

# ==================================================
# Сортировка по ID (по убыванию)
# ==================================================

cursor.execute("""
SELECT *
FROM users
ORDER BY id DESC
""")

users = cursor.fetchall()

print("\n===== ПОСЛЕДНИЕ ДОБАВЛЕННЫЕ =====")

for user in users:
    print(user)

# ==================================================
# Закрываем соединение
# ==================================================

connection.close()

print("\n✅ Работа завершена!")