from django import forms
from .models import Person
from bootstrap_modal_forms.forms import BSModalModelForm

class PersonForm(BSModalModelForm):
    class Meta:
        model = Person
        fields = '__all__'
