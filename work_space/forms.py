from django import forms
from research_engine.constants import CLASS_
from .models import WorkSpace


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
