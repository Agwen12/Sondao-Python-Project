from enum import Enum, auto, unique


@unique
class RelationTypes(Enum):
    CHILD = auto()  ## zgidy na odrzucenie dla nieletniego 1
    FULL_ADOPTED_CHILD = auto() # 2
    PARTIAL_ADOPTED_CHILD = auto() # 3
    SIBLING = auto() # 4
    PARENT = auto() # 5
    FULL_ADOPTED_PARENT = auto() # 6
    PARTIAL_ADOPTED_PARENT = auto() # 7
    SPOUSE = auto() # 8
    EX_SPOUSE = auto() # 9

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

    def opposite(self):
        match self:
            case RelationTypes.CHILD | RelationTypes.PARTIAL_ADOPTED_CHILD | RelationTypes.FULL_ADOPTED_CHILD:
                return RelationTypes.PARENT
            case RelationTypes.PARENT:
                return RelationTypes.CHILD
            case _:
                return self

    @staticmethod
    def from_string(relation: str):
        # TODO all possibilities
        # print(type(relation))
        # print(relation)
        match relation:
            case "SIBLING":
                return RelationTypes.SIBLING
            case "CHILD":
                return RelationTypes.CHILD
            case "PARENT":
                return RelationTypes.PARENT

# CHILD
# SIBLING
# CHILD
# PARENT


# definie niezwłocznie
# data wpływu
# prawomocnosci
# zwrócenei się o odpisa prawomocny
# data doręcznia
