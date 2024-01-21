from django import forms
from bookshelf.models import Source
from .models import PaperFile, SourceFile
from paper_work.models import Paper
from research_engine.constants import ACCEPTED_UPLOAD_FORMATS, _CLASS
from user_management.models import User


class UploadPaperFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))

    def save_new_paper_file(self, paper: Paper, user: User):
        """Create and save new PaperFile obj"""
        new_file = PaperFile(user=user, paper=paper, file=self.cleaned_data["file"])
        new_file.save()


class UploadSourceFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "accept": ACCEPTED_UPLOAD_FORMATS,
        "id": "file-field",
        "class": _CLASS,
        "placeholder": "File"})
    )

    def save_new_source_file(self, source: Source):
        """Create and save new SourceFile obj"""
        new_file = SourceFile(source=source, file=self.cleaned_data["file"])
        new_file.save()
