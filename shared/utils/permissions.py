from discord import Member
from discord.ext import commands
from shared.utils import misc
import os
import json
CURRENT_PATH = os.path.dirname(__file__)
from shared.config import Config
from enum import Enum

rl_id = Config.json_config['rl_id']

class Level(Enum):
    REGISTERED = 0
    REGULAR = 1
    HELPER = 2
    STAFF = 3
    LEAD = 4
    ADMIN = 5
    CO_OWNER = 6
    OWNER = 7

class PermissionManager:

    _OWNER = [rl_id['owner']]
    _CO_OWNER = [rl_id['co-owner'], *_OWNER]
    _ADMIN = [rl_id['*'], *_CO_OWNER]
    _LEAD = [rl_id['a-director'], *_ADMIN]
    _STAFF = [rl_id['staff'], rl_id['staff-junior'], rl_id['on-leave'], rl_id['in-training'], rl_id['-'], *_LEAD]
    _HELPER = [rl_id['helper'], *_STAFF]
    _REGULAR = [rl_id['regular'], *_HELPER]
    _REGISTERED = [rl_id['new'], *_REGULAR]

    _MAPPING = {
        Level.REGISTERED: _REGISTERED,
        Level.REGULAR: _REGULAR,
        Level.HELPER: _HELPER,
        Level.STAFF: _STAFF,
        Level.LEAD: _LEAD,
        Level.ADMIN: _ADMIN,
        Level.CO_OWNER: _CO_OWNER,
        Level.OWNER: _OWNER,
    }

    @classmethod
    def get_roles(cls, level: Level) -> list[int]:
        return cls._MAPPING.get(level, [])


class UserPermissionsError(commands.CheckFailure):
    def __init__(self, required_perms: Level):
        self.required_perms = required_perms
        super().__init__(f"User tried to use a command for {required_perms.name}")


def has_permission(member: Member, permission_level: Level) -> bool:
    user_roles = set(misc.get_ids(member.roles))
    staff_roles = set(PermissionManager.get_roles(permission_level))
    return not user_roles.isdisjoint(staff_roles)


def permission_check(permission_level: Level):
    async def predicate(ctx: commands.Context):
        if has_permission(ctx.author, permission_level):
            return True
        raise UserPermissionsError(permission_level)

    return commands.check(predicate)
