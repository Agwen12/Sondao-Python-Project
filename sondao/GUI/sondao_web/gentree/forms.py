from django import forms
from .models import Person, Relation, Document
import datetime


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class RelationFrom(forms.ModelForm):
    class Meta:
        model = Relation
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
        widgets = {
            'date': forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                years=range(datetime.date.today().year - 100, datetime.date.today().year + 1)
            )
        }
