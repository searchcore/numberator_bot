import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .misc.env import get_token_from_env
from .misc.utils import config_read

from .handlers.games.mul import init_handlers as game_mul_init_handlers
from .handlers.games.add import init_handlers as game_add_init_handlers

from .handlers.common import init_handlers as common_init_handlers

from .database.models.user import init_users_db

token = get_token_from_env('NUMBERATOR_BOT')
bot = Bot(token=token)

dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

def main(cfg_path):

    cfg = config_read(cfg_path)

    init_users_db(cfg['RANKING'])
    common_init_handlers(dp)
    game_mul_init_handlers(dp, cfg['MUL'])
    game_add_init_handlers(dp, cfg['ADD'])

    executor.start_polling(dp, skip_updates=True)