from telebot.handler_backends import State, StatesGroup


class Search(StatesGroup):
    """Состояния пользователя для работы с ботом"""
    wait_choice = State()
    title_search = State()
    custom_search = State()
