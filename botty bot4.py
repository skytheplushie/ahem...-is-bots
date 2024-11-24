from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать каллории')
kb.add(button1)
kb.add(button2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Информация о боте!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Рассчитать каллории'])
async def set_age(message):
    await message.answer('Скажи свой возраст')
    await UserState.age.set()


@dp.message_handler(state=[UserState.age])
async def set_growth(message, state):
    await state.update_data(set_age=message.text)
    await message.answer('Скажи свой рост')
    await UserState.growth.set()


@dp.message_handler(state=[UserState.growth])
async def set_weight(message, state):
    await state.update_data(set_growth=message.text)
    await message.answer('Скажи свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(set_weight=message.text)
    data = await state.get_data()
    await message.answer(10 * int(data["set_weight"]) + 6.25 * int(data["set_growth"]) - 5 * int(data["set_age"]) + 5)
    await state.finish()


# @dp.message_handler(text=['Привет'])
# async def all_messages(message):
#    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
