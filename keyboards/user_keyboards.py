from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboard_confirm_screenshot(tg_id: int):
    logging.info("keyboard_confirm_screenshot")
    button_1 = InlineKeyboardButton(text='Принять',  callback_data=f'confirm_yes_{tg_id}')
    button_2 = InlineKeyboardButton(text='Отклонить', callback_data=f'confirm_no_{tg_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2, button_1]], )
    return keyboard


def keyboard_get_more():
    logging.info("keyboard_get_more")
    button_1 = InlineKeyboardButton(text='Покажите еще 3',  callback_data=f'get_more')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
    return keyboard


def keyboard_get_more_event():
    logging.info("keyboard_get_more_event")
    button_1 = InlineKeyboardButton(text='Покажите еще 3',  callback_data=f'get_more_event')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
    return keyboard




def keyboard_full_text_1(yandex):
    logging.info("keyboard_full_text_1")
    button_1 = ''
    if validators.url(yandex):
        button_1 = InlineKeyboardButton(text='Яндекс Карты',  url=f'{yandex}')
    else:
        button_1 = InlineKeyboardButton(text='Яндекс Карты', callback_data=' ')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
    return keyboard