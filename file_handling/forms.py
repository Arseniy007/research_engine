from django import forms
from .models import PaperVersion
from paper_work.models import Paper
from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from user_management.models import User


class NewPaperVersionForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))

    def save_new_file(self, paper: Paper, user: User):
        """Saves new PaperVersion object"""
        new_file = PaperVersion(user=user, paper=paper, file=self.cleaned_data["file"])
        new_file.save()
