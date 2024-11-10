from typing import Dict, TypeVar

from peewee import ModelSelect

from database.model_favorite import db, BaseModel, FavoriteUser

T = TypeVar("T")


def _save_data(model: T, data: Dict) -> None:
    """Добавит данные в таблицу базы данных"""
    with db.atomic():
        model.create(
            user_id=data["user_id"],
            id_film=data["id_film"],
            poster=data["poster"],
            description=data["description"]
        )


def _show_data(model: T, user_id: int, *columns: BaseModel) -> ModelSelect:
    """Выведет информацию из базы данных по переданному пользователю (user_id)"""
    with db.atomic():
        response = model.select(*columns).where(FavoriteUser.user_id == user_id)

        return response


def _delete_data(model: T, id_film: int) -> None:
    """Удалит фильм (по id_film) из базы данных"""
    instance = model.get(FavoriteUser.id_film == id_film)
    instance.delete_instance()


class CRUDInterface:
    """Интерфейс работы с базой данных"""

    @staticmethod
    def create():
        """Вызовет функцию добавления в БД"""
        return _save_data

    @staticmethod
    def retrieve():
        """Вызовет функцию вывода информации из БД"""
        return _show_data

    @staticmethod
    def delete():
        """Вызовет функцию удаления из БД"""
        return _delete_data
