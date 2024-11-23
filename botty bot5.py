from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "7516083893:AAFIUKbjt4PGvyOgqKNqDfuD5gP97c0ecvM"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()


menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]
],
    resize_keyboard=True)

inline_choices = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
        ]
    ]
)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выбери опцию:', reply_markup=inline_choices)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('Расчётные формулы, которыми я пользуюсь: '
                              '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;')


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий {result}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=menu)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)