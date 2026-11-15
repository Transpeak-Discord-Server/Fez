from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message_count: Mapped[int] = mapped_column(Integer)
    under_18: Mapped[bool] = mapped_column(Boolean)
    reg_banned: Mapped[bool] = mapped_column(Boolean)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Watchlist(Base):
    __tablename__ = 'watchlist'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class VcWatch(Base):
    __tablename__ = 'vc_watch'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class SpecialConsiderations(Base):
    __tablename__ = 'special_considerations'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Names(Base):
    __tablename__ = 'names'
    name_occurrence_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

class UserRole(Base):
    __tablename__ = 'user_role'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class MessageCountWeek(Base):
    __tablename__ = 'message_count_week'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    week: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)

class Warn(Base):
    __tablename__ = 'warn'
    warn_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    reason: Mapped[str] = mapped_column(String)
    issuer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    warn_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    warn_type: Mapped[str] = mapped_column(String)

class Ban(Base):
    __tablename__ = 'ban'
    ban_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    reason: Mapped[str] = mapped_column(String)
    issuer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    ban_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    ban_type: Mapped[str] = mapped_column(String)

class OptinBan(Base):
    __tablename__ = 'optin_ban'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class ImageRestricted(Base):
    __tablename__ = 'image_restricted'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)

class Event(Base):
    __tablename__ = 'event'
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fire_time: Mapped[datetime] = mapped_column(DateTime)
    type: Mapped[str] = mapped_column(String)
    data: Mapped[dict] = mapped_column(JSON)

class BottomPinnedMessage(Base):
    __tablename__ = 'bottom_pinned_message'
    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger)

class DmReminder(Base):
    __tablename__ = 'dm_reminder'
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class Help(Base):
    __tablename__ = 'help'
    command: Mapped[str] = mapped_column(String, primary_key=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    format: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    level: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Glossary(Base):
    __tablename__ = 'glossary'
    word: Mapped[str] = mapped_column(String, primary_key=True)
    definition: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class GlossaryAliases(Base):
    __tablename__ = 'glossary_aliases'
    word: Mapped[str] = mapped_column(String, ForeignKey('glossary.word'), primary_key=True)
    alias: Mapped[str] = mapped_column(String, primary_key=True)

class Stars(Base):
    __tablename__ = 'stars'
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    staff_board: Mapped[bool] = mapped_column(Boolean, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    deleted: Mapped[bool] = mapped_column(Boolean)
    board_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    author_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))

class CommandLog(Base):
    __tablename__ = 'command_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    command: Mapped[str] = mapped_column(String)
    args: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class RegistrationStatusLog(Base):
    __tablename__ = 'registration_status_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))