import sqlite3

# Подключаемся к базе данных
connection = sqlite3.connect("database.db")

print("База данных создана!")

# Закрываем соединение
connection.close()