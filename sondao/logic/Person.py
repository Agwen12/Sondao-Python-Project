from dataclasses import dataclass, field
from typing import TypeVar
from datetime import date
from abc import ABC, abstractmethod
from collections import namedtuple

from sondao.logic.PersonalInfo import PersonalInfo
from sondao.logic.RelationTypes import RelationTypes as RT

PersonObject = TypeVar("PersonObject")
Spouse = namedtuple("Spouse", ["person", "relation"])

#TODO TYPEVAR NIE MA SENSU UZYC KALSY KTORA NIC NIE ROBI. MOZNA TEZ ZREZYGNOWAC Z TYPINGU TUTAJ TYPOWO
@dataclass
class GenericPerson(ABC):
    personal_info: PersonalInfo

    @abstractmethod
    def add_relative(self, relative: PersonObject, relation_type: RT):
        pass


@dataclass
class Person(GenericPerson):
    children: list[GenericPerson] = field(default_factory=lambda: list())
    siblings: list[GenericPerson] = field(default_factory=lambda: list())
    parents: list[GenericPerson] = field(default_factory=lambda: list())

    def add_relative(self, relative: PersonObject, relation_type: RT):
        match relation_type:
            case RT.CHILD | RT.FULL_ADOPTED_CHILD | RT.PARTIAL_ADOPTED_CHILD:
                self.children.append(PersonObject)
                PersonObject.parent.append(self)
                return True
            case RT.SIBLING:
                self.siblings.append(PersonObject)
                PersonObject.siblings.append(self)
                return True
            case RT.PARENT:
                self.parents.append(PersonObject)
                PersonObject.children.append(self)
                return True

        return False


@dataclass
class Testator(Person):
    spouse: list[Spouse] = field(default_factory=lambda: list())

    def add_relative(self, relative: Person, relation_type: RT):
        if not super().add_relative(relative, relation_type):
            self.spouse.append(Spouse(relative, relation_type))


@dataclass
class Relative(Person):
    pass
    # mail_sent: date = None
    # mail_received: date = None
