from django import forms
from .models import Comment
from work_space.models import WorkSpace
from user_management.models import User


class NewCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_comment(self, space: WorkSpace, user: User):
        """Save new Comment object"""
        new_comment = Comment(work_space=space, user=user, text=self.cleaned_data["text"])
        return new_comment.save()


class AlterCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_altered_comment(self, comment: Comment):
        """Update text field in Comment obj"""
        comment.text = self.cleaned_data["text"]
        return comment.save(update_fields=("text",))
