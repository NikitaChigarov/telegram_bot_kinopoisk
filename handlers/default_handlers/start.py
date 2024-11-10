from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Обработка команды start выведет приветственное сообщение из переменной text"""
    text = (
        f'Приветствую Вас, {message.from_user.full_name}👋.\nЯ бот (🤖) предоставляющий информацию по фильмам и сериалам '
        f'на основе данных "Кинопоиска". \n\nНажав кнопку в левом нижнем углу, '
        f'Вы увидите основные возможности данного чата 📱. \n↙️')
    bot.send_message(message.from_user.id, text)
    bot.delete_message(message.chat.id, message.message_id)
