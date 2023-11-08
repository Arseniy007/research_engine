#import re
from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website

from user_management.models import User
from work_space.models import WorkSpace


EXCLUDED_FIELDS = ("user", "work_space", "file", "real_type", "author", "multiple_authors")


class NewSourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ("title", "year", "link")

    author_last_name = forms.CharField(max_length=40)
    author_first_name = forms.CharField(max_length=40)
    author_second_name = forms.CharField(max_length=40)


    def save_source(self, user: User, space: WorkSpace):

        # deal with authors here!

        # Have another func with re module to fix all possible problems?

        title = self.cleaned_data["title"].strip(". ")

        author_last_name = self.cleaned_data["author_last_name"].strip(". ")
        author_first_name = self.cleaned_data["author_first_name"].strip(". ")
        author_second_name = self.cleaned_data["author_second_name"].strip(". ")

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year, publishing_house = self.cleaned_data["year"].strip(". "), self.cleaned_data["publishing_house"].strip(". ")

        new_book = Book(user=user, work_space=space, title=title, author=author, year=year, publishing_house=publishing_house)
        new_book.save()


class NewBookForm(forms.Form):

    publishing_house = forms.CharField(max_length=30)


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = EXCLUDED_FIELDS


class NewChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = "__all__"
        exclude = EXCLUDED_FIELDS




class NewWebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = "__all__"
        exclude = EXCLUDED_FIELDS
    













class UploadSourceForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))

    
    def save_file(self, source: Source):
       """Save new source-file"""
       source.file = self.cleaned_data["file"]
       source.save(update_fields=("file",))


class AlterSourceForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "multiple_authors", "file"]


    def save_source(self, book: Book):

        params = ("title", "author", "year", "publishing_house", "link")

        # Set new attr if was submitted
        for param in params:
            if self.cleaned_data[param]:
                setattr(book, param, self.cleaned_data[param])

        book.save(update_fields=params)
    

class NewQuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = "__all__"
        exclude = ["source"]

        # TODO qury set of books, articles and websites
    

    def save_quote(self, source: Source):
        """Save new Quote object"""
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()
