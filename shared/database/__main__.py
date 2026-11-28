# Fez/TransBot - A Discord.py bot for Transpeak
# Copyright (C) 2026 Fez project contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from shared.database.BanDAO import BanDAO


class Database:

    engine: AsyncEngine
    async_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, url: URL):
        self.engine = create_async_engine(url)
        self.async_session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    @staticmethod
    def ban_dao(session: AsyncSession) -> BanDAO:
        return BanDAO(session)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_session_maker() as session:
            try:
                yield session
            finally:
                await session.commit()
                await session.close()

env_path = Path(__file__) / ".." / ".." / ".env"
env = load_dotenv(env_path)

def get_database() -> Database:
    db_url_username = os.getenv("DB_USERNAME")
    db_url_password = os.getenv("DB_PASSWORD")
    db_url_host = os.getenv("DB_HOST")
    db_url_database = os.getenv("DB_DATABASE")
    if not db_url_username or not db_url_password or not db_url_host or not db_url_database:
        raise ValueError("Database .env variables not set")
    db_url = URL.create(
        "postgresql+psycopg",
        username=db_url_username,
        password=db_url_password,
        host=db_url_host,
        database=db_url_database)
    return Database(db_url)