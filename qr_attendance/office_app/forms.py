from django import forms
from django.forms import ModelForm
from . import models

class EventForm(forms.ModelForm):
    # event_datetime = forms.DateTimeField(input_formats=['%Y-%m-%dT%H%M',],widget=DateInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local','class':'form-control'}))
    class Meta:
        model = models.Event
        fields = ['id','office','location','name','event_datetime_from','event_datetime_to','description','attendees']
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_datetime_from':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local','class':'form-control'}),
            'event_datetime_to':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local','class':'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),            
            'office': forms.Select(attrs={'class': 'form-control'}),            
            'description': forms.Textarea(attrs={'class': 'form-control','style':'height:5em'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control'}),            
        }


