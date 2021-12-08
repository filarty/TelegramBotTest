from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Button1 = KeyboardButton('💼 Ваш портфель в тинькофф')
Button2 = KeyboardButton('🏦 Установить API ключ')

keyboard = ReplyKeyboardMarkup().add(Button1, Button2)
