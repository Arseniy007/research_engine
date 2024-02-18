from django import forms
from bookshelf.models import Source
from research_engine.constants import CLASS_


class NewPaperForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )


class RenamePaperForm(NewPaperForm):
    def set_initial(self, paper_title: str):
        """Pre-populate form fields"""
        self.fields["title"].initial = paper_title
        return self


class ChooseSourcesForm(forms.Form):
    sources = forms.ModelMultipleChoiceField(queryset=Source.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    def set_initials(self, sources):
        """Pre-populate field with all sources in a workspace"""
        self.fields["sources"].queryset = sources
        return self
