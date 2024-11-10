from datetime import datetime
from os.path import basename

from telebot.types import CallbackQuery

from api.site_api import ApiInterface
from keyboards.inline.pagination import search_pagination, favorite_pagination
from keyboards.inline.search_buttons import *
from loader import bot
from states.state_bot.state_search import Search


@bot.callback_query_handler(func=lambda call: call.data == 'custom')
def response_custom(call: CallbackQuery) -> None:
    """Удалит клавиатуру и покажет критерии поиска"""
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.set_state(call.from_user.id, Search.custom_search, call.message.chat.id)
    bot.send_message(call.from_user.id, "Вы хотите подобрать фильм или сериал?", reply_markup=types_movie())


@bot.callback_query_handler(func=lambda call: call.data in ["no_type", "false", "true"])
def get_types(call: CallbackQuery) -> None:
    """Запрашивает и сохраняет (в состояние) тип поиска (фильм/сериал)"""
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.from_user.id, "При необходимости установите рейтинг для поиска", reply_markup=rating())

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["type"] = None if call.data == "no_type" else call.data


@bot.callback_query_handler(func=lambda call: call.data in ["no_rating", "4", "5", "6", "7", "8", "9"])
def get_rating(call: CallbackQuery) -> None:
    """Запрашивает и сохраняет (в состояние) рейтинг фильма/сериал"""
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.from_user.id, "Желаете выбрать жанр для поиска?", reply_markup=genre())

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["rating"] = None if call.data == "no_rating" else call.data


@bot.callback_query_handler(
    func=lambda call: call.data in ["no_genre", "аниме", "биография", "боевик", "драма", "детектив", "документальный",
                                    "комедия", "мелодрама", "триллер", "фантастика", "ужасы"])
def get_info_movie(call: CallbackQuery) -> None:
    """
    Запрашивает и сохраняет (в состояние) информацию о фильме/сериале,
    выводит результат поиска.
    """
    bot.set_state(call.from_user.id, Search.wait_choice, call.message.chat.id)
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.id)
    text_exception = ("Во время работы функции 'get_info_movie' было вызвано исключение {} - {}\n"
                      "Время - {}. Место - {}\n")
    try:
        custom = ApiInterface.custom_response()
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["genre"] = None if call.data == "no_genre" else call.data
            data["movie_info"] = custom(data["type"], data["rating"], data["genre"])
            search_pagination(call.message, data["movie_info"])
    except BaseException as exc:
        print(text_exception.format(type(exc), exc, datetime.now(), basename(__file__)))
        bot.send_message(call.message.chat.id, "Упс, что-то пошло не так.")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'search_page')
def get_page_search(call: CallbackQuery) -> None:
    """Получает текущую страницу пагинации, удаляет ее и возвращает запрошенную страницу (для изменяемого поиска)"""
    text_exception = ("Во время работы функции 'get_page_search' было вызвано исключение {} - {}\n"
                      "Время - {}. Место - {}\n")
    try:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            page = int(call.data.split('#')[1])
            bot.delete_message(call.message.chat.id, call.message.message_id)
            search_pagination(call.message, data["movie_info"], page)
    except BaseException as exc:
        print(text_exception.format(type(exc), exc, datetime.now(), basename(__file__)))
        bot.send_message(call.message.chat.id, "Упс, что-то пошло не так.")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'favorite_page')
def get_page_favorite(call: CallbackQuery) -> None:
    """Получает текущую страницу пагинации, удаляет ее и возвращает запрошенную страницу (для избранного)"""
    text_exception = ("Во время работы функции 'get_page_favorite' было вызвано исключение {} - {}\n"
                      "Время - {}. Место - {}\n")
    try:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            page = int(call.data.split('#')[1])
            bot.delete_message(call.message.chat.id, call.message.message_id)
            favorite_pagination(call.message, data["favorite_movie"], page)
    except BaseException as exc:
        print(text_exception.format(type(exc), exc, datetime.now(), basename(__file__)))
        bot.send_message(call.message.chat.id, "Упс, что-то пошло не так.")
