from enum import Enum, unique


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
        match relation:
            case "SIBLING":
                return RelationTypes.SIBLING
            case "CHILD":
                return RelationTypes.CHILD
            case "PARENT":
                return RelationTypes.PARENT
            case "SPOUSE":
                return RelationTypes.SPOUSE
