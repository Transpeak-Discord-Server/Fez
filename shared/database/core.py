from contextlib import asynccontextmanager

from dotenv import load_dotenv
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import os

ENV_PATH = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(dotenv_path=ENV_PATH)

class Base(DeclarativeBase):
    pass

class Database:

    _engine = create_async_engine(os.getenv("DATABASE_INFO"), echo=True)

    async_session = async_sessionmaker(bind=_engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self):
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()


### DATABASE TABLES ###


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message_count: Mapped[int] = mapped_column(BigInteger, default=0)

    bans: Mapped[list["Ban"]] = relationship(back_populates="user")
    messages_week: Mapped[list["UserMessagesWeek"]] = relationship(back_populates="user")
    roles: Mapped[list["UserRoles"]] = relationship(back_populates="user")


class Ban(Base):

    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    banner: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id))
    timestamp: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship(back_populates="bans")


class UserMessagesWeek(Base):

    __tablename__ = "user_messages_week"

    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    messages: Mapped[int] = mapped_column(BigInteger, default=0)
    week: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    user: Mapped["User"] = relationship(back_populates="messages_week")

class UserRoles(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    role: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True)

    user: Mapped["User"] = relationship(back_populates="roles")