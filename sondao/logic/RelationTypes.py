from enum import Enum, auto


class RelationTypes(Enum):
    CHILD = auto()
    FULL_ADOPTED_CHILD = auto()
    PARTIAL_ADOPTED_CHILD = auto()
    SIBLING = auto()
    PARENT = auto()
    SPOUSE = auto()
    EX_SPOUSE = auto()

