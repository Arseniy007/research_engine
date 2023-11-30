"""

def validate_file_extension(value):
    print(value.file.content_type)
    if value.file.content_type != "application/pdf":
        raise ValidationError(u'Error message')
"""


"""
def __str__(self):
    return f"uploads/papers/{str(self.file)}"
"""

"""
def file_link(self):
    
    return format_html("<a href='%s'>download</a>" % (f"file/uploads/papers/{self.file.url}",))

file_link.allow_tags = True
"""




"""

from .check_paper import check_paper, check_file
from django.http import FileResponse

def handle_file_2(user_id, file_id):

    file = check_file(user_id, file_id)

    if not file:
        pass


    location = file.get_path()

    opened_file = open(location, "rb")

    return FileResponse(opened_file)

"""


"""

def delete_files(paper_id, user):

    paper = check_paper(paper_id, user)

    files_directory_location = paper.get_path()

    remove(files_directory_location)

 """


"""


from django.http import FileResponse

from . verification import check_file


def display_file(user, file_id):

    file = check_file(file_id, user)

    return FileResponse(open(file.get_path(), "rb"))


"""

"""
    words = text.split()
    header = "Lorem ipsum dolor sit amet"
    print(len(words) - len(header.split()))
    print(len(text) - len(header))

    print(text)
  

    
    

    #word_count = len(re.findall(r"\b\w+\b", text)) 

    #word_count = re.sub('<(.|\n)*?>','', text)

    #print(len(text))

    

    paragraphs = text.split("\n\n")

    num_of_word = len(paragraphs)

    for paragraph in paragraphs:

        if paragraph != "\n":

            words = len(paragraph.split())
            num_of_word += words

    num_of_word += len(paragraphs)
    
    
    print(num_of_word, "hf")
    print(len(text))
    #print(text.encode().decode('utf-8', 'ignore'))


    print(text)



    f"user_{instance.user.id}/paper_{instance.paper.pk}/{saving_date}/{filename}"

"""









"""
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/paper_<id>/<saving_date>/<filename>

    saving_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"user_{instance.paper.user.pk}/paper_{instance.paper.pk}/{saving_date}/{filename}"
"""

"""
def get_saving_time():

    return datetime.now().strftime(SAVING_TIME_FORMAT)

"""

"""
def ownership_required(function):

    def wrapper(user, space_id):
        
        space = check_work_space(space_id)

        if space.owner != user:
            raise Http404
        
        function(user, space_id)

    return wrapper

"""

"""
    if paper.work_space.owner != user and user not in paper.work_space.guests:
        raise Http404
    return paper


    if file.paper.work_space.owner != user or user not in file.paper.work_space.guests:
        raise Http404
    return file

"""


"""

@login_required(redirect_field_name=None)
def test_restructure_dir(request, space_id):

    space = check_work_space(space_id, request.user)

    papers = space.papers.all()
    books = space.books.all()

    if not papers and not books:
        return JsonResponse({"message": "Empty Work Space"})

    space.create_friendly_dir()
    root_path = space.get_friendly_path()


    if papers:

        papers_root = f"{root_path}/papers"

        os.mkdir(papers_root)

        authors = [paper.user for paper in papers]

        for author in authors:

            author_name = f"{author.last_name} {author.first_name}"

            os.makedirs(os.path.join(papers_root, author_name), exist_ok=True)

            author_papers = papers.filter(user=author)

            for author_paper in author_papers:

                path_to_paper = f"{papers_root}/{author_name}/{author_paper}"

                os.makedirs(path_to_paper, exist_ok=True)

                versions = author_paper.versions.all()

                for version in versions:

                    path_to_paper_version = f"{path_to_paper}/{version.get_saving_time()}"
                    os.makedirs(path_to_paper_version, exist_ok=True)
                    file_name = version.file_name()


                    original_file = version.get_full_path()
                    destination = os.path.join(path_to_paper_version, file_name)

                    shutil.copyfile(original_file, destination)
    
    if books:
        # Create a txt/exel etc. file for all books (not book files)?
        pass

    return JsonResponse({"message": "ok"})

"""



"""
   if len(name) != 2:

                last_name, first_name = name[0], name[1]
                return f"{last_name} {first_name[0]}. ({self.year}). {self.title}. {self.publishing_house}."
        
            else:
                last_name, first_name, second_name = name[0], name[1], name[2]
                return f"{last_name} {first_name[0]}. {second_name[0]}. ({self.year}). {self.title}. {self.publishing_house}."

def quote_apa(self):
        '''Makes qoute following APA standarts'''

        authors = self.author.split(",")
        authors_name = []

        for one in authors:

            name = one.split()
            last_name = name[0]
            initials = ""

            for i in range(1, len(name)):
                initials += f"{name[i][0]}."

            authors_name.append(f"{last_name} {initials}")
                
        if len(authors_name) == 1:
            author = authors_name[0]
        else:
            author = ", ".join(authors_name)

        # See quoting.py

        return f"{author} ({self.year}). {self.title}. {self.publishing_house}."


    def quote_mla(self):

        pass



"""






"""
from user_management.models import User

from work_space.models import WorkSpace

from bookshelf.models import Book

from bookshelf.quoting_apa import quote_book_apa

user = User.objects.get(pk=1)

space = WorkSpace.objects.get(pk=2)


book = Book.objects.get(pk=2)



quote_book_apa(book)
"""


#Old bookshelf models:

"""
def author_last_name(self):

    if self.multiple_authors:

        authors = self.author.split("/")
        pass

    else:
        return self.author.split()[0]
"""




"""

class EditedBook(Book):

    #work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="edited_books")
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edited_books")
    #authors = models.ManyToManyField(,related_name="edited_books")
    #edition = models.CharField(max_length=10)


class Book(Text):

    pass

    def __str__(self):
        return f"{self.author_last_name} {self.author_first_name[0]}. ({self.year}). {self.title}. {self.publishing_house}"

class MultipleAuthorsBook(Text):

    authors = models.ManyToManyField(Author,related_name="multiple_authors_book")
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="multiple_authors_book")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="multiple_authors_book")

#author_last_name = models.CharField(max_length=30)
#author_first_name = models.CharField(max_length=30)
#author_second_name = models.CharField(max_length=30, blank=True)

class Author(models.Model):

    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    #initials = models.CharField(max_length=10)

    
    def __str__(self):
        '''Display authors name'''
        return f"{self.last_name} {self.first_name}"

class BookAbstractModel(models.Model):

    related_name = "books"

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name=related_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)

    title = models.CharField(max_length=100)
    year = models.IntegerField(blank=True)
    link_to_text = models.CharField(max_length=40, blank=True)
    publishing_house = models.CharField(max_length=20)


    class Meta:
        abstract = True




class Chapter(BookAbstractModel):

    pages = models.CharField(max_length=20)


class CommonInfo(models.Model):

    title = models.CharField(max_length=100)
    year = models.IntegerField(blank=True)

    link_to_text = models.CharField(max_length=40, blank=True)

    class Meta:
        abstract = True

    
    def __str__(self):
        '''Display book title''''''
        return self.title


class Book(CommonInfo):

    related_name = "books"

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name=related_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)

    author = models.ManyToManyField(Author, related_name=related_name)

    publishing_house = models.CharField(max_length=20)
    #city = models.CharField(max_length=20, blank=True)

    is_edited = models.BooleanField(default=False)


    def __str__(self):
        
        author = self.author.all()[0]
        return f"{author.last_name} {author.first_name} ({self.year}). {self.title}"


class Journal(CommonInfo):

    related_name = "journals"

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name=related_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)

    author = models.ManyToManyField(Author, related_name=related_name)

    pass


class Article(Journal):

    pages = models.CharField(max_length=20)


class Website(CommonInfo):

    related_name = "websites"

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name=related_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)

    author = models.ManyToManyField(Author, related_name=related_name)

    link = models.CharField(max_length=40, blank=True)


class Quote(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quotes")
    page = models.IntegerField()
    text = models.TextField()

    
    def __str__(self):
        '''Display quotes text'''
        return self.text
    


"""

"""
def check_book(book_id, user):
    '''Checks if book exists'''

    try:
        book = Book.objects.get(pk=book_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(book.work_space.pk, user)
        return book
    

def check_article(article_id, user):
    '''Checks if article exists'''

    try:
        article = Article.objects.get(pk=article_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(article.work_space.pk, user)
        return article
    

def check_website(website_id, user):
    '''Checls if website exists'''

    try:
        website = Website.objects.get(pk=website_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(website.work_space.pk, user)
        return website

        


def article_ownership_required(func: Callable):
    '''Checks if current user added this article'''
    def wrapper(request, article_id):

        article = check_article(article_id, request.user)
        if article.user != request.user:
            raise PermissionDenied
        
        return func(request, article_id)
    return wrapper


def book_ownership_required(func: Callable):
    '''Checks if current user added this book'''
    def wrapper(request, book_id):

        book = check_book(book_id, request.user)
        if book.user != request.user:
            raise PermissionDenied
        
        return func(request, book_id)
    return wrapper


class Book(Source):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="sources")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sources")

    publishing_house = models.CharField(max_length=20, blank=True)


    def __str__(self):
        '''Display book title'''
        return self.title
    

    def get_path(self):
        '''Returns a path to the book directory'''
        return f"{self.work_space.get_path()}/books/user_{self.user.pk}/book_{self.pk}"
    

    def get_path_to_file(self):
        '''Returns a path to the book file'''
        return os.path.join(self.get_path(), os.path.basename(self.file.name))

        

class Quote(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="quotes")
    object_id = models.PositiveIntegerField()
    source = GenericForeignKey("content_type", "object_id")
    page = models.IntegerField()
    text = models.TextField()

    
    def __str__(self):
        '''Display quotes text'''
        return f'"{self.text}" (p. {self.page})'


"""

"""
class NewSourceForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "author", "multiple_authors", "file"]


    author_last_name = forms.CharField(max_length=40)
    author_first_name = forms.CharField(max_length=40)
    author_second_name = forms.CharField(max_length=40)


    def save_source(self, user: User, space: WorkSpace):

        # deal with authors here!

        # Have another func with re module to fix all possible problems?

        title = self.cleaned_data["title"].strip(". ")

        author_last_name = self.cleaned_data["author_last_name"].strip(". ")
        author_first_name = self.cleaned_data["author_first_name"].strip(". ")
        author_second_name = self.cleaned_data["author_second_name"].strip(". ")

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year, publishing_house = self.cleaned_data["year"].strip(". "), self.cleaned_data["publishing_house"].strip(". ")

        new_book = Book(user=user, work_space=space, title=title, author=author, year=year, publishing_house=publishing_house)
        new_book.save()

"""


""""

#import re
from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website

from user_management.models import User
from work_space.models import WorkSpace


EXCLUDED_FIELDS = ("user", "work_space", "file", "real_type", "author", "multiple_authors")


class NewSourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ("title", "year", "link")

    author_last_name = forms.CharField(max_length=40)
    author_first_name = forms.CharField(max_length=40)
    author_second_name = forms.CharField(max_length=40)


    def save_source(self, user: User, space: WorkSpace):

        # deal with authors here!

        # Have another func with re module to fix all possible problems?

        title = self.cleaned_data["title"].strip(". ")

        author_last_name = self.cleaned_data["author_last_name"].strip(". ")
        author_first_name = self.cleaned_data["author_first_name"].strip(". ")
        author_second_name = self.cleaned_data["author_second_name"].strip(". ")

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year, publishing_house = self.cleaned_data["year"].strip(". "), self.cleaned_data["publishing_house"].strip(". ")

        new_book = Book(user=user, work_space=space, title=title, author=author, year=year, publishing_house=publishing_house)
        new_book.save()


class NewBookForm(forms.Form):

    publishing_house = forms.CharField(max_length=30)


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = EXCLUDED_FIELDS


class NewChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = "__all__"
        exclude = EXCLUDED_FIELDS




class NewWebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = "__all__"
        exclude = EXCLUDED_FIELDS
    



class UploadSourceForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))

    
    def save_file(self, source: Source):
       '''Save new source-file'''
       source.file = self.cleaned_data["file"]
       source.save(update_fields=("file",))


class AlterSourceForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "multiple_authors", "file"]


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
        '''Save new Quote object'''
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()

        class NewBookForm(forms.Form):

    publishing_house = forms.CharField(max_length=30)


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = EXCLUDED_FIELDS


class NewChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = "__all__"
        exclude = EXCLUDED_FIELDS




class NewWebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = "__all__"
        exclude = EXCLUDED_FIELDS
    

<h3>Book form</h3>
    <form enctype="multipart/form-data" action="{% url 'bookshelf:add_source' space.pk %}" method="post">
        {% csrf_token %} 
        {{ book_form }}
        <button  type="submit">Add Book</button>
    </form><br><br><br>
    <h3>Article form</h3>
    <form enctype="multipart/form-data" action="{% url 'bookshelf:add_source' space.pk %}" method="post">
        {% csrf_token %} 
        {{ article_form }}
        <button  type="submit">Add Article</button>
    </form><br><br><br>
    <h3>Chapter form</h3>
    <form enctype="multipart/form-data" action="{% url 'bookshelf:add_source' space.pk %}" method="post">
        {% csrf_token %} 
        {{ chapter_form }}
        <button  type="submit">Add Chapter</button>
    </form><br><br><br>
    <h3>Website form</h3>
    <form enctype="multipart/form-data" action="{% url 'bookshelf:add_source' space.pk %}" method="post">
        {% csrf_token %} 
        {{ website_form }}
        <button  type="submit">Add Website</button>
    </form><br><br><br>

      title = clean_text_data(self.cleaned_data["title"])

        author_last_name = clean_text_data(self.cleaned_data["author_last_name"])
        author_first_name = clean_text_data(self.cleaned_data["author_first_name"])
        author_second_name = clean_text_data(self.cleaned_data["author_second_name"])

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year = self.cleaned_data["year"]

        common_info["author"] = author
        common_info["title"] = title
        common_info["year"] = year

        
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
       '''Save new source-file'''
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

        exclude = ["source"]

        # TODO qury set of books, articles and websites
    

    def save_quote(self, source: Source):
        '''Save new Quote object'''
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()


        class SourceTypeForm(forms.Form):
    '''Do I need it???'''

    source_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={"required": True}))


"""

"""

<h3>Source form</h3>
    <form action="{% url 'bookshelf:add_source' space.pk %}" method="post">
        {% csrf_token %} 
        {{ source_form.as_p }}
        <button type="submit">Add Source</button>
    </form><br><br><br>



     <form action="{% url 'bookshelf:add_source' space.pk %}" method="post" id="website_form">
        {% csrf_token %} 
        {{ website_form.as_p }}
        <button value="website" type="submit">Add Website</button>
    </form><br><br><br>

        <form action="{% url 'bookshelf:add_source' space.pk %}" method="post" id="book_form">
        {% csrf_token %} 
        {{ book_form.as_p }}
        <button value="book" type="submit">Add Book</button>
    </form><br><br><br>

    <form action="{% url 'bookshelf:add_source' space.pk %}" method="post" id="article_form">
        {% csrf_token %} 
        {{ article_form.as_p }}
        <button value="article" type="submit">Add Article</button>
    </form><br><br><br>



        <form action="{% url 'bookshelf:add_source' space.pk %}" method="post">
        {% csrf_token %} 
        {{ author_formset }}
        <button id="add_author">Add Author</button>
        <button type="submit">Submit authors</button>
    </form>


    from django import forms
from django.forms import BaseFormSet

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Article, Book, Chapter, Quote, Source, Website


from convenient_formsets import ConvenientBaseFormSet
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


AuthorFormSet = formset_factory(AuthorForm, formset=ConvenientBaseFormSet, can_delete=True, can_order=True)



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
    for i in range(22):
        second_author = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "hidden"}))
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
       '''Save new source-file'''
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
        '''Save new Quote object'''
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()

        
    <div id="author-formset">
        <div id="author-forms-container">
            {% for author_form in author_formset.forms %}
                <div class="author-form">
                    {{ author_form.last_name }}
                    {{ author_form.first_name }}
                    {{ author_form.second_name }}
                    {% if author_formset.can_delete %}
                        {{ author_form.DELETE }}
                        <input type="button" id="delete-form-button" value="Delete">
                    {% endif %}
                    {% if author_formset.can_order %}
                        {{ author_form.ORDER }}
                        <input type="button" id="move-form-up-button" value="Move up">
                        <input type="button" id="move-form-down-button" value="Move down">
                    {% endif %}
                </div>
            {% endfor %}
        </div>
        <div><input type="button" id="add-form-button" value="Add another"></div>
        <template id="empty-form-template">
            <div class="author-form">
                {{ author_formset.empty_form.last_name }}
                {{ author_formset.empty_form.first_name }}
                {{ author_formset.empty_form.second_name }}
                {% if author_formset.can_delete %}
                    <input type="button" id="delete-form-button" value="Delete">
                {% endif %}
                {% if author_formset.can_order %}
                    {{ author_form.ORDER }}
                    <input type="button" id="move-form-up-button" value="Move up">
                    <input type="button" id="move-form-down-button" value="Move down">
                {% endif %}
            </div>
        </template>
        {{ author_formset.management_form }}
    </div>
#class BaseArticleFormSet(BaseFormSet):
    #ordering_widget = forms.HiddenInput()
#AuthorFormSet = formset_factory(AuthorForm, formset="", can_delete=True, can_order=True)

class AuthorForm(forms.Form):

    last_name = forms.CharField()
    first_name = forms.CharField()
    second_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))

    class CommonFields(forms.Form):

    def __init__(self):
        self.title = forms.CharField()
        self.author_last_name = forms.CharField()
        self.author_first_name = forms.CharField()
        self.author_second_name = forms.CharField(widget=forms.TextInput(attrs={"required": False}))
        self.year = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.common_fields}))
        self.link = forms.CharField(widget=forms.TextInput(attrs={"required": False}))

        
    #second_author = forms.CharField(widget=forms.TextInput(attrs={"class": "hidden"}))


#from django.forms import formset_factory

BOOK_FIELDS = ("title", "author_last_name", "author_first_name", "author_second_name", "publishing_house", "year", "link")
ARTICLE_FIELDS = ("journal_title", "article_title", "author_last_name", 
                  "author_first_name", "author_second_name", "volume_number", 
                  "journal_number", "pages", " is_electronic", "link_to_journal")

CHAPTER_FIELDS = ("chapter_title", "chapter_author", "book_title", "book_author", "edition", "pages")
WEBSITE_FIELDS = ("website_title", "page_author", "page_title", "page_url", "date")

#multiple_authors = models.BooleanField(default=False)

    def save_endnote(self, endnote: Endnote):
        "Alter text field in Endnote obj"

            QUOTING_TYPES = (("APA", "APA"), ("MLA", "MLA"))

    quoting_type = forms.ChoiceField(choices=QUOTING_TYPES, widget=forms.HiddenInput())

        if self.quoting_type == "APA":
            endnote.apa = self.cleaned_data["new_text"]
            endnote.save(update_fields=("apa",))
        else:
            endnote.mla = self.cleaned_data["new_text"]
            endnote.save(update_fields=("mla",))


    @login_required(redirect_field_name=None)
    def quote_sourse(request, source_id):
    # TODO

    source = check_source(source_id, request.user)
    # Do I need it?
    pass
    
    CHOICES = (("Book", "Book"), ("Article", "Article"), ("Chapter", "Chapter"), ("Website", "Website"),)


    author_last_name = forms.CharField()
    author_first_name = forms.CharField(required=False)
    author_second_name = forms.CharField(required=False)

    #chapter_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))

     book_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))

     #page_author = forms.CharField(widget=forms.TextInput(attrs={"class": FieldClass.chapter_class}))

     function show_form(type) {

                let form = document.getElementById(`${type}_form`);

                form.style.display = 'block';
            }

            book_button.addEventListener('click', () => show_form(book_button.innerHTML));
            article_button.addEventListener('click', () => show_form(article_button.innerHTML));
            chapter_button.addEventListener('click', () => show_form(chapter_button.innerHTML));
            website_button.addEventListener('click', () => show_form(website_button.innerHTML));

                        const book_button = document.getElementById('book_button');
            const article_button = document.getElementById('article_button');
            const chapter_button = document.getElementById('chapter_button');
            const website_button = document.getElementById('website_button');

"""

"""
<script>

        document.addEventListener('DOMContentLoaded', function() {







            



            const show_form_buttons = document.getElementsByClassName('show_form_button');
           
            const number_of_buttons = show_form_buttons.length;
            console.log(number_of_buttons);
            

            for (let i = 0; i < number_of_buttons; i++) {

                let button = show_form_buttons[i];
   

                button.addEventListener('click', () => show_and_hide_forms(`${button.id}_form`));


            
            }


            




          
            const first_button = document.getElementById('first_button');
            first_button.addEventListener('click', function() {

                let new_div = document.getElementById('second_author');

                new_div.style.display = 'block';

            })




           // New staff

            let authors_divs = document.getElementsByClassName('authors_div');
            const number_of_divs = authors_divs.length;

            for (let i = 0; i < number_of_divs; i++) {

                let div = authors_divs[i];

                div.innerHTML = `
                <div class="author_${i}">
                    <label>Author Last Name: <input id="author_last_name_${i}" type="text"></label>
                    <label>Author First Name: <input id="author_first_name_${i}" type="text"></label>
                    <label>Author Second Name: <input id="author_second_name_${i}" type="text"></label>
                    <button id="add_author_button_${i}" type="button">Add Author(s)</button>
                </div>`;

                let add_button = document.querySelector(`#add_author_button_${i}`);
                add_button.addEventListener('click', function() {

                    add_button.style.display = 'none';

                    let new_div = document.createElement('div');

                    new_div.className = ""

                })
            }



function show_and_hide_forms(form_id) {

    let all_forms = document.querySelector('.source_form');
    const number_of_forms = all_forms.length;

    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }

    document.querySelector(`#${form_id}`).style.display = 'block';

};
        

        });
    </script>

    

    """

"""
def clean_text_data(data: str):



def clean_author_data(data):
Get, clean and validate all author-related form-field
    try:
        number_of_authors = int(data.get("number_of_authors"))
    except ValueError:
        # TODO
        pass

    authors: list = []
    for i in range(number_of_authors):
        last_name = data.get(f"last_name_{i}")
        first_name = data.get(f"first_name_{i}")
        second_name = data.get(f"second_name_{i}")

        if not last_name:
            # TODO
            pass
        last_name = clean_text_data(last_name)
        
        if not first_name:
            author = last_name
        else:
            first_name = clean_text_data(first_name)
            if second_name:
                second_name = clean_text_data(second_name)
                author = f"{last_name} {first_name} {second_name}"
            else:
                author = f"{last_name} {first_name}"
            
        authors.append(author)
    return ", ".join(authors)

    def save_form(self, user: User, space: WorkSpace, author: str):

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

        def save_form(self, user: User, space: WorkSpace, author: str):
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

         def save_form(self, user: User, space: WorkSpace, author: str):
        Custom save func for Chapter obj        # TODO

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

"""

# forms_test.py

"""

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
        Save new Quote object
        new_quote = Quote(source=source, page=self.cleaned_data["page"], text=self.cleaned_data["text"])
        new_quote.save()


class SourceTypeForm(forms.Form):
    '''Do I need it???'''

    source_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={"required": True}))

"""
# bookshelf/script.js:
"""
document.addEventListener('DOMContentLoaded', function() {

    const show_form_buttons = document.getElementsByClassName('show_form_button');
    const number_of_buttons = show_form_buttons.length;
    
    for (let i = 0; i < number_of_buttons; i++) {
        let button = show_form_buttons[i];
        button.addEventListener('click', () => show_and_hide_forms(`${button.id}_form`));
    }

    console.log("hus");


});



function show_and_hide_forms(form_id) {

    let all_forms = document.querySelector('.source_form');
    const number_of_forms = all_forms.length;

    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }

    document.querySelector(`#${form_id}`).style.display = 'block';

};


function hide_all_forms() {

    let all_forms = document.querySelector('.source_form');
    const number_of_forms = all_forms.length;
    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }
}

   # Interate through every aurhor
    for one in authors:
        name = one.split()
        last_name = name[0]
        # Get initials
        initials = ""
        # Iterate through first and second names
        for i in range(1, len(name)):
            initials += f"{name[i][0]}."
            
        authors_name.append(f"{last_name} {initials}")
    return ", ".join(authors_name)

    def format_date_apa(date: str):

    MONTHS = {"01": "January", "02": "February", "03": "March", "04": "April", 
              "05": "May", "06": "June", "07": "July", "08": "August", 
              "09": "September", "10": "October", "11": "November", "12": "December"}
    year, month, day = date.split("-")

    # Turn month from num to word
    month = MONTHS[month]

    # Delete '0' from day
    if day[0] == "0":
        day = day[-1]
    return f"{year}, {month} {day}"
    
    quote_pk = forms.CharField(widget=forms.HiddenInput())


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

        def set_initial_book_form(form, book: Book):
            pass
            
     # Get form type
    if "book" in request.POST:
        form = BookForm(request.POST)
    elif "article" in request.POST:
        form = ArticleForm(request.POST)
    elif "chapter" in request.POST:
        form = ChapterForm(request.POST)
    elif "webpage" in request.POST:
        form = WebpageForm(request.POST)
    else:
        # TODO
        return JsonResponse({"message": "error"})

                        if field == "date":
                    right_date = validate_date(info)
                    if not right_date:
                        # TODO
                        pass
                elif field == "link"


    def alter_article(article: Article, form: AlterArticleForm):

    was_updated = False
    for field in form.fields:
        if field != "source_type":
            info = form.cleaned_data[field]
            if article.__getattribute__(field) != info:
                if type(info) == str:
                    info = clean_text_data(info)
                article.__setattr__(field, info)
                article.save(update_fields=(field,))
    if was_updated:
        return update_endnotes(article)


def alter_chapter(chapter: Chapter, form: AlterChapterForm):

    was_updated = False
    for field in form.fields:
        if field != "source_type":
            info = form.cleaned_data[field]
            if chapter.__getattribute__(field) != info:
                if type(info) == str:
                    info = clean_text_data(info)
                chapter.__setattr__(field, info)
                chapter.save(update_fields=(field,))
    if was_updated:
        return update_endnotes(chapter)


def alter_webpage(webpage: Webpage, form: AlterWebpageForm):

    was_updated = False
    for field in form.fields:
        if field != "source_type":
            info = form.cleaned_data[field]
            if webpage.__getattribute__(field) != info:
                if type(info) == str:
                    info = clean_text_data(info)
                if field == "date":
                    if not validate_date(info):
                        # TODO
                        pass
                elif field == "page_url":
                    if not check_link(info):
                        # TODO
                        pass  
                webpage.__setattr__(field, info)
                webpage.save(update_fields=(field,))
    if was_updated:
        return update_endnotes(webpage)

    return data.strip(., )
    if url:
        return cleaned_data
    return cleaned_data.title()

        else:
        print(form.errors)
        # TODO
        return JsonResponse({"message": "error"})
"""
"""

@post_request_required
@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_info(request, source_id):

    form = get_type_of_source_form(request.POST, alter_source=True)
    if not form:
        return JsonResponse({"message": "error"})

    if form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Alter and save source obj
        alter_source(source, form)

        link = reverse("bookshelf:source_space", args=(source_id,))
        return redirect(link)

    else:
        print(form.errors)
        # TODO
        pass

        new_space = form.save_work_space(request.user)
        new_space.create_dir()
        display_success_message(request)

        
    #invitation = check_invitation(space_code)



    #original_space = invitation.work_space
    #original_sources = original_space.sources.all()

    # copy all sources (see stack overflow!)
    # friendly_dir but for these func!

    #copied_space = create_new_space(request.user, f"Copied from {original_space.owner}")



def copy_source_file(source: Source, new_space: WorkSpace, new_owner_id: int) -> str:
    '''Returns a new path to the copied file'''
    space_path = new_space.get_base_dir()
    source_id, user_id = source.pk, new_owner_id
    filename = source.file_name()
    return f"{space_path}/books/user_{user_id}/source_{source_id}/{filename}"

    if source.file:
        source.file = copy_source_file(source, new_space, new_owner.pk)
    source.save(update_fields=("file",))




"""


