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

@dataclass
class MessageCountWeek:
    user_id: int
    week: int
    count: int

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