from django.db import models
from django.core.validators import RegexValidator
from sondao.logic.DocumentType import DocumentType
from sondao.logic.RelationTypes import RelationTypes


class Person(models.Model):
    pesel_validator = RegexValidator(regex=r"\d{11}", message="Pesel must have 11 digits")

    name = models.CharField("Person first name", max_length=30)
    surname = models.CharField("Person surname", max_length=30)
    pesel = models.CharField('Person pesel', max_length=11, validators=[pesel_validator], unique=True, null=True)
    phone_number = models.CharField('Person phone number', max_length=15,
                                    null=True)  # TODO check other countries. Maybe add validator
    home_address = models.CharField('Person home address', max_length=50, null=True)
    birthday = models.DateField("Person birthday", null=True)
    is_testator = models.BooleanField("Is person a testator", default=False)
    death_date = models.DateField("Person death date", null=True)
    want_inherit = models.BooleanField("Is person eager to inherit", default=False)
    supposed_death_notification = models.DateField("Person supposed date notification", null=True)
    proxy = models.CharField("Juvenile proxy", null=True, max_length=60)
    notes = models.TextField("Notes for person", null=True)
    receive_confirmation_place = models.CharField("Place of received confirmation", null=True, max_length=30)


class Document(models.Model):
    doc_types = [(x.value, DocumentType(x.value)) for x in DocumentType]

    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.CharField("Document type", max_length=30, choices=doc_types)
    code = models.CharField("Document code", max_length=30)
    note = models.CharField("Document notes", max_length=30)
    date = models.DateField("Document date", null=True)


class Relation(models.Model):
    first_relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="first_relative")
    second_relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="second_relative")
    relation = models.CharField("Document type", max_length=30, choices=RelationTypes.choices())
