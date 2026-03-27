### Database

The database is not stored within the Git repository, only on the server. This project uses a PostgreSQL database.

```postgresql
CREATE TABLE IF NOT EXISTS reglog(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    status TEXT,
    "user" TEXT,
    timestamp TEXT);

CREATE TABLE IF NOT EXISTS staffwarnings(
    id TEXT,
    reason TEXT,
    issuer_id TEXT,
    timestamp TEXT);
CREATE INDEX IF NOT EXISTS staffwarningsindexid on staffwarnings(id);

CREATE TABLE IF NOT EXISTS lastchance(
    id TEXT,
    timestamp TEXT);

CREATE TABLE IF NOT EXISTS vcwatch(
    id TEXT);
CREATE INDEX IF NOT EXISTS vcwatchindexid on vcwatch(id);

CREATE TABLE IF NOT EXISTS msgcount(
    id TEXT,
    count TEXT,
    lastmsg TEXT);
CREATE INDEX IF NOT EXISTS msgcountindexid on msgcount(id);

CREATE TABLE IF NOT EXISTS dmreminders(
    messageID TEXT,
    userID TEXT);

CREATE TABLE IF NOT EXISTS watchlist(
    id TEXT,
    "desc" TEXT);
CREATE INDEX IF NOT EXISTS watchlistindexid on watchlist(id);

CREATE TABLE IF NOT EXISTS registered(
    user_id TEXT,
    mc_name TEXT);
CREATE INDEX IF NOT EXISTS registeredindexid on registered(user_id);

CREATE TABLE IF NOT EXISTS bans(
    userid TEXT,
    banner TEXT,
    timestamp TEXT,
    reason TEXT);
CREATE INDEX IF NOT EXISTS userid on bans(userid);

CREATE TABLE IF NOT EXISTS wallets(
    id TEXT,
    amount TEXT);
CREATE INDEX IF NOT EXISTS walletsindexid on wallets(id);

CREATE TABLE IF NOT EXISTS warns(
    id TEXT,
    reason TEXT,
    issuer_id TEXT,
    timestamp TEXT);
CREATE INDEX IF NOT EXISTS warnsindexid on warns(id);

CREATE TABLE IF NOT EXISTS msgcount_week(
    id TEXT,
    week TEXT,
    count TEXT);

CREATE TABLE IF NOT EXISTS "glossary" (
    Word TEXT NULL,
    Definition TEXT NULL,
    Aliases TEXT NULL);
CREATE INDEX IF NOT EXISTS glossary_index ON glossary(LOWER(Word));

CREATE TABLE IF NOT EXISTS optinban(
    id TEXT,
    chan TEXT);
CREATE INDEX IF NOT EXISTS optinbanindex on optinban(id);

CREATE TABLE IF NOT EXISTS vcban(
    id TEXT,
    reason TEXT,
    issuer_id TEXT,
    timestamp TEXT,
    softban TEXT);
CREATE INDEX IF NOT EXISTS vcbanindex on vcban(id);

CREATE TABLE IF NOT EXISTS not18(
    id TEXT);
CREATE INDEX IF NOT EXISTS not18indexid on not18(id);

CREATE TABLE IF NOT EXISTS notes(
    id TEXT,
    msg TEXT);
CREATE INDEX IF NOT EXISTS notesindex on notes(id);

CREATE TABLE IF NOT EXISTS todo(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    userid TEXT,
    timestamp TEXT,
    task TEXT,
    status INT,
    priority int default 0);

CREATE TABLE IF NOT EXISTS activity(
    id TEXT,
    total_time TEXT);
CREATE INDEX IF NOT EXISTS activityindexid on activity(id);

CREATE TABLE IF NOT EXISTS bios(
    name TEXT,
    user_id TEXT,
    bio TEXT);
CREATE INDEX IF NOT EXISTS biosindexid on bios(user_id);

CREATE TABLE IF NOT EXISTS "help" (
        command TEXT,
        category TEXT,
        "user" TEXT,
        format TEXT,
        "desc" TEXT,
        level TEXT
);

CREATE TABLE IF NOT EXISTS msgcount_week(
    id TEXT,
    week TEXT,
    count TEXT);

CREATE TABLE IF NOT EXISTS online(
    id TEXT,
    lastonline TEXT);
CREATE INDEX IF NOT EXISTS onlineindexid on online(id);

CREATE TABLE IF NOT EXISTS sc(
    id TEXT,
    "desc" TEXT);
CREATE INDEX IF NOT EXISTS scindexid on sc(id);

CREATE TABLE IF NOT EXISTS timezones(
    id TEXT,
    tz TEXT);
CREATE INDEX IF NOT EXISTS timezonesid on timezones(id);

CREATE TABLE IF NOT EXISTS names(
    id TEXT,
    name TEXT,
    timestamp TEXT);
CREATE INDEX IF NOT EXISTS namesindexid on names(id);

CREATE TABLE IF NOT EXISTS regban(
    id TEXT);
CREATE INDEX IF NOT EXISTS regbanindex on regban(id);

CREATE TABLE IF NOT EXISTS events(
    fire_time INTEGER,
    type TEXT,
    data TEXT);
CREATE INDEX IF NOT EXISTS events_time_index on events(fire_time);

CREATE TABLE IF NOT EXISTS commandlog(
    id TEXT,
    timestamp TEXT,
    command TEXT,
    commandargs TEXT);

CREATE TABLE IF NOT EXISTS stars(
    msgid TEXT,
    count INT,
    deleted TEXT,
    starid TEXT,
    authorid TEXT);
CREATE INDEX IF NOT EXISTS starsindexid ON stars(msgid);
CREATE INDEX IF NOT EXISTS scoreindex ON stars(authorid);

CREATE TABLE IF NOT EXISTS ir(
    id TEXT);

CREATE TABLE IF NOT EXISTS roles(
    userid TEXT,
    roles TEXT);
```