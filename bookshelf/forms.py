from django import forms

from .models import Article, Book, Chapter, Quote, Source, Website, Endnote
from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla
from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from user_management.models import User
from utils.verification import check_link
from work_space.models import WorkSpace

from .validation import clean_text_data


# Delete all author related fields!
# Add author as an arg to all saving methods!

# get initials as separate func! (or method)



def save_endnotes(source: Source):
    """Creates and saves new Endnote obj for given source"""
    endnotes = Endnote(source=source, apa=quote_source_apa(source), mla=quote_source_mla(source))
    return endnotes.save()


class FieldClass:

    common_fields = "common_fields"
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    website_class = "website"


class BookForm(forms.Form):

    source_type = forms.CharField(initial="book", widget=forms.HiddenInput())
    number_of_authors = forms.IntegerField(widget=forms.HiddenInput(attrs={"name": "number_of_authors", 
                                                                                      "class": "final_number_of_authors"}))

    title = forms.CharField()
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))


    def save_form(self, user: User, space: WorkSpace, author: str):
        """Custom save func for Book obj"""
        # TODO

        data: dict = {}

        for field in self.fields:
            info = self.cleaned_data[field]
            if type(info) == str:
                info = clean_text_data(info)
            data[field] = info
        
        new_book = Book(work_space=space, user=user, title=data["title"], 
                        author=author, year=data["year"], 
                        publishing_house=data["publishing_house"])
        
        new_book.save()

        return save_endnotes(new_book)


class ArticleForm(forms.Form):

    source_type = forms.CharField(initial="article", widget=forms.HiddenInput())
    number_of_authors = forms.IntegerField(initial=1, widget=forms.HiddenInput(attrs={"name": "number_of_authors"}))

    journal_title = forms.CharField()
    article_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    volume = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    issue = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))


    def save_form(self, user: User, space: WorkSpace, author: str):
        """Custom save func for Article obj"""
        # TODO
        
        data: dict = {}

        for field in self.fields:
            info = self.cleaned_data[field]
            if type(info) == str:
                info = clean_text_data(info)
            data[field] = info

        new_article = Article(work_space=space, user=user, title=data["article_title"], author=author, year=data["year"], 
                              journal_title=data["journal_title"], volume=data["volume"], 
                              issue=data["issue"], pages=data["pages"], link_to_journal=data["link_to_journal"])
        
        new_article.save()
        return save_endnotes(new_article)


class ChapterForm(forms.Form):

    source_type = forms.CharField(initial="chapter", widget=forms.HiddenInput())
    number_of_authors = forms.IntegerField(initial=1, widget=forms.HiddenInput(attrs={"name": "number_of_authors"}))

    # chapter authors + book authors!

    chapter_title = forms.CharField()
    book_title = forms.CharField()
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))


    def save_form(self, user: User, space: WorkSpace, author: str):
        """Custom save func for Chapter obj"""
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
    number_of_authors = forms.IntegerField(initial=1, widget=forms.HiddenInput(attrs={"name": "number_of_authors"}))

    # page authors!

    website_title = forms.CharField()
    page_title = forms.CharField()
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))


    def save_form(self, user: User, space: WorkSpace, author: str):
        """Custom save func for Website obj"""
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
