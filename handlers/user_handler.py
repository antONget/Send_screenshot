from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, or_f, and_f, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filter.admin_filter import IsSuperAdmin
from config_data.config import Config, load_config
from database import requests as rq
from keyboards import user_keyboards as kb

import logging
router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    screenshot = State()


@router.message(or_f(and_f(CommandStart(), ~IsSuperAdmin()),
                     and_f(IsSuperAdmin(), F.text == '/user')))
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    """
    Пользовательский режим запускается если, пользователь ввел команду /start
     или если администратор ввел команду /user
    1. Добавляем пользователя в БД если его еще нет в ней
    :param message:
    :param state:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.update_data(state=None)
    await rq.add_user(tg_id=message.chat.id,
                      data={"tg_id": message.chat.id, "username": message.from_user.username})
    await message.answer(text=f'Приветственное сообщение. Описание того для чего нужен этот бот. Как им пользоваться')
    await message.answer(text=f'Для участи я в розыгрыше пришлите скриншот "присейва". Требования к скриншоту.\n\n'
                              f'В подписи к скриншоту укажите адрес вашей электронной почты')
    await state.set_state(User.screenshot)


@router.message(F.photo, StateFilter(User.screenshot))
async def get_screenshot(message: Message, bot: Bot) -> None:
    """
    Получаем screenshot "пресейва"
    :param message:
    :param bot:
    :return:
    """
    logging.info(f'get_screenshot: {message.chat.id}')
    screenshot = message.photo[-1].file_id
    email = message.caption
    await message.answer(text=f'Данные отправлены на модерацию. Ожидайте...')
    await rq.update_user(tg_id=message.chat.id,
                         screenshot=screenshot,
                         email=email)
    try:
        for admin in config.tg_bot.admin_ids.split(','):
            await bot.send_photo(chat_id=admin,
                                 photo=screenshot,
                                 caption=f'Пользователь {message.chat.id} отправил screenshot "пресейва":\n\n'
                                         f'<b>Username_TG:</b> {message.from_user.username}\n'
                                         f'<b>Email:</b> {email}\n\n'
                                         f'Подтвердите или отклоните!',
                                 reply_markup=kb.keyboard_confirm_screenshot(tg_id=message.chat.id))
    except:
        pass



@router.message(F.text == 'Задать вопрос')
async def process_question(message: Message) -> None:
    """
    Обработка обратной связи
    :param message:
    :return:
    """
    logging.info(f'process_question: {message.chat.id}')
    await message.answer(text='Если у вас возникли вопросы по работе бота или у вас есть предложения,'
                              ' то можете написать @legeau')
