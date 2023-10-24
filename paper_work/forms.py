from django import forms

#from .models import Paper, PaperVersion


class NewPaperForm(forms.Form):

    title = forms.CharField(max_length=50)


class NewPaperVersionForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ".pdf, .doc, .docx"}))