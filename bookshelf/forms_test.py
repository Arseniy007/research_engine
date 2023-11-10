#import re
from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website

from user_management.models import User
from work_space.models import WorkSpace


CHOICES = (("Book", "Book"), ("Article", "Article"), ("Chapter", "Chapter"), ("Website", "Website"),)
COMMON_FIELDS = ("title", "author_last_name", "author_first_name", "author_second_name", "year", "link")


def clean_text_data(data):

    return data.strip("., ")


class FieldClass:
    common_fields = "common_fields"
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    website_class = "website"


class NewSourceForm(forms.Form):

    source_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={"required": False}))

    # Cross-type fields
    title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    author_last_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    author_first_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    author_second_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    link = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))

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

        source_type = self.cleaned_data["source_type"]
        if not source_type:
            return False

        common_info: dict = {}

        for field in COMMON_FIELDS:
            common_info[field] = clean_text_data(self.cleaned_data[field])


        common_info["author"] = f"{common_info['author_last_name']} {'author_first_name'} {'author_second_name'}"


        # Here call other func (or methods!)
        match source_type:
            case "Book":
                self.save_book(user, space, common_info)
            case "Article":
                self.save_article(user, space, common_info)
            case "Chapter":
                self.save_chapter(user, space, common_info)
            case "Website":
                self.save_website(user, space, common_info)
            case _:
                print("error")

                
    def save_book(self, user: User, space: WorkSpace, common_info: dict):
        # TODO

        publishing_house = clean_text_data(self.cleaned_data["publishing_house"])

        new_book = Book(user=user, work_space=space, 
                        title=common_info["title"], 
                        author=common_info["author"], 
                        year=common_info["year"], publishing_house=publishing_house)
        new_book.save()
        
        return print("book")


    def save_article(self, user: User, space: WorkSpace, common_info: dict):
        # TODO
        return print("article")
        

    def save_chapter(self, user: User, space: WorkSpace, common_info: dict):
        # TODO
        return print("chapter")


    def save_website(self, user: User, space: WorkSpace, common_info: dict):
        # TODO
        return print("website")









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

    # Probably gonna change that later


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


class SourceTypeForm(forms.Form):
    '''Do I need it???'''

    source_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={"required": True}))