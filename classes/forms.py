from django import forms
from django.forms import ModelForm
from .models import Class, Lecture, Attendance


class ClassForm(ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Class
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = "Intro to Data Structures"

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class LectureForm(ModelForm):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}, format='%d-%m-%YT%H:%M'))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}, format='%d-%m-%YT%H:%M'))

    class Meta:
        model = Lecture
        fields = ['no', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)

        self.fields['no'].widget.attrs['placeholder'] = "1"

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
