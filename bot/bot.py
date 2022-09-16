import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .misc.env import get_token_from_env

from .handlers.games.mul import register_handlers as game_mul_register_handlers
from .handlers.games.add import register_handlers as game_add_register_handlers

from .handlers.common import register_handlers as common_register_handlers

token = get_token_from_env('NUMBERATOR_BOT')
bot = Bot(token=token)

dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

def main():
    common_register_handlers(dp)
    game_mul_register_handlers(dp)
    game_add_register_handlers(dp)

    executor.start_polling(dp, skip_updates=True)