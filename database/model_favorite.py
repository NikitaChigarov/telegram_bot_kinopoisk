from peewee import SqliteDatabase, Model, IntegerField, TextField

db = SqliteDatabase("database/favorites.db")


class BaseModel(Model):
    """Базовая модель сохраняющая id пользователя"""
    user_id = IntegerField()

    class Meta:
        database = db


class FavoriteUser(BaseModel):
    """Модель сохранения избранного"""
    id_film = IntegerField(primary_key=True)
    poster = TextField(null=True)
    description = TextField()


def create_model_database():
    """Создание таблицы избранного в базе данных"""
    db.create_tables([FavoriteUser])
