from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    messageCount: Mapped[int] = mapped_column(Integer)
    under18: Mapped[bool] = mapped_column(Boolean)
    regBanned: Mapped[bool] = mapped_column(Boolean)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lastSeen: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    lastMessage: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Watchlist(Base):
    __tablename__ = 'watchlist'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class VcWatch(Base):
    __tablename__ = 'vc_watch'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class SpecialConsiderations(Base):
    __tablename__ = 'special_considerations'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Names(Base):
    __tablename__ = 'names'
    nameOccurrenceId: Mapped[int] = mapped_column(Integer, primary_key=True)
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

class UserRole(Base):
    __tablename__ = 'user_role'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    roleId: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class MessageCountWeek(Base):
    __tablename__ = 'message_count_week'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    week: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)

class Warn(Base):
    __tablename__ = 'warn'
    warnId: Mapped[int] = mapped_column(Integer, primary_key=True)
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    reason: Mapped[str] = mapped_column(String)
    issuerId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    warnTimestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    warnType: Mapped[str] = mapped_column(String)

class Ban(Base):
    __tablename__ = 'ban'
    banId: Mapped[int] = mapped_column(Integer, primary_key=True)
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    reason: Mapped[str] = mapped_column(String)
    issuerId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    banTimestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    banType: Mapped[str] = mapped_column(String)

class OptinBan(Base):
    __tablename__ = 'optin_ban'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    channelId: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class ImageRestricted(Base):
    __tablename__ = 'image_restricted'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)

class Event(Base):
    __tablename__ = 'event'
    eventId: Mapped[int] = mapped_column(Integer, primary_key=True)
    fireTime: Mapped[datetime] = mapped_column(DateTime)
    type: Mapped[str] = mapped_column(String)
    data: Mapped[dict] = mapped_column(JSON)

class BottomPinnedMessage(Base):
    __tablename__ = 'bottom_pinned_message'
    channelId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    messageId: Mapped[int] = mapped_column(BigInteger)

class DmReminder(Base):
    __tablename__ = 'dm_reminder'
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), primary_key=True)
    messageId: Mapped[int] = mapped_column(BigInteger, primary_key=True)

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
    messageId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    staffBoard: Mapped[bool] = mapped_column(Boolean, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    deleted: Mapped[bool] = mapped_column(Boolean)
    boardMessageId: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    authorId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))

class CommandLog(Base):
    __tablename__ = 'command_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    command: Mapped[str] = mapped_column(String)
    args: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class RegistrationStatusLog(Base):
    __tablename__ = 'registration_status_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[bool] = mapped_column(Boolean)
    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)