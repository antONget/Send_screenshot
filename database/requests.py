from database.models import User
from database.models import async_session
from sqlalchemy import select
import logging


"""USER"""


async def add_user(tg_id: int, data: dict) -> None:
    """
    Добавляем нового пользователя если его еще нет в БД
    :param tg_id:
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # если пользователя нет в базе
        if not user:
            session.add(User(**data))
            await session.commit()


async def get_all_users() -> list[User]:
    """
    Получаем список всех пользователей зарегистрированных в боте
    :return:
    """
    logging.info(f'get_all_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users


async def get_list_users() -> list:
    """
    ПОЛЬЗОВАТЕЛЬ - список пользователей верифицированных в боте
    :return:
    """
    logging.info(f'get_list_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        return [[user.tg_id, user.username] for user in users]


async def update_user(tg_id: int, screenshot: str, email: str) -> None:
    """
    Обновляем данные пользователя
    :return:
    """
    logging.info(f'get_list_users')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.screenshot = screenshot
            if email:
                user.email = email
            await session.commit()


async def get_list_users_confirm() -> list:
    """
    Список пользователей прошедших модерацию
    :return:
    """
    logging.info(f'get_list_users')
    async with async_session() as session:
        users = await session.scalars(select(User).where(User.moderation != 0))
        return [user for user in users]


async def set_moderation(tg_id: int, moderation: int) -> None:
    """
    Обновляем модерацию скриншота
    :return:
    """
    logging.info(f'get_list_users')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.moderation = moderation
            await session.commit()


async def get_info_user(tg_id: int) -> User:
    """
    Получаем данные пользователя
    :return:
    """
    logging.info(f'get_list_users tg_id-{tg_id}')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
