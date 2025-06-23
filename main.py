import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY
import random
import aiohttp

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://i.pinimg.com/736x/4f/ec/27/4fec278fca401b21166b6d3389a271bc.jpg',
        'https://i.pinimg.com/736x/87/65/95/8765951856fd5e8b415b0d8620af2034.jpg',
        'https://i.pinimg.com/originals/59/d0/1f/59d01f805d4971d4694164d5dec46616.png'
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Лови слоника!')


@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Классная фотка!', 'Вау! присылай еще фото', 'Отличный выбор фото!']
    await message.answer(random.choice(responses))


@dp.message(F.text == 'Что такое зерокодинг?')
async def aitext(message: Message):
    await message.answer('Зерокодинг (zero-code, no-code) — это метод создания сайтов и приложений без кода')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет кое-что:\n/start\n/help\n/photo\n/weather')


@dp.message(Command('weather'))
async def get_weather(message: Message):
    city = 'Pyatigorsk'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                await message.answer(f'Погода в Пятигорске: {temp}°C, {description}')
            else:
                await message.answer('Не удалось получить данные о погоде 😔')

@dp.message(CommandStart)
async def start(message: Message):
    await message.answer('Привет! Я бот! Напиши /weather, чтобы узнать погоду в Пятигорске.')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
