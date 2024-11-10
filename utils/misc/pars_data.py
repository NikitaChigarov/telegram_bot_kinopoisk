from typing import List, TypeVar, Dict


T = TypeVar("T")


def get_string(data: List) -> str:
    """Раскрывает список словарей и возвращает строку"""
    count = len(data)
    if count >= 1:
        genres_string = ""
        for data_list in data:
            genres_string += " {},".format(data_list['name'])
        return genres_string[:-1]  # вернет срез стоки без последней запятой
    else:
        return "Не определен"


def get_data_list(model: T) -> List[Dict]:
    """Формирует модель ответа (список словарей) для вывода информации в телеграмм"""
    answer_list = list()
    for item in model:
        model_dict = dict()
        id_film = item.id_film
        poster = item.poster
        description = item.description
        model_dict["id_film"] = id_film
        model_dict["poster"] = poster
        model_dict["description"] = description
        answer_list.append(model_dict)
    return answer_list
