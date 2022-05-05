from django import forms


class PersonForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=30)
    name = forms.CharField(label="Person first name", max_length=30)
    surname = forms.CharField(label="Person surname", max_length=30)
    pesel = forms.CharField(label='Person pesel', max_length=11, required=False)
    phone_number = forms.CharField(label='Person phone number', max_length=15, required=False)
    home_address = forms.CharField(label='Person home address', max_length=50, required=False)
    birthday = forms.DateField(label="Person birthday", required=False)
    is_testator = forms.BooleanField(label="Is person a testator", required=False)
    death_date = forms.DateField(label="Person death date", required=False)
    want_inherit = forms.BooleanField(label="Is person eager to inherit", required=False)
    supposed_death_notification = forms.DateField(label="Person supposed date notification", required=False)
    proxy = forms.CharField(label="Juvenile proxy", required=False, max_length=60)
    notes = forms.CharField(label="Notes for person", required=False)
    receive_confirmation_place = forms.CharField(label="Place of received confirmation", required=False, max_length=30)
