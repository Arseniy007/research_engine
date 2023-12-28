from django import forms
from .models import PaperFile
from paper_work.models import Paper
from research_engine.constants import ACCEPTED_UPLOAD_FORMATS
from user_management.models import User


class UploadPaperFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))

    def save_new_file(self, paper: Paper, user: User):
        """Saves new PaperFile object"""
        new_file = PaperFile(user=user, paper=paper, file=self.cleaned_data["file"])
        new_file.save()


class UploadSourceFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))
