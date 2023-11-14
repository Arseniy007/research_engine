from django import forms
from django.forms import BaseFormSet

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website


from django.forms import formset_factory

from user_management.models import User
from work_space.models import WorkSpace


CHOICES = (("Book", "Book"), ("Article", "Article"), ("Chapter", "Chapter"), ("Website", "Website"),)
BOOK_FIELDS = ("book_title", "author_last_name", "author_first_name", "author_second_name", "pulishing_house", "year", "link")
ARTICLE_FIELDS = ("journal_title", "article_title", "author_last_name", 
                  "author_first_name", "author_second_name", "volume_number", 
                  "journal_number", "pages", " is_electronic", "link_to_journal")

CHAPTER_FIELDS = ("chapter_title", "chapter_author", "book_title", "book_author", "edition", "pages")
WEBSITE_FIELDS = ("website_title", "page_author", "page_title", "page_url", "date")


def clean_text_data(data: str):

    return data.strip("., ")


#class BaseArticleFormSet(BaseFormSet):
    #ordering_widget = forms.HiddenInput()



class AuthorForm(forms.Form):

    last_name = forms.CharField()
    first_name = forms.CharField()
    second_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))


#AuthorFormSet = formset_factory(AuthorForm, formset="", can_delete=True, can_order=True)



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
    second_author = forms.CharField(widget=forms.TextInput(attrs={"class": "hidden"}))
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = CommonFields().year
    link = CommonFields().link


    def save_form(self, user: User, space: WorkSpace):
        # TODO

        data: dict = {}

        for field in BOOK_FIELDS:
            data[field] = clean_text_data(self.cleaned_data[field])

        author = f"{data['author_last_name']} {data['author_first_name']} {data['author_second_name']}"
        
        new_book = Book(work_space=space, user=user, title=data["title"], 
                        author=author, year=data["year"], link=data["link"], 
                        publishing_house=data["publishing_house"])
        return new_book.save()


class ArticleForm(forms.Form):

    journal_title = CommonFields().title
    article_title = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    author_last_name = CommonFields().author_last_name
    author_first_name = CommonFields().author_first_name
    author_second_name = CommonFields().author_second_name
    volume_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    journal_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.article_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))
    link_to_journal = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.article_class}))


    def save_form(self, user: User, space: WorkSpace):
        # TODO
        
        data: dict = {}

        for field in ARTICLE_FIELDS:
            data[field] = clean_text_data(self.cleaned_data[field])

        author = f"{data['author_last_name']} {data['author_first_name']} {data['author_second_name']}"

        new_article = Article(work_space=space, user=user, title=data["title"], author=author, year=data["year"], 
                              link=data["link"],journal_title=data["journal_title"], article_title=data["article_title"], 
                              volume_number=data["volume_number"], journal_number=data["journal_number"], pages=data["pages"],
                              link_to_journal=data["link_to_journal"])
        
        return new_article.save()


class ChapterForm(forms.Form):

    chapter_title = CommonFields().title
    chapter_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    book_title = CommonFields().title
    book_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.IntegerField(widget=forms.NumberInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))


    def save_form(self, user: User, space: WorkSpace):
        # TODO

        data: dict = {}

        for field in CHAPTER_FIELDS:
            data[field] = clean_text_data(str(self.cleaned_data[field]))
        
        
        new_chapter = Chapter(work_space=space, user=user, title=data["book_title"], author=data["book_author"], 
                              chapter_title=data["chapter_title"], chapter_author=data["chapter_author"],
                              edition = data["edition"], pages=data["pages"])
        
        return new_chapter.save()

        

class WebsiteForm(forms.Form):

    website_title = CommonFields().title
    page_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    page_title = CommonFields().title
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.website_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class": FieldClass.website_class}))


    def save_form(self, user: User, space: WorkSpace):
        # TODO

        data: dict = {}

        for field in WEBSITE_FIELDS:
            data[field] = clean_text_data(self.cleaned_data[field])

        new_website = Website(work_space=space, user=user, title=data["page_title"], author = data["page_author"], 
                              website_title=data["website_title"], page_url=data["page_url"], date=data["date"])
        
        return new_website.save()
        












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
