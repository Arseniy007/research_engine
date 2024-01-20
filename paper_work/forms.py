from django import forms
from bookshelf.models import Source
from .models import Paper
from user_management.models import User
from work_space.models import WorkSpace


_CLASS = "form-control"

CITATION_STYLES = (("APA", "APA"), ("MLA", "MLA"),)


class NewPaperForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    def save_paper(self, space: WorkSpace, user: User):
        """Save new Paper object"""
        new_paper = Paper(work_space=space, user=user, title=self.cleaned_data["title"])
        new_paper.save()
        return new_paper


class RenamePaperForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    def set_initial(self, paper: Paper):
        self.fields["title"].initial = paper.title
        return self

    def save_new_name(self, paper: Paper) -> Paper:
        """Updates title of Paper object"""
        paper.title = self.cleaned_data["title"]
        paper.save(update_fields=("title",))
        return paper


class ChooseSourcesForm(forms.Form):
    sources = forms.ModelMultipleChoiceField(queryset=Source.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    def set_initials(self, sources):
        """Pre-populate field with all sources in a work space"""
        self.fields["sources"].queryset = sources
        return self
    

class CitationStyleForm(forms.Form):
    citation_style = forms.ChoiceField(choices=CITATION_STYLES, widget=forms.Select(attrs={"class": _CLASS}))

    def save_citation_style(self, paper: Paper):
        "Update citation_style field in Workspace obj"
        paper.citation_style = self.cleaned_data["citation_style"]
        return paper.save(update_fields=("citation_style",))
