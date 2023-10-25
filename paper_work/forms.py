from django import forms

#from .models import Paper, PaperVersion


class NewPaperForm(forms.Form):
    
    title = forms.CharField(max_length=50)


class NewPaperVersionForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ".pdf, .doc, .docx"}))


class RenamePaperForm(forms.Form):

    new_title = forms.CharField(max_length=50)


class RenameFileForm(forms.Form):

    new_title = forms.CharField(max_length=50)

