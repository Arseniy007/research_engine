from django import forms
from .models import Article, Book, Chapter, Endnote, Quote, Source, Webpage
from research_engine.constants import ACCEPTED_UPLOAD_FORMATS
from utils.verification import check_link


_CLASS = "form-control"

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
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Book title"})
    )

    publishing_house = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "publishing-house-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Publishing House"})
    )

    year = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "book-year-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Publishing year"})
    )


class ArticleForm(CommonFields):
    source_type = SourceTypes.article

    journal_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "journal-title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Journal Title"})
    )

    article_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "article-title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Article Title"})
    )

    volume = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "volume-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Journal Volume"})
    )

    issue = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "issue-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Journal Issue"})
    )

    pages = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "article-pages-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Pages range"})
    )

    link_to_journal = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "type": "url",
        "id": "link-to-journal-field",
        "class": _CLASS,
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
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Book Title"})
    )

    chapter_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "chapter-title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Chapter Title"})
    )

    publishing_house = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "chapter-publishing-house-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Publishing House"})
    )

    edition = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "edition-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Book Edition"})
    )

    pages = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "chapter-pages-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Pages range"})
    )

    year = forms.IntegerField(widget=forms.NumberInput(attrs={
        "type": "number",
        "id": "chapter-year-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Publishing year"})
    )


class WebpageForm(CommonFields):
    source_type = SourceTypes.webpage

    page_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "page-title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Page Title"})
    )

    website_title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "website-title-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Website Title"})
    )

    page_url = forms.URLField(widget=forms.URLInput(attrs={
        "type": "url",
        "id": "page-url-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Webpage url"})
    )

    date = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "id": "date-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Date"})
    )


class AlterBookForm(BookForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Book author"})
    )

    def set_initials(self, book: Book):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors",):
                self.fields[field].initial = book.__getattribute__(field)
        return self


class AlterArticleForm(ArticleForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Article author"})
    )

    def set_initials(self, article: Article):
        for field in self.fields:
            if field != "source_type":
                self.fields[field].initial = article.__getattribute__(field)
        return self


class AlterChapterForm(ChapterForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Book author"})
    )

    chapter_author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Chapter author"})
    )

    def set_initials(self, chapter: Chapter):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors",):
                self.fields[field].initial = chapter.__getattribute__(field)
        return self


class AlterWebpageForm(WebpageForm):
    webpage_author = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "author-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Webpage author"})
    )

    def set_initials(self, webpage: Webpage):
        for field in self.fields:
            if field not in ("source_type", "number_of_authors",):
                self.fields[field].initial = webpage.__getattribute__(field)
        return self


class AddLinkForm(forms.Form):
    link = forms.CharField()

    def save_link(self, source: Source) -> bool | str:
        """Checks and saves link for given source"""
        link = self.cleaned_data["link"]
        if not check_link(link):
            return False
        source.link = link
        source.save(update_fields=("link",))
        return link


class NewQuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "page"]
    
    def save_quote(self, source: Source) -> Quote:
        """Save new Quote object"""
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()
        return new_quote


class AlterQuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "page"]

    def set_initials(self, quote: Quote):
        """Pre-populate fields"""
        self.fields["text"].initial = quote.text
        self.fields["page"].initial = quote.page
        return self 


    def save_altered_quote(self, quote: Quote) -> Quote:
        quote.text = self.cleaned_data["text"]
        quote.page = self.cleaned_data["page"]
        quote.save(update_fields=("text", "page",))
        return quote
        

class AlterEndnoteForm(forms.Form):
    apa = forms.CharField(widget=forms.TextInput)
    mla = forms.CharField(widget=forms.TextInput)

    def set_initials(self, endnote: Endnote):
        """Pre-populate fields"""
        self.fields["apa"].initial = endnote.apa
        self.fields["mla"].initial = endnote.mla
        return self
        

    def save_altered_endnote(self, endnote: Endnote) -> Endnote:
        """Alter text field in Endnote obj"""
        endnote.apa = self.cleaned_data["apa"]
        endnote.mla = self.cleaned_data["mla"]
        endnote.save(update_fields=("apa", "mla",))
        return endnote


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
