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

from datetime import datetime, timezone
from typing import Optional

import sqlalchemy
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, JSON, String, MetaData
from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

metadata = MetaData(schema="transpeak")

class BanType(Enum):
    permanent = "permanent"
    temporary = "temporary"
    vc = "vc"
    vc_soft = "vc_soft"

class WarnType(Enum):
    hard = "hard"
    soft = "soft"
    staff = "staff"

class EventType(Enum):
    reminder = "reminder"
    staff_reminder = "staff_reminder"
    temp_ban_expiry = "temp_ban_expiry"

class UserLevel(Enum):
    user = "user"
    helper = "helper"
    staff = "staff"

class User(Base):
    __tablename__ = 'user'
    metadata = metadata
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message_count: Mapped[int] = mapped_column(Integer)
    under_18: Mapped[bool] = mapped_column(Boolean)
    reg_banned: Mapped[bool] = mapped_column(Boolean)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Watchlist(Base):
    __tablename__ = 'watchlist'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class VcWatch(Base):
    __tablename__ = 'vc_watch'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class SpecialConsiderations(Base):
    __tablename__ = 'special_considerations'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Names(Base):
    __tablename__ = 'names'
    metadata = metadata
    name_occurrence_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

class UserRole(Base):
    __tablename__ = 'user_role'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class MessageCountWeek(Base):
    __tablename__ = 'message_count_week'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    week: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)

class Warn(Base):
    __tablename__ = 'warn'
    metadata = metadata
    warn_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    reason: Mapped[str] = mapped_column(String)
    issuer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    warn_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    warn_type: Mapped[WarnType] = mapped_column(sqlalchemy.Enum(WarnType, name="warn_type", metadata=metadata))

class Ban(Base):
    __tablename__ = 'ban'
    metadata = metadata
    ban_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    reason: Mapped[str] = mapped_column(String)
    issuer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    ban_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    ban_type: Mapped[BanType] = mapped_column(sqlalchemy.Enum(BanType, name="ban_type", metadata=metadata))

class OptinBan(Base):
    __tablename__ = 'optin_ban'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    channel_name: Mapped[str] = mapped_column(String, primary_key=True)

class ImageRestricted(Base):
    __tablename__ = 'image_restricted'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)

class Event(Base):
    __tablename__ = 'event'
    metadata = metadata
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fire_time: Mapped[datetime] = mapped_column(DateTime)
    type: Mapped[EventType] = mapped_column(sqlalchemy.Enum(EventType, name="event_type", metadata=metadata))
    data: Mapped[dict] = mapped_column(JSON)

class BottomPinnedMessage(Base):
    __tablename__ = 'bottom_pinned_message'
    metadata = metadata
    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger)

class DmReminder(Base):
    __tablename__ = 'dm_reminder'
    metadata = metadata
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class Help(Base):
    __tablename__ = 'help'
    metadata = metadata
    command: Mapped[str] = mapped_column(String, primary_key=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    format: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    level: Mapped[Optional[UserLevel]] = mapped_column(sqlalchemy.Enum(UserLevel, name="user_level", metadata=metadata), nullable=True)

class Glossary(Base):
    __tablename__ = 'glossary'
    metadata = metadata
    word: Mapped[str] = mapped_column(String, primary_key=True)
    definition: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class GlossaryAliases(Base):
    __tablename__ = 'glossary_aliases'
    metadata = metadata
    word: Mapped[str] = mapped_column(String, ForeignKey('glossary.word'), primary_key=True)
    alias: Mapped[str] = mapped_column(String, primary_key=True)

class Stars(Base):
    __tablename__ = 'stars'
    metadata = metadata
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    staff_board: Mapped[bool] = mapped_column(Boolean, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    deleted: Mapped[bool] = mapped_column(Boolean)
    board_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    author_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))

class CommandLog(Base):
    __tablename__ = 'command_log'
    metadata = metadata
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    command: Mapped[str] = mapped_column(String)
    args: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class RegistrationStatusLog(Base):
    __tablename__ = 'registration_status_log'
    metadata = metadata
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))