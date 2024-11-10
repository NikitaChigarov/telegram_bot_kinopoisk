from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """Обработчик, куда летят текстовые сообщения без указанного состояния"""
    bot.send_message(
        message.chat.id,
        'Пожалуйста, управляйте ботом через in-line клавиатуру.\n'
        f'Ваше сообщение: "{message.text}" не может быть распознано ботом.'
    )
