import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import random
import aiohttp
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

from config import TOKEN, WEATHER_API_KEY
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=kb.inline_keyboard_url)

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer("Нажми кнопку ниже:", reply_markup=kb.inline_keyboard_more)

@dp.callback_query(F.data == 'more')
async def show_options(callback: CallbackQuery):
    await callback.message.edit_text("Выбери опцию:", reply_markup=kb.inline_keyboard_options)
    await callback.answer()


@dp.callback_query(F.data.in_({'option_1', 'option_2'}))
async def option_selected(callback: CallbackQuery):
    if callback.data == "option_1":
        option = "Опция 1"
    else:
        option = "Опция 2"
    await callback.message.answer(f"Вы выбрали: {option}")
    await callback.answer()


@dp.message(F.text == "Привет")
async def hello (message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')

@dp.message(F.text == "Пока")
async def bye(message: Message):
    await message.answer(f'До свидания, {message.from_user.first_name}!')


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("audio_voice.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("tart.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://i.pinimg.com/736x/4f/ec/27/4fec278fca401b21166b6d3389a271bc.jpg',
        'https://i.pinimg.com/736x/87/65/95/8765951856fd5e8b415b0d8620af2034.jpg',
        'https://i.pinimg.com/originals/59/d0/1f/59d01f805d4971d4694164d5dec46616.png'
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Лови слоника!')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет кое-что:\n/start\n/help\n/photo\n/weather\n&текст — перевод и озвучка')

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


# Перевод &текст
@dp.message(F.text.startswith('&'))
async def translate_and_speak(message: Message):
    text_ru = message.text[1:].strip()

    if not text_ru:
        await message.answer("❗️После `&` ничего нет для перевода.")
        return

    try:
        text_en = GoogleTranslator(source='ru', target='en').translate(text_ru)
    except Exception:
        await message.answer("Ошибка при переводе 😔")
        return

    try:
        tts = gTTS(text_en, lang='en')
        filename = f"audio_{message.from_user.id}.mp3"
        tts.save(filename)
    except Exception:
        await message.answer("Ошибка при озвучке 🎤")
        return

    await message.answer(f"Перевод: {text_en}")
    voice_file = FSInputFile(filename)
    await message.answer_voice(voice_file)
    os.remove(filename)

@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Классная фотка! Сохраняем!', 'Вау! присылай еще! Сохраняем', 'Отличный выбор фото! Сохраняем!']
    await message.answer(random.choice(responses))
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(F.text == 'Что такое зерокодинг?')
async def aitext(message: Message):
    await message.answer('Зерокодинг (zero-code, no-code) — это метод создания сайтов и приложений без кода')

@dp.message(CommandStart)
async def start(message: Message):
    await message.answer(f'Выберите кнопку', reply_markup= kb.main)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
