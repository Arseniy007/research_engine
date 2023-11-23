from django import forms
from .models import Book, Quote, Source, Endnote, Article, Chapter, Webpage
from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from utils.verification import check_link


EXCLUDE_FIELDS = ("user", "work_space", "real_type", "file", "link",)


# Do I need this?
class FieldClass:
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    webpage_class = "webpage"


class CommonFields(forms.Form):
    number_of_authors = forms.IntegerField(widget=forms.HiddenInput(attrs={
        "name": "number_of_authors", 
        "class": "final_number_of_authors"}))


class BookForm(CommonFields):
    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "book"}))
    title = forms.CharField()
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))


class ArticleForm(CommonFields):
    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "article"}))
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
    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "chapter"}))
    chapter_title = forms.CharField()
    book_title = forms.CharField()
    publishing_house = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.book_class}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    edition = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))
    pages = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))


class WebpageForm(CommonFields):
    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "webpage"}))
    page_title = forms.CharField()
    website_title = forms.CharField()
    page_url = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.webpage_class}))
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": FieldClass.webpage_class}))


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


class NewQuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "page"]
    
    def save_quote(self, source: Source):
        """Save new Quote object"""
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()


class AlterQuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "page"]

    def save_altered_quote(self, quote: Quote):
        quote.text = self.cleaned_data["text"]
        quote.page = self.cleaned_data["page"]
        quote.save(update_fields=("text", "page",))
        

class AlterEndnoteForm(forms.Form):
    apa = forms.CharField(widget=forms.Textarea)
    mla = forms.CharField(widget=forms.Textarea)

    def save_endnote(self, endnote: Endnote):
        """Alter text field in Endnote obj"""
        endnote.apa = self.cleaned_data["apa"]
        endnote.mla = self.cleaned_data["mla"]
        return endnote.save(update_fields=("apa", "mla",))


class AlterBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = EXCLUDE_FIELDS
    
    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "book"}))

    def set_initials(self, book: Book):
        for field in self.fields:
            if field != "source_type":
                self.fields[field].initial = book.__getattribute__(field)
        return self


class AlterArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = EXCLUDE_FIELDS
    
    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "article"}))

    def set_initials(self, article: Article):
        for field in self.fields:
            if field != "source_type":
                self.fields[field].initial = article.__getattribute__(field)
        return self


class AlterChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = "__all__"
        exclude = EXCLUDE_FIELDS

    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "chapter"}))

    def set_initials(self, chapter: Chapter):
        for field in self.fields:
            if field != "source_type":
                self.fields[field].initial = chapter.__getattribute__(field)
        return self


class AlterWebpageForm(forms.ModelForm):
    class Meta:
        model = Webpage
        fields = "__all__"
        exclude = EXCLUDE_FIELDS

    source_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "webpage"}))

    def set_initials(self, webpage: Webpage):
        for field in self.fields:
            if field != "source_type":
                self.fields[field].initial = webpage.__getattribute__(field)
        return self


def get_type_of_source_form(data, alter_source=False):
    """
    Based on form hidden imput get obj type and return either obj-creation or obj-alter form.
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
