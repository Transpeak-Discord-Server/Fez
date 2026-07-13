from dataclasses import dataclass, field

@dataclass
class UserData:

    id: int
    message_count: int
    roles: list[int] = field(default_factory=list)
    bans: list[BanData] = field(default_factory=list)
    weekly_messages: list[UserMessagesWeekData] = field(default_factory=list)

@dataclass
class BanData:

    user: int
    banner: int
    timestamp: int
    reason: str
    links: list[str]

@dataclass
class UserMessagesWeekData:

    user: int
    messages: int
    week: int