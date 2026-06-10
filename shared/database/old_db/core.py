from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class _Base(DeclarativeBase):
    pass

class _Reglog(_Base):
    __tablename__ = 'reglog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Text, nullable=True)
    user = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)


class _Staffwarning(_Base):
    __tablename__ = 'staffwarnings'

    id = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    issuer_id = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)


class _Lastchance(_Base):
    __tablename__ = 'lastchance'

    id = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)


class _Vcwatch(_Base):
    __tablename__ = 'vcwatch'

    id = Column(Text, nullable=True)


class _Msgcount(_Base):
    __tablename__ = 'msgcount'

    id = Column(Text, nullable=True)
    count = Column(Text, nullable=True)
    lastmsg = Column(Text, nullable=True)


class _Dmreminder(_Base):
    __tablename__ = 'dmreminders'

    message_id = Column(Text, nullable=True)
    user_id = Column(Text, nullable=True)


class _Watchlist(_Base):
    __tablename__ = 'watchlist'

    id = Column(Text, nullable=True)
    desc = Column(Text, nullable=True)


class _Registered(_Base):
    __tablename__ = 'registered'

    user_id = Column(Text, nullable=True)
    mc_name = Column(Text, nullable=True)


class _Ban(_Base):
    __tablename__ = 'bans'

    userid = Column(Text, nullable=True)
    banner = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)


class _Wallet(_Base):
    __tablename__ = 'wallets'

    id = Column(Text, nullable=True)
    amount = Column(Text, nullable=True)


class _Warn(_Base):
    __tablename__ = 'warns'

    id = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    issuer_id = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)


class _MsgcountWeek(_Base):
    __tablename__ = 'msgcount_week'

    id = Column(Text, nullable=True)
    week = Column(Text, nullable=True)
    count = Column(Text, nullable=True)


class _Glossary(_Base):
    __tablename__ = 'glossary'

    word = Column(Text, nullable=True)
    definition = Column(Text, nullable=True)
    aliases = Column(Text, nullable=True)


class _Optinban(_Base):
    __tablename__ = 'optinban'

    id = Column(Text, nullable=True)
    chan = Column(Text, nullable=True)

class _Vcban(_Base):
    __tablename__ = 'vcban'

    id = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    issuer_id = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)
    softban = Column(Text, nullable=True)


class _Not18(_Base):
    __tablename__ = 'not18'

    id = Column(Text, nullable=True)


class _Note(_Base):
    __tablename__ = 'notes'

    id = Column(Text, nullable=True)
    msg = Column(Text, nullable=True)


class _Todo(_Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)
    task = Column(Text, nullable=True)
    status = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=True, default=0)


class _Activity(_Base):
    __tablename__ = 'activity'

    id = Column(Text, nullable=True)


class _Bio(_Base):
    __tablename__ = 'bios'

    name = Column(Text, nullable=True)
    user_id = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)


class _Help(_Base):
    __tablename__ = 'help'

    command = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    user = Column(Text, nullable=True)
    format = Column(Text, nullable=True)
    desc = Column(Text, nullable=True)
    level = Column(Text, nullable=True)

class _Online(_Base):
    __tablename__ = 'online'

    id = Column(Text, nullable=True)
    lastonline = Column(Text, nullable=True)


class _Sc(_Base):
    __tablename__ = 'sc'

    id = Column(Text, nullable=True)
    desc = Column(Text, nullable=True)


class _Timezone(_Base):
    __tablename__ = 'timezones'

    id = Column(Text, nullable=True)
    tz = Column(Text, nullable=True)


class _Name(_Base):
    __tablename__ = 'names'

    id = Column(Text, nullable=True)
    name = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)


class _Regban(_Base):
    __tablename__ = 'regban'

    id = Column(Text, nullable=True)


class _Event(_Base):
    __tablename__ = 'events'

    fire_time = Column(Integer, nullable=True)
    type = Column(Text, nullable=True)
    data = Column(Text, nullable=True)


class _Commandlog(_Base):
    __tablename__ = 'commandlog'

    id = Column(Text, nullable=True)
    timestamp = Column(Text, nullable=True)
    command = Column(Text, nullable=True)
    commandargs = Column(Text, nullable=True)


class _Star(_Base):
    __tablename__ = 'stars'

    msgid = Column(Text, nullable=True)
    count = Column(Integer, nullable=True)
    deleted = Column(Text, nullable=True)
    starid = Column(Text, nullable=True)
    authorid = Column(Text, nullable=True)

class _Ir(_Base):
    __tablename__ = 'ir'

    id = Column(Text, nullable=True)


class _Role(_Base):
    __tablename__ = 'roles'

    userid = Column(Text, nullable=True)
    roles = Column(Text, nullable=True)