from django.forms import ModelForm
from django import forms
from .models import UserProfile, StaffProfile


class UserProfileForm(ModelForm):
    image = forms.ImageField(label="Choose profile image", required=False, error_messages={
        'invalid': ("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['prn', 'name', 'email', 'course', 'phone', 'image', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['prn'].disabled = True
        self.fields['name'].disabled = True
        self.fields['email'].disabled = True

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'registration-input'})


class StaffProfileForm(ModelForm):
    image = forms.ImageField(label="Choose profile image", required=False, error_messages={
        'invalid': ("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = StaffProfile
        fields = ['empno', 'name', 'email', 'phone', 'image', 'bio']

    def __init__(self, *args, **kwargs):
        super(StaffProfileForm, self).__init__(*args, **kwargs)
        self.fields['empno'].disabled = True
        self.fields['name'].disabled = True
        self.fields['email'].disabled = True

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'registration-input'})
