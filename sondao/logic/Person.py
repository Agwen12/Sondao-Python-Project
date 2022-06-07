from sondao.logic.PersonalInfo import PersonalInfo
from sondao.logic.RelationTypes import RelationTypes
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import TypeVar

PersonObject = TypeVar("PersonObject")
Spouse = namedtuple("Spouse", ["person", "relation"])


@dataclass
class GenericPerson(ABC):
    personal_info: PersonalInfo

    @abstractmethod
    def add_relative(self, relative: PersonObject, relation_type: RelationTypes):
        pass


@dataclass
class Person(GenericPerson):
    internal_id: int
    children: list[GenericPerson] = field(default_factory=lambda: list())
    siblings: list[GenericPerson] = field(default_factory=lambda: list())
    parents: list[GenericPerson] = field(default_factory=lambda: list())

    def add_relative(self, relative: PersonObject, relation_type: RelationTypes):
        match relation_type:
            case RelationTypes.CHILD | RelationTypes.FULL_ADOPTED_CHILD | RelationTypes.PARTIAL_ADOPTED_CHILD:
                self.children.append(relative)
                relative.parents.append(self)
                return True
            case RelationTypes.SIBLING:
                self.siblings.append(relative)
                relative.siblings.append(self)
                return True
            case RelationTypes.PARENT:
                self.parents.append(relative)
                relative.children.append(self)
                return True

        return False


@dataclass
class Testator(Person):
    spouse: list[Person] = field(default_factory=lambda: list())

    def add_relative(self, relative: Person, relation_type: RelationTypes):
        if not super().add_relative(relative, relation_type):
            self.spouse.append(relative)


@dataclass
class Relative(Person):
    pass
