from functools import singledispatch
from datetime import datetime
from typing import Iterable, Protocol


class HasId(Protocol):
    id: int

def get_ids(items: Iterable[HasId]):
    return [item.id for item in items]


# format time

@singledispatch
def format_time(time, time_format: str = "t") -> str:
    return f"<t:{int(time)}:{time_format}>"

@format_time.register(datetime)
def _(time: datetime, time_format: str = "t") -> str:
    return format_time(int(time.timestamp()), time_format)