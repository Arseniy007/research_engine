from django import forms
from .models import Comment, Link, Note
from work_space.models import WorkSpace
from user_management.models import User
from utils.verification import check_link


class NewCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_comment(self, space: WorkSpace, user: User) -> Comment:
        """Save new Comment object"""
        new_comment = Comment(work_space=space, user=user, text=self.cleaned_data["text"])
        new_comment.save()
        return new_comment


class AlterCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def set_initial(self, comment: Comment):
        self.fields["text"].initial = comment.text
        return self


    def save_altered_comment(self, comment: Comment) -> Comment:
        """Update text field in Comment obj"""
        comment.text = self.cleaned_data["text"]
        comment.save(update_fields=("text",))
        return comment


class NewNoteForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea())

    def save_note(self, space: WorkSpace, user: User) -> Note:
        """Save new Note object"""
        new_note = Note(work_space=space, user=user, title=self.cleaned_data["title"], text=self.cleaned_data["text"])
        new_note.save()
        return new_note


class AlterNoteForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def set_initial(self, note: Note):
        self.fields["text"].initial = note.text
        return self


    def save_altered_note(self, note: Note) -> Note:
        """Update text field in Comment obj"""
        note.text = self.cleaned_data["text"]
        note.save(update_fields=("text",))
        return note


class NewLinkForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()

    def save_link(self, space: WorkSpace, user: User) -> Link:
        """Save new Link object"""
        new_link = Link(work_space=space, user=user, name=self.cleaned_data["name"], url=self.cleaned_data["url"])
        new_link.save()
        return new_link


class AlterLinkForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()

    def set_initial(self, link: Link):
        self.fields["name"].initial = link.name
        self.fields["url"].initial = link.url
        return self


    def save_altered_link(self, link: Link) -> Link:
        """Update text field in Comment obj"""
        link.name = self.cleaned_data["name"]
        link.url = self.cleaned_data["url"]
        link.save(update_fields=("name", "url",))
        return link
    


# TODO: check link?