from dataclasses import dataclass, field
from typing import List, TypeVar
from datetime import date
from abc import ABC, abstractmethod

from PersonalInfo import PersonalInfo
from RelationTypes import RelationTypes as RT

PersonObject = TypeVar("PersonObject")

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
    spouse: list[GenericPerson] = field(default_factory=lambda: list())

    def add_relative(self, relative: Person, relation_type: RT):
        if not super().add_relative(relative, relation_type):
            self.spouse.append(relative)


@dataclass
class Relative(Person):
    mail_sent: date = None
    mail_received: date = None
