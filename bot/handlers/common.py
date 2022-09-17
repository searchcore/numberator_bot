from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from ..database.models.user import get_top_ranks
from ..database.phrases.main import get_phrase

def init_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_rank, commands="rank", state="*")

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    for phrase in get_phrase('common__start'):
            await message.answer(phrase)

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    for phrase in get_phrase('common__cancel'):
            await message.answer(phrase)

async def cmd_rank(message: types.Message, state: FSMContext):
    await state.finish()
    for phrase in get_phrase('common__rank'):
            await message.answer(phrase)

    ranks = get_top_ranks()

    ranks_info_str = ''
    for u in ranks:
        s = f'{u[0]} - {u[1]}\n'
        ranks_info_str = ranks_info_str + s

    if len(ranks_info_str) == 0:
        for phrase in get_phrase('common__rank_empty'):
            await message.answer(phrase)
    else:
        await message.answer(ranks_info_str)