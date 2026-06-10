### Database

The database is not stored within the Git repository, only on the server.

Currently, the database uses SQLite, however we plan to clean up the structure and migrate it to PostgreSQL.

### Old Schema
```sqlite
CREATE TABLE reglog(id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT, user TEXT, timestamp TEXT);
CREATE TABLE staffwarnings(id TEXT, reason TEXT, issuer_id TEXT, timestamp TEXT);
CREATE INDEX staffwarningsindexid on staffwarnings(id);
CREATE TABLE lastchance(id TEXT, timestamp TEXT);
CREATE TABLE vcwatch(id TEXT);
CREATE INDEX vcwatchindexid on vcwatch(id);
CREATE TABLE msgcount(id TEXT, count TEXT, lastmsg TEXT);
CREATE INDEX msgcountindexid on msgcount(id);
CREATE TABLE dmreminders(messageID TEXT, userID TEXT);
CREATE TABLE watchlist(id TEXT, desc TEXT);
CREATE INDEX watchlistindexid on watchlist(id);
CREATE TABLE registered(user_id TEXT, mc_name TEXT);
CREATE INDEX registeredindexid on registered(user_id);
CREATE TABLE bans(userid TEXT, banner TEXT, timestamp TEXT, reason TEXT);
CREATE INDEX userid on bans(userid);
CREATE TABLE wallets(id TEXT, amount TEXT);
CREATE INDEX walletsindexid on wallets(id);
CREATE TABLE warns(id TEXT, reason TEXT, issuer_id TEXT, timestamp TEXT);
CREATE INDEX warnsindexid on warns(id);
CREATE TABLE msgcount_week(id TEXT, week TEXT, count TEXT);
CREATE TABLE "glossary" (Word TEXT NULL, Definition TEXT NULL, Aliases TEXT NULL);
CREATE INDEX glossary_index ON glossary(LOWER(Word));
CREATE TABLE optinban(id TEXT, chan TEXT);
CREATE INDEX optinbanindex on optinban(id);
CREATE TABLE vcban(id TEXT, reason TEXT, issuer_id TEXT, timestamp TEXT, softban TEXT);
CREATE INDEX vcbanindex on vcban(id);
CREATE TABLE not18(id TEXT);
CREATE INDEX not18indexid on not18(id);
CREATE TABLE notes(id TEXT, msg TEXT);
CREATE INDEX notesindex on notes(id);
CREATE TABLE todo(id INTEGER PRIMARY KEY AUTOINCREMENT, userid TEXT, timestamp TEXT, task TEXT, status INT, priority int default 0);
CREATE TABLE activity(id TEXT, total_time, TEXT);
CREATE INDEX activityindexid on activity(id);
CREATE TABLE bios(name TEXT, user_id TEXT, bio TEXT);
CREATE INDEX biosindexid on bios(user_id);
CREATE TABLE "help" (
        `command`       TEXT,
        `category`      TEXT,
        `user`  TEXT,
        `format`        TEXT,
        `desc`  TEXT,
        `level` TEXT
);
CREATE TABLE warns(id TEXT, reason TEXT, issuer_id TEXT, timestamp TEXT);
CREATE INDEX warnsindexid on warns(id);
CREATE TABLE stars(id TEXT);
CREATE TABLE msgcount_week(id TEXT, week TEXT, count TEXT);
CREATE TABLE online(id TEXT, lastonline TEXT);
CREATE INDEX onlineindexid on online(id);
CREATE TABLE sc(id TEXT, desc TEXT);
CREATE INDEX scindexid on sc(id);
CREATE TABLE timezones(id TEXT, tz TEXT);
CREATE INDEX timezonesid on timezones(id);
CREATE TABLE names(id TEXT, name TEXT, timestamp TEXT);
CREATE INDEX namesindexid on names(id);
CREATE TABLE regban(id TEXT);
CREATE INDEX regbanindex on regban(id);
CREATE TABLE events(fire_time INTEGER, type TEXT, data TEXT);
CREATE INDEX events_time_index on events(fire_time);
CREATE TABLE commandlog(id TEXT, timestamp TEXT, command TEXT, commandargs TEXT);
CREATE TABLE stars(msgid TEXT, count INT, deleted TEXT, starid TEXT, authorid TEXT);
CREATE INDEX starsindexid ON stars(msgid);
CREATE INDEX scoreindex ON stars(authorid)
;
CREATE TABLE ir(id TEXT);
CREATE TABLE roles(userid TEXT, roles TEXT);
```