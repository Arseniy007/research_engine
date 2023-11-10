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

    title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    author_last_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    author_first_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    author_second_name = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
    link = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))


class SourceTypeForm(forms.Form):

    source_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={"required": True}))


class BookForm(CommonFields):

    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))


class ArticleForm(CommonFields):

    journal_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    volume_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    journal_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    is_electronic = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))


class ChapterForm(CommonFields):

    chapter_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    chapter_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))


class WebsiteForm(CommonFields):

    has_author = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": FieldClass.website_class}))
    website_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))


