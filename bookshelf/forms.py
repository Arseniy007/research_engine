from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website, Endnote

from user_management.models import User
from work_space.models import WorkSpace

from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla


CHOICES = (("Book", "Book"), ("Article", "Article"), ("Chapter", "Chapter"), ("Website", "Website"),)


def save_endnotes(source: Source):
    """Creates and saves new Endnote obj for given source"""

    endnotes = Endnote(source=source, apa=quote_source_apa(source), mla=quote_source_mla(source))
    return endnotes.save()


def clean_text_data(data: str):

    return data.strip("., ")


class FieldClass:

    common_fields = "common_fields"
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    website_class = "website"


class BookForm(forms.Form):

    source_type = forms.CharField(initial="book", widget=forms.HiddenInput())

    title = forms.CharField()
    author_last_name = forms.CharField()
    author_first_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))
    author_second_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    link = forms.CharField(widget=forms.TextInput(attrs={"required": False}))

    def save_form(self, user: User, space: WorkSpace):
        # TODO

        data: dict = {}

        for field in self.fields:
            info = self.cleaned_data[field]
            if type(info) == str:
                info = clean_text_data(info)
            data[field] = info

        author = f"{data['author_last_name']} {data['author_first_name']} {data['author_second_name']}"
        
        new_book = Book(work_space=space, user=user, title=data["title"], 
                        author=author, year=data["year"], link=data["link"], 
                        publishing_house=data["publishing_house"])
        new_book.save()

        return save_endnotes(new_book)


class ArticleForm(forms.Form):

    source_type = forms.CharField(initial="article", widget=forms.HiddenInput())

    journal_title = forms.CharField()
    article_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    author_last_name = forms.CharField()
    author_first_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))
    author_second_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))
    volume_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    journal_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    link = forms.CharField(widget=forms.TextInput(attrs={"required": False}))


    def save_form(self, user: User, space: WorkSpace):
        # TODO
        
        data: dict = {}

        for field in self.fields:
            info = self.cleaned_data[field]
            if type(info) == str:
                info = clean_text_data(info)
            data[field] = info

        author = f"{data['author_last_name']} {data['author_first_name']} {data['author_second_name']}"

        new_article = Article(work_space=space, user=user, title=data["article_title"], author=author, year=data["year"], 
                              link=data["link"], journal_title=data["journal_title"], volume_number=data["volume_number"], 
                              journal_number=data["journal_number"], pages=data["pages"], link_to_journal=data["link_to_journal"])
        
        new_article.save()
        return save_endnotes(new_article)


class ChapterForm(forms.Form):

    source_type = forms.CharField(initial="chapter", widget=forms.HiddenInput())

    chapter_title = forms.CharField()
    chapter_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    book_title = forms.CharField()
    book_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    link = forms.CharField(widget=forms.TextInput(attrs={"required": False}))


    def save_form(self, user: User, space: WorkSpace):
        # TODO

        data: dict = {}

        for field in self.fields:
            info = self.cleaned_data[field]
            if type(info) == str:
                info = clean_text_data(info)
            data[field] = info
        
        
        new_chapter = Chapter(work_space=space, user=user, title=data["book_title"], author=data["book_author"], 
                              chapter_title=data["chapter_title"], chapter_author=data["chapter_author"],
                              edition = data["edition"], pages=data["pages"], link=data["link"])
        
        new_chapter.save()
        return save_endnotes(new_chapter)

        

class WebsiteForm(forms.Form):

    source_type = forms.CharField(initial="website", widget=forms.HiddenInput())

    website_title = forms.CharField()
    page_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    page_title = forms.CharField()
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))
    link = forms.CharField(widget=forms.TextInput(attrs={"required": False}))


    def save_form(self, user: User, space: WorkSpace):
        # TODO

        data: dict = {}

        for field in self.fields:
            info = self.cleaned_data[field]
            if type(info) == str:
                info = clean_text_data(info)
            data[field] = info

        new_website = Website(work_space=space, user=user, title=data["page_title"], author = data["page_author"], 
                              website_title=data["website_title"], page_url=data["page_url"], date=data["date"])
        
        new_website.save()
        return save_endnotes(new_website)
        












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



class AlterEndnoteForm(forms.Form):

    QUOTING_TYPES = (("APA", "APA"), ("MLA", "MLA"))

    quoting_type = forms.ChoiceField(choices=QUOTING_TYPES, widget=forms.HiddenInput())
    new_text = forms.CharField()

    
    def save_endnote(self, endnote: Endnote):
        "Alter text field in Endnote obj"

        if self.quoting_type == "APA":
            endnote.apa = self.cleaned_data["new_text"]
            endnote.save(update_fields=("apa",))
        else:
            endnote.mla = self.cleaned_data["new_text"]
            endnote.save(update_fields=("mla",))
