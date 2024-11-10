from typing import List, Dict

from telebot.types import InlineKeyboardButton, Message
from telegram_bot_pagination import InlineKeyboardPaginator

from loader import bot


def search_pagination(message: Message, search_list: List[Dict], page=1) -> None:
    """Добавление кнопок пагинации к выводу информации поиска"""
    paginator = InlineKeyboardPaginator(len(search_list), current_page=page, data_pattern='search_page#{page}')
    paginator.add_before(InlineKeyboardButton('🍿Добавить в избранное', callback_data='favorite#{}'.format(page)))
    paginator.add_after(InlineKeyboardButton('🎬👈Перейти в поиск по своим параметрам', callback_data='custom'))
    bot.send_photo(message.chat.id,
                   photo=search_list[page - 1]["poster"],
                   caption=search_list[page - 1]["description"],
                   reply_markup=paginator.markup)


def favorite_pagination(message: Message, favorite_list: List[Dict], page=1) -> None:
    """Добавление кнопок пагинации к выводу информации по добавленным в избранное"""
    paginator = InlineKeyboardPaginator(len(favorite_list), current_page=page, data_pattern='favorite_page#{page}')
    paginator.add_before(
        InlineKeyboardButton(text="🗑️🎥Удалить из избранного", callback_data='delete#{}'.format(page)))
    paginator.add_after(InlineKeyboardButton('🎬👈 Перейти к поиску', callback_data='custom'))
    bot.send_photo(message.chat.id,
                   photo=favorite_list[page - 1]["poster"],
                   caption=favorite_list[page - 1]["description"],
                   reply_markup=paginator.markup)
