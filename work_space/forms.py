from django import forms
from .models import WorkSpace, Comment
from user_management.models import User


class NewWorkSpaceForm(forms.Form):
    title = forms.CharField(max_length=50)

    def save_work_space(self, user: User):
        """Sace new WorkSpace object"""
        new_work_space = WorkSpace(owner=user, title=self.cleaned_data["title"])
        new_work_space.save()
        return new_work_space


class RenameWorkSpaceForm(forms.Form):
    new_title = forms.CharField(max_length=50)

    def set_initial(self, space: WorkSpace):
        self.fields["new_title"].initial = space.title
        return self
    

    def save_new_title(self, space: WorkSpace):
        space.title = self.cleaned_data["new_title"]
        return space.save(update_fields=("title",))


class ReceiveInvitationForm(forms.Form):
    code = forms.CharField(max_length=15)


class NewCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_comment(self, space: WorkSpace, user: User):
        """Save new Comment object"""
        new_comment = Comment(work_space=space, user=user, text=self.cleaned_data["text"])
        new_comment.save()


class AlterCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_altered_comment(self, comment: Comment):
        """Update text field in Comment obj"""
        comment.text = self.cleaned_data["text"]
        comment.save(update_fields=("text",))
