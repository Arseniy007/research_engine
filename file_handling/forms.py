from django import forms
from research_engine.constants import ACCEPTED_UPLOAD_FORMATS, CLASS_


class UploadPaperFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))


class UploadSourceFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "accept": ACCEPTED_UPLOAD_FORMATS,
        "id": "file-field",
        "class": CLASS_,
        "placeholder": "File"})
    )
