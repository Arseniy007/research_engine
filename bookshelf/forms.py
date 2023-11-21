from django import forms
from .models import Book, Quote, Source, Endnote
from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from utils.verification import check_link

# Do I need this?
class FieldClass:
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    website_class = "website"


class CommonFields(forms.Form):
    number_of_authors = forms.IntegerField(widget=forms.HiddenInput(attrs={
        "name": "number_of_authors", 
        "class": "final_number_of_authors"}))


class BookForm(CommonFields):
    source_type = forms.CharField(initial="book", widget=forms.HiddenInput())
    title = forms.CharField()
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))


class ArticleForm(CommonFields):
    source_type = forms.CharField(initial="article", widget=forms.HiddenInput())
    journal_title = forms.CharField()
    article_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    volume = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    issue = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))


class ChapterForm(CommonFields):
    number_of_chapter_authors = forms.IntegerField(widget=forms.HiddenInput(attrs={
        "name": "number_of_chapter_authors", 
        "class": "final_number_of_chapter_authors"}))
    source_type = forms.CharField(initial="chapter", widget=forms.HiddenInput())
    chapter_title = forms.CharField()
    book_title = forms.CharField()
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))


class WebsiteForm(CommonFields):
    source_type = forms.CharField(initial="website", widget=forms.HiddenInput())
    website_title = forms.CharField()
    page_title = forms.CharField()
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))

    # page authors!











class UploadSourceForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))


    def save_file(self, source: Source):
       """Save new source-file"""
       source.file = self.cleaned_data["file"]
       source.save(update_fields=("file",))


class AddLinkForm(forms.Form):
    link = forms.CharField()


    def save_link(self, source: Source):
        """Checks and saves link for given source"""
        link = self.cleaned_data["link"]
        if not check_link(link):
            return False
        
        source.link = link
        source.save(update_fields=("link",))
        return True


class AlterSourceForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "multiple_authors", "file"]

    # Probably gonna chaned that later
    # TODO


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
        fields = ["text", "page"]
    

    def save_quote(self, source: Source):
        """Save new Quote object"""
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()


class AlterEndnoteForm(forms.Form):

    # TODO

    apa = forms.CharField(widget=forms.Textarea)
    mla = forms.CharField(widget=forms.Textarea)


    def save_endnote(self, endnote: Endnote):
        """Alter text field in Endnote obj"""
        endnote.apa = self.cleaned_data["apa"]
        endnote.mla = self.cleaned_data["mla"]
        return endnote.save(update_fields=("apa", "mla",))
