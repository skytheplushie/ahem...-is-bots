from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '7680989311:AAEIRSxJCLJkGTza1H1Kci3e_m2LVRYwo3A'
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


ikb = InlineKeyboardMarkup()
ilbutton1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
ilbutton2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
ikb.add(ilbutton1)
ikb.add(ilbutton2)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.reply("Выберите опцию:", reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Расчётные формулы, которыми я пользуюсь: '
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Информация о боте!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(call=['calories'])
async def set_age(call):
    await call.message.answer('Скажи свой возраст')
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
