from django import forms
from django.forms import ModelForm,DateTimeInput,DateInput
from . import models

class StudentForm(forms.Form):
    student_id = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    student_id.widget.attrs.update({'class':'form-control'})
    username.widget.attrs.update({'class':'form-control'})
    password.widget.attrs.update({'class':'form-control'})
    first_name.widget.attrs.update({'class':'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    
    # class Meta:
    #     model = models.Student
    #     fields = ['student_id', 'user']
        