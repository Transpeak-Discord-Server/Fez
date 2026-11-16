from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


@dataclass
class User:
    id: int
    message_count: int
    under_18: bool
    reg_banned: bool
    bio: Optional[str]
    last_seen: Optional[datetime]
    last_message: Optional[str]


class BanType(Enum):
    Permanent = "permanent"
    Temporary = "temporary"
    VC = "vc"
    VCSoft = "vc_soft"

@dataclass
class Ban:
    ban_id: int
    user_id: int
    issuer_id: int
    reason: str
    timestamp: datetime
    ban_type: BanType