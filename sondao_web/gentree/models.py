from django.db import models
from django.core.validators import RegexValidator
from sondao.logic.DocumentType import DocumentType
from sondao.logic.RelationTypes import RelationTypes


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Person(models.Model):
    pesel_validator = RegexValidator(regex=r"\d{11}", message="Pesel must have 11 digits")

    name = models.CharField("Person first name", max_length=50)
    surname = models.CharField("Person surname", max_length=50)
    pesel = models.CharField('Person pesel', max_length=11, validators=[pesel_validator], unique=True, null=True)
    phone_number = models.CharField('Person phone number', max_length=15,
                                    null=True)  # TODO chekc other countries. Maybe add validator
    home_address = models.CharField('Person home address', max_length=50, null=True)
    birthday = models.DateField("Person birthday", null=True)
    is_testator = models.BooleanField("Is person a testator", default=False)
    death_date = models.DateField("Person death date", null=True)
    want_inherit = models.BooleanField("Is person eager to inherit", default=False)
    supposed_death_notification = models.DateField("Person supposed date notification", null=True)
    proxy = models.CharField("Juvenile proxy", null=True)
    notes = models.TextField("Notes for person", null=True)
    receive_confirmation_place = models.CharField("place_of_receive_confirmation", null=True)


class Documents(models.Model):
    doc_types = [x.value for x in RelationTypes]

    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.CharField("Document type", max_length=30, choices=doc_types)
    code = models.CharField("Document code", max_length=30)
    note = models.CharField("Document notes", max_length=30)
    date = models.DateField("Document date", null=True)


class Relations(models.Model):
    relation_types = [x.value for x in DocumentType]

    person1 = models.ForeignKey(Person, on_delete=models.CASCADE)
    person2 = models.ForeignKey(Person, on_delete=models.CASCADE)
    relation = models.CharField("Document type", max_length=30, choices=relation_types)
