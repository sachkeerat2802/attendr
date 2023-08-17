from django import forms
from .models import User
from django.forms import ModelForm


class RegisterUserCreationForm(ModelForm):
    uid = forms.IntegerField(label='PRN')

    class Meta:
        model = User
        fields = ['name', 'email', 'uid']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'uid': 'PRN',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Sachkeerat Singh'
        self.fields['email'].widget.attrs['placeholder'] = 'sas2121155@sicsr.ac.in'
        self.fields['uid'].widget.attrs['placeholder'] = '21030121155'

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'registration-input'})


class RegisterStaffCreationForm(ModelForm):
    uid = forms.IntegerField(label='Employee No.')

    class Meta:
        model = User
        fields = ['name', 'email', 'uid']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'uid': 'Employee No.',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterStaffCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = "Sachkeerat Singh"
        self.fields['email'].widget.attrs['placeholder'] = "sas2121155@sicsr.ac.in"
        self.fields['uid'].widget.attrs['placeholder'] = "123456"

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'registration-input'})
