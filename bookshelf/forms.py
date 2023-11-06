from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Book

from user_management.models import User
from work_space.models import WorkSpace


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "author", "multiple_authors", "file"]


    author_last_name = forms.CharField(max_length=40)
    author_first_name = forms.CharField(max_length=40)
    author_second_name = forms.CharField(max_length=40)


    def save_form(self, user: User, space: WorkSpace):

        # deal with authors here!

        # Have another func with re module to fix all possible problems?

        title = self.cleaned_data["title"]

        author_last_name = self.cleaned_data["author_last_name"]
        author_first_name = self.cleaned_data["author_first_name"]
        author_second_name = self.cleaned_data["author_second_name"]

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year, publishing_house = self.cleaned_data["year"], self.cleaned_data["publishing_house"]

        new_book = Book(user=user, work_space=space, title=title, author=author, year=year, publishing_house=publishing_house)
        new_book.save()








class UploadBookForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))


class AlterBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "multiple_authors"]


    def save_form(self, book: Book):

        params = ("title", "author", "year", "publishing_house", "link")

        # Set new attr if was submitted
        for param in params:
            if self.cleaned_data[param]:
                setattr(book, param, self.cleaned_data[param])

        book.save(update_fields=params)
    

"""
class NewQuoteForm(forms.ModelForm):
    class Meta:
        model = ""
        fields = "__all__"
        exclude = []
    
     # add exsta fields here
"""
