from datetime import datetime
from os.path import basename

from telebot.types import Message, CallbackQuery

from api.site_api import ApiInterface
from keyboards.inline.pagination import search_pagination
from keyboards.inline.search_buttons import selection_keyboard
from loader import bot
from states.state_bot.state_search import Search


@bot.message_handler(commands=['movie_search'])
def response_type_search(message: Message) -> None:
    """Выведет сообщение и клавиатуру выбора поиска"""
    bot.delete_message(message.chat.id, message.message_id)
    bot.set_state(message.from_user.id, Search.wait_choice, message.chat.id)
    bot.send_message(message.from_user.id, "Выберете тип поиска.", reply_markup=selection_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "title")
def title_search(call: CallbackQuery) -> None:
    """Удалит клавиатуру, предыдущее сообщение и запросит название фильма"""
    bot.set_state(call.from_user.id, Search.title_search, call.message.chat.id)
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Напишите название фильма")


@bot.message_handler(state=Search.title_search)
def reply_by_title(message: Message) -> None:
    """Выведет результат по введенному названию фильма и удалит предыдущее сообщение"""
    bot.edit_message_text(f'Результаты поиска: "{message.text}"', message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)
    text = "К сожалению, поиск по Вашему запросу не удался, пожалуйста, повторите попытку."
    text_exception = "Сообщение пользователя '{}' вызвало ошибку {} - {}\nВремя - {}. Место - {}\n"
    try:
        response_title = ApiInterface.title_response()
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["movie_info"] = response_title(message.text)
            search_pagination(message, data["movie_info"])
    except BaseException as exc:
        print(text_exception.format(message.text, type(exc), exc, datetime.now(), basename(__file__)))
        bot.send_message(message.chat.id, text)
