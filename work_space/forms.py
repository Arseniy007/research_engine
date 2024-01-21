from django import forms
from .models import Link, WorkSpace
from research_engine.constants import _CLASS


SOURCES_RECEIVING_OPTIONS = (("copy", "Create New Work Space"), ("download", "Download sources"),)


class NewSpaceForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Workspace title"})
    )


class RenameSpaceForm(forms.Form):
    new_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    def set_initial(self, space: WorkSpace):
        self.fields["new_title"].initial = space.title
        return self
    

    def save_new_title(self, space: WorkSpace) -> WorkSpace:
        space.title = self.cleaned_data["new_title"]
        space.save(update_fields=("title",))
        return space


class NewLinkForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "name-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    url = forms.URLField()

    def save_link(self, space: WorkSpace) -> Link:
        """Save new Link object"""
        new_link = Link(work_space=space, name=self.cleaned_data["name"], url=self.cleaned_data["url"])
        new_link.save()
        return new_link


class ReceiveInvitationForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "code-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Invitation code"})
    )


class ReceiveSourcesForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "sources-code-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    # Maybe make it as a part of html?
    option = forms.ChoiceField(choices=SOURCES_RECEIVING_OPTIONS, widget=forms.RadioSelect(attrs={
        #"class": "form-check-input",
    }))
