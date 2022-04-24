from enum import Enum, auto, unique


@unique
class RelationTypes(Enum):
    CHILD = auto()  ## zgidy na odrzucenie dla nieletniego
    FULL_ADOPTED_CHILD = auto()
    PARTIAL_ADOPTED_CHILD = auto()
    SIBLING = auto()
    PARENT = auto()
    FULL_ADOPTED_PARENT = auto()
    PARTIAL_ADOPTED_PARENT = auto()
    SPOUSE = auto()
    EX_SPOUSE = auto()

## definie niezwłocznie
# data wpływu
# prawomocnosci
# zwrócenei się o odpisa prawomocny
# data doręcznia
