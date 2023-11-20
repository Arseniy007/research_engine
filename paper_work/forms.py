from django import forms
from .models import Paper
from user_management.models import User
from work_space.models import WorkSpace


class NewPaperForm(forms.Form):
    title = forms.CharField(max_length=50)


    def save_paper(self, space: WorkSpace, user: User):
        """Save new Paper object"""
        new_paper = Paper(work_space=space, user=user, title=self.cleaned_data["title"])
        new_paper.save()
        return new_paper


class RenamePaperForm(forms.Form):
    title = forms.CharField(max_length=50)


    def save_new_name(self, paper: Paper):
        """Updates title of Paper object"""
        field = "title"
        paper.title = self.cleaned_data[field]
        paper.save(update_fields=(field,))
