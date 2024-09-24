from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id_user: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20), default='none')
    screenshot: Mapped[str] = mapped_column(String, default='none')
    moderation: Mapped[int] = mapped_column(Integer, default=0)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

