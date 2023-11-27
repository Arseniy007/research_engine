from django import forms
from .models import Comment, WorkSpace
from user_management.models import User


CITATION_STYLES = (("APA", "APA"), ("MLA", "MLA"), ("APA & MLA", "APA & MLA"),)


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
        return new_comment.save()


class AlterCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_altered_comment(self, comment: Comment):
        """Update text field in Comment obj"""
        comment.text = self.cleaned_data["text"]
        return comment.save(update_fields=("text",))


class CitationStyleForm(forms.Form):
    citation_style = forms.ChoiceField(choices=CITATION_STYLES)

    def save_citation_style(self, space: WorkSpace):
        "Update citation_style field in Workspace obj"
        space.citation_style = self.cleaned_data["citation_style"]
        return space.save(update_fields=("citation_style",))
