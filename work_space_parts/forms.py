from django import forms
from .models import Comment, Link, Note
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

    def set_initial(self, comment: Comment):
        self.fields["text"].initial = comment.text
        return self


    def save_altered_comment(self, comment: Comment):
        """Update text field in Comment obj"""
        comment.text = self.cleaned_data["text"]
        return comment.save(update_fields=("text",))


class NewNoteForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def save_note(self, space: WorkSpace, user: User):
        """Save new Note object"""
        new_note = Note(work_space=space, user=user, text=self.cleaned_data["text"])
        return new_note.save()


class AlterNoteForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())

    def set_initial(self, note: Note):
        self.fields["text"].initial = note.text
        return self


    def save_altered_comment(self, note: Note):
        """Update text field in Comment obj"""
        note.text = self.cleaned_data["text"]
        return note.save(update_fields=("text",))


class NewLinkForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()

    def save_link(self, space: WorkSpace, user: User):
        """Save new Link object"""
        new_link = Link(work_space=space, user=user, name=self.cleaned_data["name"], url=self.cleaned_data["url"])
        return new_link.save()


class AlterLinkForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()

    def set_initial(self, link: Link):
        self.fields["name"].initial = link.name
        self.fields["url"].initial = link.url
        return self


    def save_altered_comment(self, link: Link):
        """Update text field in Comment obj"""
        link.name = self.cleaned_data["name"]
        link.url = self.cleaned_data["url"]
        return link.save(update_fields=("name", "url",))
    


# TODO: check link?