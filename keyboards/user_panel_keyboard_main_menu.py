#Импорты
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton('/Режим_работы')
button2 = KeyboardButton('/Расположение')
button3 = KeyboardButton('/Врачи')
button4 = KeyboardButton('/Записаться')

kb_user = ReplyKeyboardMarkup(resize_keyboard=True)

kb_user.add(button1).add(button2).add(button3).insert(button4)