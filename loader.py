from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data import config
from utils.misc.CRUD import CRUDInterface

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)

crud = CRUDInterface()
write_db = crud.create()
read_db = crud.retrieve()
delete_db = crud.delete()
