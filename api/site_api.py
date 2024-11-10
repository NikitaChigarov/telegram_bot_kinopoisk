from datetime import datetime
from os.path import basename
from typing import List, Dict

import requests
from telebot.apihelper import ApiTelegramException

from config_data import config
from utils.misc.pars_data import get_string


def _search(url, params, success=200) -> List[Dict]:
    """
    Принимает ссылку и параметры поиска, и обращается к api Кинопоиска,
    возвращает список словарей с информацией о фильмах/сериалах
    """
    answer_list = []
    answer_fall = [{"poster": "screenshot_from_telegram/no_poster.png",
                    "description": "Попробовал найти что-то, но так и не искал."}]
    url = url
    params_query = params

    headers = {
        "accept": "application/json",
        "X-API-KEY": config.API_KEY
    }
    try:
        response = requests.get(url, params=params_query, headers=headers, timeout=5)

        count_answer = len(response.json()["docs"])
        status_code = response.status_code

        if status_code == success:
            for index in range(count_answer):
                model_dict = {}
                id_film = response.json()["docs"][index].get("id")
                name = response.json()["docs"][index].get("name")
                description = response.json()["docs"][index].get("description")
                kp_rating, imdb_rating = (response.json()["docs"][index]["rating"].get("kp"),
                                          response.json()["docs"][index]["rating"].get("imdb"))
                year = response.json()["docs"][index].get("year")
                list_genres = response.json()["docs"][index].get("genres")
                genres = get_string(list_genres)
                age_rating = response.json()["docs"][index].get("ageRating")
                poster = response.json()["docs"][index]["poster"].get("url") if not None \
                    else "screenshot_from_telegram/no_poster.png"
                full_desc = (
                    f'📽Название: {name} \n🎯Жанр:{genres} \n💯Кинопоиск: {kp_rating} \t🗽IMDB: {imdb_rating} '
                    f'\n📆Год выпуска: {year} \n👶Возрастной рейтинг: {age_rating}+ \n\n🎬Описание:\n{description}')
                model_dict["id_film"] = id_film
                model_dict["poster"] = poster
                model_dict["description"] = full_desc
                answer_list.append(model_dict)
            return answer_list
    except ApiTelegramException as exc:
        print(
            f"Попытка запроса к API вызвало исключение {type(exc)} - {exc}\nВремя - {datetime.now()}. "
            f"Место - {basename(__file__)}")
        return answer_fall


def _by_custom_params(type_search: str, rating: str, genre_name: str, func=_search) -> List[Dict]:
    """Передаст параметры кастомного поиска в функцию поиска _search"""
    page_count = 10
    url = "https://api.kinopoisk.dev/v1.4/movie"
    params_query = {"limit": page_count, "isSeries": type_search, "rating.kp": rating, "genres.name": genre_name}
    response = func(url, params_query)
    return response


def _by_title_params(title: str, func=_search) -> List[Dict]:
    """Передаст параметры поиска по названию в функцию поиска _search"""
    page_count = 5
    url = "https://api.kinopoisk.dev/v1.4/movie/search"
    params_query = {"limit": page_count, "query": title}
    response = func(url, params_query)
    return response


class ApiInterface:
    """
    Реализация интерфейса обращения к API кинопоиска.
    Поиск по названию - title_response
    Поиск по заданным пользователем параметрам - custom_response
    """

    @staticmethod
    def title_response():
        """Вызовет функцию поиска по названию"""
        return _by_title_params

    @staticmethod
    def custom_response():
        """Вызовет функцию поиска по заданным параметрам"""
        return _by_custom_params
