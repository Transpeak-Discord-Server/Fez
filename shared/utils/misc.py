class HasId(Protocol):
    id: int

def get_ids(items: Iterable[HasId]):
    return [item.id for item in items]