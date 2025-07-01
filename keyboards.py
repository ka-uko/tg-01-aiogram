from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_url = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url='https://dzen.ru/news')],
   [InlineKeyboardButton(text="Музыка", url='https://music.yandex.ru/?tss=')],
   [InlineKeyboardButton(text="Видео", url='https://dzen.ru/video')]
])
inline_keyboard_more = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data='more')]
])

inline_keyboard_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data='option_1')],
    [InlineKeyboardButton(text="Опция 2", callback_data='option_2')],
])

# test = ["кнопка 1","кнопка 2","кнопка 3","кнопка 4"]
# async def test_keyboard():
#    keyboard = InlineKeyboardBuilder()
#    for key in test:
#       keyboard.add(InlineKeyboardButton(text=key, url = 'https://dzen.ru/search?query=gjnfqyfz%20vjkybz&sid=1804206874161&type_filter=video%2Cshort'))
#    return keyboard.adjust(2).as_markup()

# async def test_keyboard():
#    keyboard = ReplyKeyboardBuilder()
#    for key in test:
#       keyboard.add(KeyboardButton(text=key))
#    return keyboard.adjust(2).as_markup()
