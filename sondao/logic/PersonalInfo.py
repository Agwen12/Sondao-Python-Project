from dataclasses import dataclass, field
from datetime import date
from DocumentType import DocumentType


@dataclass
class Document:
    type: DocumentType
    code: str
    note: str
    date: date = None


@dataclass
class PersonalInfo:  # TODO WAIT FOR OTHER DOCS
    name: str
    surname: str
    PESEL: str
    phone_number: str
    home_address: str
    birthday: date
    is_dead: bool = False
    documents: dict[DocumentType: Document] = field(default_factory=lambda: dict.fromkeys(list(DocumentType)))


class RelativesInfo(PersonalInfo):
    supposed_death_notification: date = None