from django import forms
from bookshelf.models import Source
from research_engine.constants import CLASS_
from user_management.models import User
from work_space.models import WorkSpace
from .models import Paper


CITATION_STYLES = (("APA", "APA"), ("MLA", "MLA"),)


class NewPaperForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    def save_paper(self, space: WorkSpace, user: User):
        """Save new Paper object"""
        new_paper = Paper(work_space=space, user=user, title=self.cleaned_data["title"])
        new_paper.save()
        return new_paper


class RenamePaperForm(NewPaperForm):
    def set_initial(self, paper_title: str):
        """Pre-populate form fields"""
        self.fields["title"].initial = paper_title
        return self


class ChooseSourcesForm(forms.Form):
    sources = forms.ModelMultipleChoiceField(queryset=Source.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    def set_initials(self, sources):
        """Pre-populate field with all sources in a work space"""
        self.fields["sources"].queryset = sources
        return self
    
