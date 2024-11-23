from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Calories'])
async def set_age(message):
    await message.answer('Скажи свой возраст')
    await UserState.age.set()


@dp.message_handler(state=[UserState.age])
async def set_growth(message, state):
    await message.answer('Скажи свой рост')
    await message.text.update_data(set_age=message.text)
    await UserState.growth.set()


@dp.message_handler(state=[UserState.growth])
async def set_weight(message, state):
    await message.answer('Скажи свой вес')
    await message.text.update_data(set_growth=message.text)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await message.text.update_data(set_weight=message.text)
    data = await state.get_data()
    await message.answer(f'ваши возраст, рост и вес {data["age"]}, {data["growth"]} и {data["weight"]}. Ведётся подсчёт'
                         f', пожалуйста, подождите')
    await message.answer(f'результаты подсчёта: {10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5}')
    await state.finish()


# @dp.message_handler(text=['Привет'])
# async def all_messages(message):
#    print('Введите команду /start, чтобы начать общение.')
#    await message.answer('Введите команду /start, чтобы начать общение.')


# @dp.message_handler(commands=['start'])
# async def start(message):
#    print('Привет! Я бот помогающий твоему здоровью.')
#    await message.answer('Привет! Я бот помогающий твоему здоровью.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
