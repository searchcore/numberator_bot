from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from ...database.phrases.main import get_phrase

import random
from datetime import datetime

N_SECONDS = 3
N_QUESTIONS = 20

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_info_mul, commands="info_mul", state='*')
    dp.register_message_handler(cmd_game_start, commands="mul", state='*')
    dp.register_message_handler(cmd_game_mul, state=GameMulStates.game_in_progress)

async def cmd_info_mul(message: types.Message):
    for phrase in get_phrase('mul__info_msg'):
            await message.answer(phrase)

async def cmd_game_start(message: types.Message, state: FSMContext):
    await state.finish()
    await state.set_state(GameMulStates.game_in_progress.state)
    q, a = gen_question()

    await state.update_data(q_number=1)
    await state.update_data(expected_answer=a)
    await state.update_data(last_answ_timestep=datetime.now())

    await message.answer(q)

async def cmd_game_mul(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        for phrase in get_phrase('misc__nan'):
            await message.answer(phrase)
        return
    
    u_data = await state.get_data()

    time_elapsed = abs((u_data['last_answ_timestep'] - datetime.now()).total_seconds())

    if time_elapsed > N_SECONDS:
        for phrase in get_phrase('misc__time_out'):
            await message.answer(phrase)
        await state.finish()
        return

    players_answ = int(message.text)
    expected_answ = u_data['expected_answer']

    if players_answ == expected_answ:

        await state.update_data(q_number=u_data['q_number'] + 1)
        if u_data['q_number'] >= N_QUESTIONS:
            for phrase in get_phrase('misc__game_end'):
                await message.answer(phrase)
            await state.finish()
            return

        q, a = gen_question()
        await state.update_data(expected_answer=a)
        await state.update_data(last_answ_timestep=datetime.now())
        await message.answer(q)
    else:
        for phrase in get_phrase('misc__wrong_answ'):
            await message.answer(phrase)
        await state.finish()

class GameMulStates(StatesGroup):
    game_in_progress = State()

def gen_question():
    """Generates tuple (question, answer)"""
    x, y = random.randint(2, 9), random.randint(2, 9)
    question = f'{x} ∙ {y}'
    answer = x*y
    return question, answer