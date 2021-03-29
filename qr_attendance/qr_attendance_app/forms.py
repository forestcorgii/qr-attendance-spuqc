from django import forms
from django.forms import ModelForm,DateTimeInput,DateInput
from . import models

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        widget=forms.FileInput(attrs={'class':'form-control','style':'height:3em'})
    )
