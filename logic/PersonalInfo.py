from dataclasses import dataclass, field
from datetime import date
from DocumentType import DocumentType


@dataclass
class GenericDocument:
    type: DocumentType
    code: str
    note: str
    date: date = None


@dataclass
class PersonalInfo: #TODO THINK ABOUT OTHER DOCS -> maybe divide to testaor/relatives info or idk -> relation info (ex or current wife for example)
    name: str
    surname: str
    PESEL: str
    phone_number: str
    home_address: str
    birthday: date
    deathdate: date = None
    documents: dict[DocumentType: GenericDocument] = field(default_factory=lambda: dict.fromkeys(list(DocumentType)))
