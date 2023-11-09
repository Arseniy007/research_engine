#import re
from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website

from user_management.models import User
from work_space.models import WorkSpace


CHOICES = ((Book, "Book"),(Article, "Article"), (Chapter, "Chapter"), (Website, "Website"),)


class FieldClass:

    all_classes = "book article chapter website"
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    website_class = "website"


class NewSourceForm(forms.Form):

    source_type = forms.ChoiceField(choices=CHOICES)

    # Cross-type fileds
    title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.all_classes}))
    author_last_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.all_classes}))
    author_first_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.all_classes}))
    author_second_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.all_classes}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.all_classes}))
    link = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.all_classes}))

    # Book field:
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))

    # Article fields:
    journal_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    volume_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    journal_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    is_electronic = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))

    # Chapter fields:
    chapter_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    chapter_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))

    # Website fields:
    has_author = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": FieldClass.website_class}))
    website_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))


    def save_source(self, user: User, space: WorkSpace):

        # deal with authors here!
        # Have another func with re module to fix all possible problems?

        # Need to be able to figure out whoch type was selected and then create it and only it



        title = self.cleaned_data["title"].strip(". ")

        author_last_name = self.cleaned_data["author_last_name"].strip(". ")
        author_first_name = self.cleaned_data["author_first_name"].strip(". ")
        author_second_name = self.cleaned_data["author_second_name"].strip(". ")

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year, publishing_house = self.cleaned_data["year"].strip(". "), self.cleaned_data["publishing_house"].strip(". ")

        new_book = Book(user=user, work_space=space, title=title, author=author, year=year, publishing_house=publishing_house)
        new_book.save()
















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
