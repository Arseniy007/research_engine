from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website

from user_management.models import User
from work_space.models import WorkSpace


CHOICES = (("Book", "Book"), ("Article", "Article"), ("Chapter", "Chapter"), ("Website", "Website"),)
#COMMON_FIELDS = ("title", "author_last_name", "author_first_name", "author_second_name", "year", "link")


class FieldClass:

    common_fields = "common_fields"
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    website_class = "website"


class CommonFields(forms.Form):

    def __init__(self):

        self.title = forms.CharField()
        self.author_last_name = forms.CharField()
        self.author_first_name = forms.CharField()
        self.author_second_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))
        self.year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
        self.link = forms.CharField(widget=forms.TextInput(attrs={"required": False}))


class BookForm(forms.Form):

    book_title = CommonFields().title
    author_last_name = CommonFields().author_last_name
    author_first_name = CommonFields().author_first_name
    author_second_name = CommonFields().author_second_name
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = CommonFields().year
    link = CommonFields().link


class ArticleForm(forms.Form):

    journal_title = CommonFields().title
    article_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    author_last_name = CommonFields().author_last_name
    author_first_name = CommonFields().author_first_name
    author_second_name = CommonFields().author_second_name
    volume_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    journal_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    is_electronic = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))


class ChapterForm(forms.Form):

    chapter_title = CommonFields().title
    chapter_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    book_title = CommonFields().title
    book_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))


class WebsiteForm(forms.Form):

    website_title = CommonFields().title
    has_author = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": FieldClass.website_class}))
    page_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    page_title = CommonFields().title
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))
