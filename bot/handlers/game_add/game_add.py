from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import random
from datetime import datetime

N_SECONDS = 3

def register_handlers(dp: Dispatcher):
    global initial_state
    dp.register_message_handler(cmd_info_mul, commands="info_add", state='*')
    dp.register_message_handler(cmd_game_start, commands="add", state='*')
    dp.register_message_handler(cmd_game_mul, state=GameAddStates.game_in_progress)

async def cmd_info_mul(message: types.Message):
    await message.answer(f'Детский сад, ей богу. Проверим как ты складываешь.')
    await message.answer(f'У тебя будет {N_SECONDS} секунды на ответ. Я бы еще меньше сделала, тут и решать нечего, но вот так видимо решили сверху.')
    await message.answer(f'Ответишь неверно - ставлю два. Замешкаешься - позор тебе - ставлю два.')
    await message.answer(f'Напиши /add когда будешь готов. Захочешь сбежать - пиши /cancel')

async def cmd_game_start(message: types.Message, state: FSMContext):
    await state.finish()
    await state.set_state(GameAddStates.game_in_progress.state)
    q, a = gen_question()

    await state.update_data(expected_answer=a)
    await state.update_data(last_answ_timestep=datetime.now())

    await message.answer(q)

async def cmd_game_mul(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Что говоришь-то такое? Ответ - ЧИСЛО! Сколько раз повторять?')
        return
    
    u_data = await state.get_data()

    time_elapsed = abs((u_data['last_answ_timestep'] - datetime.now()).total_seconds())

    if time_elapsed > N_SECONDS:
        await message.answer('Долго думаешь! Садись, два.')
        await state.finish()
        return

    players_answ = int(message.text)
    expected_answ = u_data['expected_answer']

    if players_answ == expected_answ:
        q, a = gen_question()
        await state.update_data(expected_answer=a)
        await state.update_data(last_answ_timestep=datetime.now())
        await message.answer(q)
    else:
        await message.answer('Приплыли... Ты если не выучил, то зачем пришел? Выучишь - тогда приходи.')
        await state.finish()

class GameAddStates(StatesGroup):
    game_in_progress = State()

def gen_question():
    """Generates tuple (question, answer)"""
    x, y = random.randint(1, 9), random.randint(1, 9)
    question = f'{x} + {y}'
    answer = x+y
    return question, answer