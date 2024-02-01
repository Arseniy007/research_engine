from django import forms
from research_engine.constants import CLASS_
from .models import Link, WorkSpace


class NewSpaceForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "width": "100%",
        "placeholder": "Workspace title"})
    )


class RenameSpaceForm(NewSpaceForm):

    def set_initial(self, space: WorkSpace):
        self.fields["title"].initial = space.title
        return self
    

class NewLinkForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "name-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Name"})
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
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Invitation code"})
    )


class ReceiveSourcesForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "sources-code-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )
