from django import forms

from research_engine.settings import ACCEPTED_PAPER_FORMATS


class NewPaperForm(forms.Form):
    
    title = forms.CharField(max_length=50)


class RenamePaperForm(forms.Form):

    new_title = forms.CharField(max_length=50)

