from django import forms

from research_engine.settings import ACCEPTED_PAPER_FORMATS


class NewPaperVersionForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_PAPER_FORMATS}))
