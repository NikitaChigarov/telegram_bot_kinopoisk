from datetime import datetime
from os.path import basename

from peewee import IntegrityError
from telebot.types import CallbackQuery, Message

from database.model_favorite import FavoriteUser
from keyboards.inline.pagination import favorite_pagination
from loader import bot, write_db, read_db, delete_db
from utils.misc.pars_data import get_data_list


@bot.message_handler(commands=['favorites'])
def my_favorites(message: Message) -> None:
    """Вывод списка фильмов/сериалов сохраненных в избранное"""
    instance = read_db(FavoriteUser, message.from_user.id)
    bot.delete_message(message.chat.id, message.message_id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["favorite_movie"] = get_data_list(instance)
        favorite_pagination(message, data["favorite_movie"])


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'favorite')
def added_favorites(call: CallbackQuery) -> None:
    """Добавление фильма/сериала в избранное"""
    text_exception = ("Во время работы функции 'added_favorites' было вызвано исключение {} - {}\n"
                      "Время - {}. Место - {}\n")
    try:
        index = int(call.data.split('#')[1]) - 1
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data_model = {"user_id": call.from_user.id,
                          "id_film": data["movie_info"][index]["id_film"],
                          "poster": data["movie_info"][index]["poster"],
                          "description": data["movie_info"][index]["description"]}
            write_db(FavoriteUser, data_model)
            bot.send_message(call.from_user.id, "Добавлено в избранное.")
    except IntegrityError:
        bot.send_message(call.from_user.id, "Невозможно добавить, уже сохранен ранее.")
    except BaseException as exc:
        print(text_exception.format(type(exc), exc, datetime.now(), basename(__file__)))
        bot.send_message(call.from_user.id, "Упс, что-то пошло не так во время добавления в избранное.")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == "delete")
def remove_from_favorites(call: CallbackQuery) -> None:
    """Удаляет фильм/сериал из избранного"""
    text_exception = ("Во время работы функции 'remove_from_favorites' было вызвано исключение {} - {}\n"
                      "Время - {}. Место - {}\n")
    try:
        index = int(call.data.split('#')[1]) - 1
        bot.delete_message(call.message.chat.id, call.message.message_id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            id_film = data["favorite_movie"][index]["id_film"]
            delete_db(FavoriteUser, id_film)
            del data["favorite_movie"][index]
            favorite_pagination(call.message, data["favorite_movie"])
    except BaseException as exc:
        print(text_exception.format(type(exc), exc, datetime.now(), basename(__file__)))
        bot.send_message(call.from_user.id, "Упс, что-то пошло не так при удаление из избранного.")
