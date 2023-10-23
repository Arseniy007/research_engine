from django import forms

from .models import Paper, PaperVersion


class NewPaperForm(forms.Form):


    title = forms.CharField(max_length=50)
    file = forms.FileField()

