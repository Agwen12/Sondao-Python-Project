from enum import Enum, auto


class DocumentType(Enum):  # TODO WAIT FOR INFO ABOUT OTHER
    DEATH_CERTIFICATE = auto()
    BIRTH_CERTIFICATE = auto()
    MARRIAGE_CERTIFICATE = auto()
    INHERITANCE_REJECTION = auto()
    OTHER = auto()
