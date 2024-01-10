from django import forms
from .models import Link, WorkSpace
from user_management.models import User


CONFIRMATION = (("Yes", "Yes"), ("No", "No"),)

SOURCES_RECEIVING_OPTIONS = (("copy", "Create New Work Space"), ("download", "Download sources"),)


class NewSpaceForm(forms.Form):
    title = forms.CharField(max_length=50)

    def save_work_space(self, user: User):
        """Save new WorkSpace object"""
        new_work_space = WorkSpace(owner=user, title=self.cleaned_data["title"])
        new_work_space.save()
        return new_work_space


class RenameSpaceForm(forms.Form):
    new_title = forms.CharField(max_length=50)

    def set_initial(self, space: WorkSpace):
        self.fields["new_title"].initial = space.title
        return self
    

    def save_new_title(self, space: WorkSpace) -> WorkSpace:
        space.title = self.cleaned_data["new_title"]
        space.save(update_fields=("title",))
        return space
    

class DeleteSpaceForm(forms.Form):
    confirm = forms.ChoiceField(choices=CONFIRMATION)


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
        """Update text field in Link obj"""
        link.name = self.cleaned_data["name"]
        link.url = self.cleaned_data["url"]
        link.save(update_fields=("name", "url",))
        return link


class ReceiveCodeForm(forms.Form):
    code = forms.CharField(max_length=15)


class ReceiveSourcesForm(forms.Form):
    code = forms.CharField(max_length=15)
    option = forms.ChoiceField(choices=SOURCES_RECEIVING_OPTIONS)
