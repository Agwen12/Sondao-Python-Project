from enum import Enum


class DocumentType(Enum):
    DEATH_CERTIFICATE = "Death certificate"
    BIRTH_CERTIFICATE = "Birth certificate"
    MARRIAGE_CERTIFICATE = "Marriage certificate"
    INHERITANCE_REJECTION = "Inheritance rejection"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
