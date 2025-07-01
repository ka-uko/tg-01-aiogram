import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, WEATHER_API_KEY
import sqlite3
import aiohttp
import logging  #Для удобства здесь можно также использовать логирование, что, по сути, является ведением журнала событий. Это полезно для записи сообщений, событий или информации о работе программы. Для этого импортируем библиотеку Logging

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO) # прописываем название модуля: basicConfig с указанием в скобках уровня логирования. Уровень info просто дает информацию о ходе выполнения работы программы

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
	CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	city TEXT NOT NULL)
	''')
    conn.commit()
    conn.close()

init_db()

# прописываем команды
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name) #Это состояние указывает программе, что следующим шагом в диалоге будет ожидание ответа от пользователя. Мы отправили запрос на получение имени и программа ждет ответ.

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age) #ожидание ответа от пользователя

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)#ожидание ответа от пользователя

@dp.message(Form.city)
async def city(message: Message, state:FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data() #возвращает словарь с данными состояния. Эта строчка сохраняет все данные, которые были сохранены в контексте состояния, и из этого создает словарь:

    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users (name, age, city) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()
    #Теперь записанную в бд информацию нужно использовать для того, чтобы передавать сведения о погоде.
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={WEATHER_API_KEY}&units=metric") as response:
            if response.status == 200:
                weather_data = await response.json()
                main = weather_data['main']
                weather = weather_data['weather'][0]

                temperature = main['temp']
                humidity = main['humidity']
                description = weather['description']

                weather_report = (f"Город - {user_data['city']}\n"
                                  f"Температура - {temperature}\n"
                                  f"Влажность воздуха - {humidity}\n"
                                  f"Описание погоды - {description}")
                await message.answer(weather_report)
            else:
                await message.answer("Не удалось получить данные о погоде")

    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
