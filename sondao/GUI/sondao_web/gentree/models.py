from django.db import models
from django.core.validators import RegexValidator
from sondao.logic.DocumentType import DocumentType
from sondao.logic.RelationTypes import RelationTypes


class Person(models.Model):
    pesel_validator = RegexValidator(regex=r"\d{11}", message="Pesel must have 11 digits")

    name = models.CharField("Person first name", max_length=30)
    surname = models.CharField("Person surname", max_length=30)
    pesel = models.CharField('Person pesel', max_length=11, unique=True, null=True, blank=True)
    phone_number = models.CharField('Person phone number', max_length=15, blank=True, null=True)
    home_address = models.CharField('Person home address', max_length=50, null=True, blank=True)
    birthday = models.DateField("Person birthday", null=True, blank=True)
    is_testator = models.BooleanField("Is person a testator", default=False)
    death_date = models.DateField("Person death date", null=True, blank=True)
    want_inherit = models.BooleanField("Is person eager to inherit", default=False)
    supposed_death_notification = models.DateField("Person supposed date notification", null=True, blank=True)
    proxy = models.CharField("Juvenile proxy", null=True, max_length=60, blank=True)
    notes = models.TextField("Notes for person", null=True, blank=True)
    receive_confirmation_place = models.CharField("Place of received confirmation", null=True, max_length=30,
                                                  blank=True)

    def __repr__(self):
        return f"{self.name} {self.surname} [{'not ' if not self.is_testator else ''}testator]"

    def get_relatives_pk(self):
        relatives_pk = list()
        objects = Relation.objects.filter(first_relative=self.pk).values()
        for obj in objects:
            relatives_pk.append(obj['pk'])

        objects = Relation.objects.filter(second_relative=self.pk).values()
        for obj in objects:
            relatives_pk.append(obj['pk'])

        return relatives_pk


class Document(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.CharField("Document type", max_length=30, choices=DocumentType.choices())
    code = models.CharField("Document code", max_length=30)
    note = models.CharField("Document notes", max_length=30)
    date = models.DateField("Document date", null=True, blank=True)

    def __repr__(self):
        return f"{self.type} of {str(Person.objects.get(pk=self.person_id))}"


class Relation(models.Model):
    first_relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="first_relative")
    second_relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="second_relative")
    relation = models.CharField("Relation type", max_length=30, choices=RelationTypes.choices())

    def __repr__(self):
        second_relative = Person.objects.get(pk=self.second_relative)
        first_relative = Person.objects.get(pk=self.first_relative)
        return f"{second_relative} is {self.type} for {first_relative}"
