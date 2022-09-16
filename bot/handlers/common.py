from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Явился? Давай, садись.')
    await message.answer('Та-а-ак... Ты что исправлять-то пришел?')
    await message.answer('/mul - тренажер таблицы умножения\n/add - тренажер сложения\nСначала ознакомьтесь с правилами:\n/info_название_режима\nПример:\n/info_mul')

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Эй! Ты куда собрался? Я щас родителям позво...\n*Вы хлопнули дверью и позорно сбежали*\n*Похоже, на следующем уроке Вам придется тяжко*')