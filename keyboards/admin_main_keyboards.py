from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import logging


def keyboards_start_admin():
    logging.info("keyboards_start_admin")
    button_1 = KeyboardButton(text='Количество участников')
    button_3 = KeyboardButton(text='Получить список участников')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_3],],
        resize_keyboard=True
    )
    return keyboard
