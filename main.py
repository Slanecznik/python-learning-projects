# импортируем инструменты для Telegram-бота
from telegram.ext import (
    Application,
    CommandHandler
)


# -------- КОМАНДА /start --------
def start(update, context):

    # бот отправляет сообщение
    update.message.reply_text(
        "Привет, Владимир 😄 Я твой первый Telegram-бот!"
    )


# -------- КОМАНДА /help --------
def help_command(update, context):

    # бот отправляет список команд
    update.message.reply_text(
        "Команды:\n/start\n/help"
    )


# -------- TOKEN БОТА --------

# сюда вставляем TOKEN из BotFather
TOKEN = "8903619367:AAFVDIQIfC-rsw1FlolcIpBjUfI-qhK8WXY"


# -------- СОЗДАЁМ БОТА --------

# создаём приложение
app = Application.builder().token(TOKEN).build()


# если человек написал /start
# вызвать функцию start
app.add_handler(
    CommandHandler("start", start)
)


# если человек написал /help
# вызвать функцию help_command
app.add_handler(
    CommandHandler("help", help_command)
)


# -------- ЗАПУСК БОТА --------

# бот начинает работать
app.run_polling()