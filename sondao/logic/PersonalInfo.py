from dataclasses import dataclass, field
from datetime import date
from sondao.logic.DocumentType import DocumentType


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
    documents: dict[DocumentType: Document] = field(default_factory=lambda: dict.fromkeys(list(DocumentType))) #TODO LISTA MOZE, NP 2 akty slubu
    proxy: str = None # pelnomocnik dla dzieciaka
    notes: str = None
    receive_confirmation_place: str = None


@dataclass
class RelativesInfo(PersonalInfo):
    want_inherit: bool = True
    supposed_death_notification: date = None