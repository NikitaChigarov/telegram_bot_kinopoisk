from telebot.custom_filters import StateFilter  # Добавление поддержки состояний бота

import handlers  # noqa
from database.model_favorite import create_model_database
from loader import bot
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    create_model_database()
    bot.add_custom_filter(StateFilter(bot))  # включение поддержки состояний
    set_default_commands(bot)
    bot.infinity_polling()
