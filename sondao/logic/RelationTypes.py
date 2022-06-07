from enum import Enum, auto, unique


@unique
class RelationTypes(Enum):
    CHILD = "Child"
    FULL_ADOPTED_CHILD = "Full adopted child"
    PARTIAL_ADOPTED_CHILD = "Partial adopted child"
    SIBLING = "Sibling"
    PARENT = "Parent"
    FULL_ADOPTED_PARENT = "Full adopted parent"
    PARTIAL_ADOPTED_PARENT = "Partial adopted parent"
    SPOUSE = "Spouse"
    EX_SPOUSE = "Ex-spouse"

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
            case "SPOUSE":
                return RelationTypes.SPOUSE

# CHILD
# SIBLING
# CHILD
# PARENT


# definie niezwłocznie
# data wpływu
# prawomocnosci
# zwrócenei się o odpisa prawomocny
# data doręcznia
