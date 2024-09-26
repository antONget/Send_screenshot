import time

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from config_data.config import Config, load_config
from keyboards.admin_main_keyboards import keyboards_start_admin
from filter.admin_filter import IsSuperAdmin
from database import requests as rq
from database.models import User
import asyncio
import logging

router = Router()

config: Config = load_config()


@router.message(CommandStart(), IsSuperAdmin())
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    """
    Бот запущен администратором
    :param message:
    :param state:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.update_data(user_name=message.from_user.username)
    await message.answer(text=f'Вы администратор проекта. Выберите раздел',
                         reply_markup=keyboards_start_admin())


@router.message(F.text == 'Количество участников', IsSuperAdmin())
async def process_get_count_users(message: Message) -> None:
    """
    Получаем количество участников
    :param message:
    :return:
    """
    logging.info(f'process_get_count_users: {message.chat.id}')
    list_user = await rq.get_list_users_confirm()
    text = f'Количество пользователей прошедших модерацию для участие в конкурсе:\n<b>{len(list_user)}</b>'
    await message.answer(text=text)


@router.message(F.text == 'Получить список участников', IsSuperAdmin())
async def process_get_count_users(message: Message) -> None:
    """
    Получаем количество участников
    :param message:
    :return:
    """
    logging.info(f'process_get_count_users: {message.chat.id}')
    list_user = await rq.get_list_users_confirm()
    text = f'<b>Список пользователей для участие в конкурсе:</b>\n\n'
    i = 0
    for user in list_user:
        i += 1
        text += f'{user.moderation}. @{user.username}/{user.tg_id}\n'
        if i % 50 == 0 and i > 0:
            await asyncio.sleep(0.1)
            await message.answer(text=text)
            text = ''
    if not i % 50 == 0:
        await message.answer(text=text)


@router.callback_query(F.data.startswith('confirm'))
async def confirm_screenshot(callback: CallbackQuery, bot: Bot):
    """
    Обработка полученного скриншота от пользователя
    :param callback:
    :param bot:
    :return:
    """
    logging.info(f'confirm_screenshot {callback.message.chat.id}')
    answer = callback.data.split('_')[1]
    tg_id = int(callback.data.split('_')[2])
    if answer == 'yes':
        count_confirm = await rq.get_list_users_confirm()
        count_confirm = len(count_confirm) + 1
        time.sleep(0.1)
        await rq.set_moderation(tg_id=tg_id, moderation=count_confirm)
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
        await callback.message.answer(text='Данные пользователя подтверждены',
                                      reply_markup=None)
        info_user: User = await rq.get_info_user(tg_id=tg_id)
        await bot.send_message(chat_id=tg_id,
                               text=f'Заявка принята! Твой порядковый номер: {info_user.moderation}\n\n'
                                    f'Итоги конкурса мы подведем 23.11., в день выхода альбома.'
                                    f' Следи за информацией в социальных сетях!')
    else:
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
        await callback.message.answer(text='Данные пользователя отклонены',
                                      reply_markup=None)
        await bot.send_message(chat_id=tg_id,
                               text=f'Заявка отклонена. Проверьте свой скриншот. Если с ним все в порядке, напишите,'
                                    f' пожалуйста, в аккаунт @brilliantsound812,'
                                    f' мы рассмотрим вашу заявку в ручном режиме.')
    await callback.answer()