from django import forms
from research_engine.constants import CLASS_
from utils.data_cleaning import clean_text_data
from .models import Article, Book, Chapter, Source, Webpage


class SourceTypes:
    book = forms.CharField(widget=forms.HiddenInput(attrs={"value": "book"}))
    article = forms.CharField(widget=forms.HiddenInput(attrs={"value": "article"}))
    chapter = forms.CharField(widget=forms.HiddenInput(attrs={"value": "chapter"}))
    webpage = forms.CharField(widget=forms.HiddenInput(attrs={"value": "webpage"}))


class CommonFields(forms.Form):
    number_of_authors = forms.IntegerField(widget=forms.HiddenInput(attrs={
        "name": "number_of_authors", 
        "class": "final_number_of_authors"})
    )


class BookForm(CommonFields):
    source_type = SourceTypes.book

    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Book title"})
    )

    publishing_house = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "publishing-house-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Publishing House"})
    )

    year = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "book-year-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Publishing year"})
    )


class ArticleForm(CommonFields):
    source_type = SourceTypes.article

    journal_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "journal-title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Journal Title"})
    )

    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "article-title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Article Title"})
    )

    volume = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "volume-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Journal Volume"})
    )

    issue = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "issue-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Journal Issue"})
    )

    pages = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "article-pages-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Pages range"})
    )

    year = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "article-year-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Publishing year"})
    )

    link_to_journal = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "type": "url",
        "id": "link-to-journal-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Link to journal"})
    )


class ChapterForm(CommonFields):
    number_of_chapter_authors = forms.IntegerField(widget=forms.HiddenInput(attrs={
        "name": "number_of_chapter_authors", 
        "class": "final_number_of_chapter_authors"})
    )

    source_type = SourceTypes.chapter

    book_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "book-title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Book Title"})
    )

    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "chapter-title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Chapter Title"})
    )

    publishing_house = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "chapter-publishing-house-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Publishing House"})
    )

    edition = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "edition-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Book Edition"})
    )

    pages = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "chapter-pages-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Pages range"})
    )

    year = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "chapter-year-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Publishing year"})
    )


class WebpageForm(CommonFields):
    source_type = SourceTypes.webpage

    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "page-title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Page Title"})
    )

    website_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "website-title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Website Title"})
    )

    link = forms.URLField(widget=forms.URLInput(attrs={
        "type": "url",
        "id": "page-url-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Webpage url"})
    )

    date = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "id": "date-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Date"})
    )


class AlterBookForm(BookForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Book author"})
    )

    number_of_authors = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def set_initials(self, book: Book):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors",):
                self.fields[field].initial = book.__getattribute__(field)
        return self


class AlterArticleForm(ArticleForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Article author"})
    )

    number_of_authors = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def set_initials(self, article: Article):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors",):
                self.fields[field].initial = article.__getattribute__(field)
        return self


class AlterChapterForm(ChapterForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Book author"})
    )

    book_author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "book-author-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Chapter author"})
    )

    number_of_authors = forms.IntegerField(widget=forms.HiddenInput, required=False)
    number_of_chapter_authors = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def set_initials(self, chapter: Chapter):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors", "number_of_chapter_authors",):
                self.fields[field].initial = chapter.__getattribute__(field)
        return self


class AlterWebpageForm(WebpageForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Webpage author"})
    )

    number_of_authors = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def set_initials(self, webpage: Webpage):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors",):
                self.fields[field].initial = webpage.__getattribute__(field)
        return self


class AddLinkForm(forms.Form):
    link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "type": "url",
        "id": "link-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Link"})
    )

    def set_initials(self, source: Source):
        """Prepopulate link field if it was already uploaded"""
        if source.link:
            self.fields["link"].initial = source.link
        return self


    def save_link(self, source: Source):
        """Checks and saves link for given source"""
        source.link = clean_text_data(self.cleaned_data["link"])
        source.save(update_fields=("link",))


def get_type_of_source_form(data, alter_source=False):
    """
    Based on form hidden input get obj type and return either obj-creation or obj-alter form.
    data arg. = request.POST
    """
    if "book" in data["source_type"]:
        if alter_source:
            return AlterBookForm(data)
        return BookForm(data)
    elif "article" in data["source_type"]:
        if alter_source:
            return AlterArticleForm(data)
        return  ArticleForm(data)
    elif "chapter" in data["source_type"]:
        if alter_source:
            return AlterChapterForm(data)
        return ChapterForm(data)
    elif "webpage" in data["source_type"]:
        if alter_source:
            return AlterWebpageForm(data)
        return WebpageForm(data)
    else:
        return None


def get_and_set_alter_form(source: Source):
    """Based on given source type get form and prepopulate it with source info"""
    source_type = source.cast()
    match source_type:
        case Book():
            return AlterBookForm().set_initials(source.book)
        case Article():
            return AlterArticleForm().set_initials(source.article)
        case Chapter():
            return AlterChapterForm().set_initials(source.chapter)
        case Webpage():
            return AlterWebpageForm().set_initials(source.webpage)
        case _:
            return None
