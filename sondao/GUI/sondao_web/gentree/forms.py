from django import forms
from .models import Person, Relation, Document

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
        widgets = {'date': forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"))}
