import sqlite3

# Подключаемся к базе данных
connection = sqlite3.connect("database.db")

# Создаём объект для выполнения SQL-команд
cursor = connection.cursor()

# Создаём таблицу users

cursor.execute("""
INSERT INTO users (name, job, city)
VALUES ('Владимир', 'Таксист', 'Лодзь')
""")

# Получаем всех пользователей
cursor.execute("""
SELECT * FROM users
""")

# Забираем все строки
users = cursor.fetchall()

# Выводим каждую запись
for user in users:
    print(user)


# Сохраняем изменения
connection.commit()

# Закрываем базу данных
connection.close()

print("✅ Пользователь успешно добавлен!")