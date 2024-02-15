from django import forms
from research_engine.constants import ACCEPTED_UPLOAD_FORMATS, CLASS_


class UploadPaperFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "accept": ACCEPTED_UPLOAD_FORMATS,
        "id": "file-field",
        "class": CLASS_,
        "placeholder": "File"})
    )

    commit_text = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "type": "text",
        "id": "commit-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Commit text"
    }))


class UploadSourceFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "accept": ACCEPTED_UPLOAD_FORMATS,
        "id": "file-field",
        "class": CLASS_,
        "placeholder": "File"})
    )
