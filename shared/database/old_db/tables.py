from sqlalchemy import Integer, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column


class _Base(DeclarativeBase):
    pass

class _Reglog(_Base):
    __tablename__ = 'reglog'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    status = mapped_column(Text, nullable=True)
    user = mapped_column(Text, nullable=True)
    timestamp = mapped_column(Text, nullable=True)


class _Staffwarning(_Base):
    __tablename__ = 'staffwarnings'

    id = mapped_column(Text, primary_key=True)
    reason = mapped_column(Text, nullable=True)
    issuer_id = mapped_column(Text, nullable=True)
    timestamp = mapped_column(Text, primary_key=True)


class _Lastchance(_Base):
    __tablename__ = 'lastchance'

    id = mapped_column(Text, primary_key=True)
    timestamp = mapped_column(Text, primary_key=True)


class _Vcwatch(_Base):
    __tablename__ = 'vcwatch'

    id = mapped_column(Text, primary_key=True)


class _Msgcount(_Base):
    __tablename__ = 'msgcount'

    id = mapped_column(Text, primary_key=True)
    count = mapped_column(Text, nullable=True)
    lastmsg = mapped_column(Text, nullable=True)


class _Dmreminder(_Base):
    __tablename__ = 'dmreminders'

    message_id = mapped_column(Text, primary_key=True)
    user_id = mapped_column(Text, primary_key=True)


class _Watchlist(_Base):
    __tablename__ = 'watchlist'

    id = mapped_column(Text, primary_key=True)
    desc = mapped_column(Text, nullable=True)


class _Registered(_Base):
    __tablename__ = 'registered'

    user_id = mapped_column(Text, primary_key=True)
    mc_name = mapped_column(Text, nullable=True)


class _Ban(_Base):
    __tablename__ = 'bans'

    userid = mapped_column(Text, primary_key=True)
    banner = mapped_column(Text, primary_key=True)
    timestamp = mapped_column(Text, primary_key=True)
    reason = mapped_column(Text, nullable=True)


class _Wallet(_Base):
    __tablename__ = 'wallets'

    id = mapped_column(Text, primary_key=True)
    amount = mapped_column(Text, nullable=True)


class _Warn(_Base):
    __tablename__ = 'warns'

    id = mapped_column(Text, primary_key=True)
    reason = mapped_column(Text, nullable=True)
    issuer_id = mapped_column(Text, nullable=True)
    timestamp = mapped_column(Text, primary_key=True)


class _MsgcountWeek(_Base):
    __tablename__ = 'msgcount_week'

    id = mapped_column(Text, primary_key=True)
    week = mapped_column(Text, primary_key=True)
    count = mapped_column(Text, nullable=True)


class _Glossary(_Base):
    __tablename__ = 'glossary'

    word = mapped_column(Text, primary_key=True)
    definition = mapped_column(Text, nullable=True)
    aliases = mapped_column(Text, nullable=True)


class _Optinban(_Base):
    __tablename__ = 'optinban'

    id = mapped_column(Text, primary_key=True)
    chan = mapped_column(Text, primary_key=True)

class _Vcban(_Base):
    __tablename__ = 'vcban'

    id = mapped_column(Text, primary_key=True)
    reason = mapped_column(Text, nullable=True)
    issuer_id = mapped_column(Text, nullable=True)
    timestamp = mapped_column(Text, primary_key=True)
    softban = mapped_column(Text, nullable=True)


class _Not18(_Base):
    __tablename__ = 'not18'

    id = mapped_column(Text, primary_key=True)


class _Note(_Base):
    __tablename__ = 'notes'

    id = mapped_column(Text, primary_key=True)
    msg = mapped_column(Text, nullable=True)


class _Todo(_Base):
    __tablename__ = 'todo'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid = mapped_column(Text, nullable=True)
    timestamp = mapped_column(Text, nullable=True)
    task = mapped_column(Text, nullable=True)
    status = mapped_column(Integer, nullable=True)
    priority = mapped_column(Integer, nullable=True, default=0)


class _Activity(_Base):
    __tablename__ = 'activity'

    id = mapped_column(Text, primary_key=True)


class _Bio(_Base):
    __tablename__ = 'bios'

    name = mapped_column(Text, nullable=True)
    user_id = mapped_column(Text, primary_key=True)
    bio = mapped_column(Text, nullable=True)


class _Help(_Base):
    __tablename__ = 'help'

    command = mapped_column(Text, primary_key=True)
    category = mapped_column(Text, nullable=True)
    user = mapped_column(Text, nullable=True)
    format = mapped_column(Text, nullable=True)
    desc = mapped_column(Text, nullable=True)
    level = mapped_column(Text, nullable=True)

class _Online(_Base):
    __tablename__ = 'online'

    id = mapped_column(Text, primary_key=True)
    lastonline = mapped_column(Text, nullable=True)


class _Sc(_Base):
    __tablename__ = 'sc'

    id = mapped_column(Text, primary_key=True)
    desc = mapped_column(Text, nullable=True)


class _Timezone(_Base):
    __tablename__ = 'timezones'

    id = mapped_column(Text, primary_key=True)
    tz = mapped_column(Text, nullable=True)


class _Name(_Base):
    __tablename__ = 'names'

    id = mapped_column(Text, primary_key=True)
    name = mapped_column(Text, nullable=True)
    timestamp = mapped_column(Text, nullable=True)


class _Regban(_Base):
    __tablename__ = 'regban'

    id = mapped_column(Text, primary_key=True)


class _Event(_Base):
    __tablename__ = 'events'

    fire_time = mapped_column(Integer, primary_key=True)
    type = mapped_column(Text, nullable=True)
    data = mapped_column(Text, primary_key=True)


class _Commandlog(_Base):
    __tablename__ = 'commandlog'

    id = mapped_column(Text, primary_key=True)
    timestamp = mapped_column(Text, primary_key=True)
    command = mapped_column(Text, nullable=True)
    commandargs = mapped_column(Text, nullable=True)


class _Star(_Base):
    __tablename__ = 'stars'

    msgid = mapped_column(Text, primary_key=True)
    count = mapped_column(Integer, nullable=True)
    deleted = mapped_column(Text, nullable=True)
    starid = mapped_column(Text, nullable=True)
    authorid = mapped_column(Text, nullable=True)

class _Ir(_Base):
    __tablename__ = 'ir'

    id = mapped_column(Text, primary_key=True)


class _Role(_Base):
    __tablename__ = 'roles'

    userid = mapped_column(Text, primary_key=True)
    roles = mapped_column(Text, nullable=True)