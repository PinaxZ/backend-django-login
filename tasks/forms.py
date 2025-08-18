from django.forms import ModelForm
from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category' ,'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Adjunte un nombre a su solicitud"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Describa su solicitud"}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input', 'placeholder':"Describa su solicitud"}), 
        }




        
