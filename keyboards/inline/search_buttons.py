from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def selection_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора типа поиска"""
    by_title = InlineKeyboardButton(text="⌨️📽 Поиск по названию", callback_data="title")
    by_custom = InlineKeyboardButton(text="🎬👈 Установить параметры поиска", callback_data="custom")
    keyboard = InlineKeyboardMarkup(row_width=1).add(by_title, by_custom)
    return keyboard


def favorites() -> InlineKeyboardMarkup:
    """Кнопка - избранное"""
    favorite = InlineKeyboardButton(text="🍿Добавить в избранное", callback_data="favorite")
    markup = InlineKeyboardMarkup().add(favorite)
    return markup


def types_movie() -> InlineKeyboardMarkup:
    """Клавиатура выбора критериев поиска фильм/сериал"""
    answer_no = InlineKeyboardButton(text="Не важно", callback_data="no_type")
    markup = InlineKeyboardMarkup().add(answer_no, row_width=2)
    film = InlineKeyboardButton(text="Фильм", callback_data="false")
    ser = InlineKeyboardButton(text="Сериал", callback_data="true")
    markup.add(film, ser, row_width=2)
    return markup


def rating() -> InlineKeyboardMarkup:
    """Клавиатура установки рейтинга фильма/сериала для поиска"""
    answer_no = InlineKeyboardButton(text="Не важно", callback_data="no_rating")
    markup = InlineKeyboardMarkup().add(answer_no, row_width=1)
    four = InlineKeyboardButton(text="4", callback_data="4")
    five = InlineKeyboardButton(text="5", callback_data="5")
    six = InlineKeyboardButton(text="6", callback_data="6")
    seven = InlineKeyboardButton(text="7", callback_data="7")
    eight = InlineKeyboardButton(text="8", callback_data="8")
    nine = InlineKeyboardButton(text="9", callback_data="9")
    markup.add(four, five, six, seven, eight, nine, row_width=3)
    return markup


def genre() -> InlineKeyboardMarkup:
    """Клавиатура установки жанра для поиска фильма/сериала"""
    answer_no = InlineKeyboardButton(text="Не важно", callback_data="no_genre")
    anime = InlineKeyboardButton(text="Аниме", callback_data="аниме")
    biography = InlineKeyboardButton(text="Биография", callback_data="биография")
    action_movie = InlineKeyboardButton(text="Боевик", callback_data="боевик")
    drama = InlineKeyboardButton(text="Драма", callback_data="драма")
    detective = InlineKeyboardButton(text="Детектив", callback_data="детектив")
    documentary = InlineKeyboardButton(text="Документальный", callback_data="документальный")
    comedy = InlineKeyboardButton(text="Комедия", callback_data="комедия")
    melodrama = InlineKeyboardButton(text="Мелодрама", callback_data="мелодрама")
    thriller = InlineKeyboardButton(text="Триллер", callback_data="триллер")
    fantastic = InlineKeyboardButton(text="Фантастика", callback_data="фантастика")
    horror = InlineKeyboardButton(text="Хоррор", callback_data="ужасы")
    markup = InlineKeyboardMarkup().add(answer_no, row_width=1)
    markup.add(anime, biography, action_movie, drama, detective, documentary, comedy, melodrama, thriller, fantastic,
               horror, row_width=2)
    return markup
