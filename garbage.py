"""
<script src="{% static 'js/profile_page.js' %}"></script>

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


def copy_source(source: Source, new_space: WorkSpace, new_owner: User) -> Source:


    # Go down to source child obj
    source_type = source.cast()
    match source_type:
        case Book():
            source = source.book
        case Article():
            source = source.article
        case Chapter():
            source = source.chapter
        case Webpage():
            source = source.webpage
        case _:
            return None
        
    # Copy the given source and alter its key fields
    source.pk, source.id = None, None
    source.work_space, source.user = new_space, new_owner
    source._state.adding = True
    source.save()

    # Change file info, if file was uploaded
    if source.file:
        source.file = copy_source_file_info(source, new_space, new_owner.pk)
    source.save(update_fields=("file",))

    # Create new Endnote obj based on new source
    save_endnotes(source)
    return source


def copy_source_file_info(source: Source, new_space: WorkSpace, new_owner_id: int) -> str:

    space_path = new_space.get_base_dir()
    source_id, user_id = source.pk, new_owner_id
    filename = source.file_name()
    return f"{space_path}/sources/user_{user_id}/source_{source_id}/{filename}"



def copy_source_quotes(source: Source, new_source: Source):

    pass


        def save_file(self, source: Source):
       '''Save new source-file'''
       source.file = self.cleaned_data["file"]
       source.save(update_fields=("file",))

       @paper_authorship_required
@login_required(redirect_field_name=None)
def get_all_published_papers(request):
    '''Return all papers marked as published to show display them at the account page'''

    # The fuck is that?

    papers = Paper.objects.filter(user=request.user, is_published=True)

    if not papers:
        return JsonResponse({"message": "none"})

    files = [paper.get_last_file_id() for paper in papers]
    # TODO
    pass
    
    os.path.join(self.get_path(), os.path.basename(self.file.name))
        return f"{self.paper.get_path()}/{self.get_saving_time()}"

        return f"{space_path}/papers/user_{user_id}/paper_{paper_id}/{saving_time}/{filename}"

        return f"{self.work_space.get_path()}/sources/user_{self.user.pk}/source_{self.pk}"

        return f"{space_path}/sources/user_{user_id}/source_{source_id}/{filename}"

        return f"{self.work_space.get_path()}/papers/user_{self.user.pk}/paper_{self.pk}"

        return f"{MEDIA_ROOT}/work_space_{self.pk}"

        return f"{FRIENDLY_TMP_ROOT}/{self.pk}"

        def profile_page_view(request, user_id):
    # TODO

    user = check_user(user_id)

    pass


@login_required(redirect_field_name=None)
def follow_profile_page(request, user_id):


    profile_user, user = check_user(user_id), request.user

    # Error case (if user is trying to follow themself)
    if profile_user == user:
        # Redirect back to profile page
        return_link = reverse("user_management:profile_page", args=(user_id,))
        return redirect(return_link)
    
    # Follow / unfollow profile user
    if user in profile_user.followers.all():
        profile_user.unfollow(user)
        status = "not followed"
    else:
        profile_user.follow(user)
        status = "followed"

    return JsonResponse({"status": status, "number_of_followers": len(profile_user.followers.all())})


    class User(AbstractUser):
    profile_page_is_opened = models.BooleanField(default=True)
    followers = models.ManyToManyField("self")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def follow(self, follower):

        return self.followers.add(follower)
    
    
    def unfollow(self, follower):

        return self.followers.remove(follower)


        

            def add_source(self, source: Source):
        '''Adds new source to the paper'''
        return self.sources.add(source)


        @paper_authorship_required
@login_required(redirect_field_name=None)
def clear_file_history(request, paper_id):
    '''Delete all files related to given paper'''

    # Check if user has right to delete all files
    paper = check_paper(paper_id, request.user)

    # Delete paper directory with all files inside
    shutil.rmtree(paper.get_path())

    # Recreate new empty directory
    paper.create_directory()

    # Remove files from the db
    PaperVersion.objects.filter(paper=paper).delete()

    return JsonResponse({"message": "ok"})

        def finish(self):
        self.finished = True
        return self.save(update_fields=("finished",))


        @paper_authorship_required
@login_required(redirect_field_name=None)
def finish_paper(request, paper_id):
    '''Mark given paper as finished'''

    # Mark paper as finished
    paper = check_paper(paper_id, request.user)
    paper.finish()

    # Do I need it?

    # Is that it?
    return JsonResponse({"message": "ok"})

        path("finish_paper/<int:paper_id>", views.finish_paper, name="finish_paper"),


    link = reverse("paper_work:paper_space", args=(paper_id,))
    return redirect(link)


    @post_request_required
@login_required(redirect_field_name=None)
def leave_comment(request, space_id):


    form = NewCommentForm(request.POST)

    if form.is_valid():
        # Create new comment obj
        space = check_work_space(space_id, request.user)
        form.save_comment(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("work_space:space_view", args=(space.pk,))
    return redirect(link)


@comment_authorship_required
@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):


    # Check comment and if user has right to its deletion
    comment = check_comment(comment_id, request.user)

    # Delete comment from the db
    comment.delete()

    link = reverse("work_space:space_view", args=(comment.work_space.pk,))
    return redirect(link)


@post_request_required
@comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):


    form = AlterCommentForm(request.POST)

    if form.is_valid():
        comment = check_comment(comment_id, request.user)
        form.save_altered_comment(comment)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("work_space:space_view", args=(comment.work_space.pk,))
    return redirect(link)

    @post_request_required
@space_ownership_required
@login_required(redirect_field_name=None)
def set_citation_style(request, space_id):
    
    form = CitationStyleForm(request.POST)

    if form.is_valid():
        space = check_work_space(space_id, request.user)
        form.save_citation_style(space)
        display_success_message(request)
    else:
        display_error_message(request)
    
    link = reverse("work_space:space_view", args=(space_id,))
    return redirect(link)


    def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("website:index"))
        else:
            return render(request, "user_management/login.html", {
                "message": "Invalid username and/or password."})
    else:
        return render(request, "user_management/login.html", {"login_form": form})


     # Save the previos url to redirect to it after submitting the form
    redirect_url = request.GET.next
    if redirect_url:
       form = form.set_redirect_url(redirect_url)
       print(redirect_url)

       class LoginForm(forms.Form):
    redirect_url = forms.CharField(required=False, widget=forms.HiddenInput(attrs={"name": "redirect_url"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def set_redirect_url(self, url: str):
        self.fields["redirect_url"].value = url
        return self

    <form onsubmit="return check_password('register_form');" action="{% url 'user_management:register' %}" id="register_form" method="post">
        {% csrf_token %}
        <div class="form-group">
            <input class="form-control" autofocus type="text" name="username" placeholder="Username">
        </div>
        <div class="form-group">
            <input class="form-control" autofocus type="text" name="first_name" placeholder="First Name">
        </div>
        <div class="form-group">
            <input class="form-control" autofocus type="text" name="last_name" placeholder="Last Name">
        </div>
        <div class="form-group">
            <input class="form-control" type="email" name="email" placeholder="Email Address">
        </div>
        <div class="form-group">
            <input class="form-control" type="password" name="password" placeholder="Password">
        </div>
        <div class="form-group">
            <input class="form-control" type="password" name="confirmation" placeholder="Confirm Password">
        </div>
        <input class="btn btn-primary" type="submit" value="Register">
    </form>

    {% extends "layout.html" %}
{% load static %}

{% block body %}

    <style>
        .two_2, .three, .four, .five
        {
            display: none;
        }
    </style>

    <script>
         document.addEventListener('DOMContentLoaded', function() {


            const one_button = document.getElementById('one_button');

            one_button.addEventListener('click', function() {

                let new_div = document.getElementsByClassName('two_2')[0];
                console.log(new_div);

                new_div.style.display = 'block';

            })
            

    









        });
    </script>


    <br>
    <form action="{% url 'lobby:lobby' %}" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Send</button>
    </form><br><br>

    <h3>New:</h3>
    <form action="{% url 'lobby:lobby' %}" method="post">

        
        <div class="one">
            <label for="id_one">One:</label>
            <input id="one" type="text" required>
            <button type="button" id="one_button">Add</button>
        </div>
        <div class="two_2">
            <label for="id_two">Two:</label>
            <input id="two" type="text" required>
            <button id="two_button">Add</button>
        </div>
        <div class="three">
            <label for="id_three">Three:</label>
            <input id="three" type="text" required>
            <button id="three_button">Add</button>
        </div>


        <button type="submit">Send</button>
    </form>
    


{% endblock %}

{% block script %}
    <script src="{% static 'user_management/script.js' %}"></script>
{% endblock %}


def quote_book_apa(book: Book) -> str:

    author = format_authors_apa(book.author)
    return f"{author} ({book.year}). {book.title}. {book.publishing_house}."


def quote_article_apa(article: Article) -> str:
    "Create apa endnote for given article"
    author = format_authors_apa(article.author)
    result: str = (
        f'{author} ({article.year}). "{article.title}" {article.journal_title}, '
        f'{article.volume}({article.issue}), {article.pages}.'
    )
    return result


def quote_chapter_apa(chapter: Chapter) -> str:

    book_author = format_authors_apa(chapter.book_author)
    chapter_author = format_authors_apa(chapter.author)
    result: str = (
        f"{chapter_author} ({chapter.year}). {chapter.title}. "
        f"In {book_author} (Eds.), {chapter.book_title} "
        f"({chapter.edition} ed., pp. {chapter.pages}). {chapter.publishing_house}."
    )
    return result


def quote_webpage_apa(webpage: Webpage) -> str:

    date = format_date(webpage.date, "apa")
    if webpage.author == "No author":
        return f"{webpage.title}. ({date}). {webpage.website_title}. {webpage.page_url}"
    
    author = format_authors_apa(webpage.author)
    return f"{author} ({date}). {webpage.title}. {webpage.website_title}. {webpage.page_url}"

    def quote_book_mla(book: Book) -> str:

    author = format_authors_mla(book.author)
    return f"{author} {book.title}. {book.publishing_house}, {book.year}."


def quote_article_mla(article: Article) -> str:

    author = format_authors_mla(article.author)
    result: str = (
        f'{author} "{article.title}" {article.journal_title}, vol. {article.volume}, '
        f'no. {article.issue}, {article.year}, pp. {article.year}.'
    )
    return result


def quote_chapter_mla(chapter: Chapter) -> str:

    book_author = format_authors_mla(chapter.book_author)
    chapter_author = format_authors_mla(chapter.author)
    result: str = (
        f'{chapter_author}. "{chapter.title}." {chapter.book_title}, edited by {book_author}. '
        f'{chapter.publishing_house}, {chapter.year}, pp. {chapter.pages}.'
    )
    return result


def quote_webpage_mla(webpage: Webpage) -> str:

    date = format_date(webpage.date, "mla")
    if webpage.author == "No author":
        return f'"{webpage.title}" {webpage.website_title}, {date}, {webpage.page_url}.'
    
    author = format_authors_mla(webpage.author)
    return f'{author}. "{webpage.title}" {webpage.website_title}, {date}, {webpage.page_url}.'


    from typing import Callable
from .dates import format_date
from .models import Article, Book, Chapter, Source, Webpage

from quoting.author_formatting import format_authors_mla


def quote_source_mla(source: Source) -> Callable | bool:


    source_type: type(object) = source.cast()
    match source_type:
        case Book():
            return quote_book_mla(source.book)
        case Article():
            return quote_article_mla(source.article)
        case Chapter():
            return quote_chapter_mla(source.chapter)
        case Webpage():
            return quote_webpage_mla(source.webpage)
        case _:
            return None

        if request.method == "POST":
        form = get_type_of_source_form(request.POST)
        if not form:
            display_error_message(request)
            # TODO
            return JsonResponse({"message": "error"})
        
        if form.is_valid():

            pass

        else:
            display_error_message(request)

                if not form:
        display_error_message()
        # TODO
        return JsonResponse({"message": "error"})


        @space_ownership_required
@login_required(redirect_field_name=None)
def share_work_space(request, space_id):

    # TODO

    # What should it be instead of json? probably url with some nice text

    space = check_work_space(space_id, request.user)
    if space.sources.all():
        share_space_code = generate_invitation(space)
        return JsonResponse({"share_space_code": share_space_code})
    else:
        return JsonResponse({"message": "You can not share empy work space"})


@post_request_required
@login_required(redirect_field_name=None)
def receive_shared_space(request):

    # TODO

    form = ReceiveCodeForm(request.POST)

    if form.is_valid():
        share_space_code = check_share_code(form.cleaned_data["code"])

        # Create a new work space
        original_work_space = share_space_code.work_space
        new_space = copy_space_with_all_sources(original_work_space, request.user)

        # Redirect to the new work space
        display_success_message(request)
        link = reverse("work_space:space_view", args=(new_space.pk,))
        return redirect(link)

    display_error_message(request)
    return redirect(ERROR_PAGE)

    def create_friendly_directory(work_space: WorkSpace) -> str | bool:
    '''Creates user-friendly directory for future zip-archiving and downloading''''''

    # Get all sources and papers in given work space
    papers, sources, comments = work_space.papers.all(), work_space.sources.all(), work_space.comments.all()
    if not papers and not sources:
        # In case work space is empty
        return False
        
    # Create new empty directory
    work_space.create_friendly_dir()
    original_path = work_space.get_friendly_path()
    root_path = os.path.join(original_path, work_space.title)

    if papers:
        # Create new "papers" dir
        papers_root = os.path.join(root_path, "papers")
        os.makedirs(papers_root, exist_ok=True)

        # Get all users
        authors = [paper.user for paper in papers]
        for author in authors:
            if len(set(authors)) != 1:
                # Create new "user" dirs inside "papers" dir if there are multiple users
                author_name = f"{author.last_name} {author.first_name}"
                author_root = os.path.join(papers_root, author_name)
                os.makedirs(author_root, exist_ok=True)
            else:
                # Don't create author dir if there is only one user
                author_root = papers_root

            # Get all user papers
            author_papers = papers.filter(user=author)
            for author_paper in author_papers:
                # Create new "paper" dirs inside "user" dir
                path_to_paper = os.path.join(author_root, author_paper.title)
                os.makedirs(path_to_paper, exist_ok=True)

                # Get all paper-related files
                versions = author_paper.versions.all()
                for version in versions:
                    # Create new "paper-file" dirs inside "paper" dir
                    path_to_paper_version = os.path.join(path_to_paper, version.get_saving_time())
                    os.makedirs(path_to_paper_version, exist_ok=True)

                    # Copy original paper file into new "paper-file" dir
                    destination = os.path.join(path_to_paper_version, version.file_name())
                    original_file = version.get_path_to_file()
                    shutil.copyfile(original_file, destination)
                    
    if sources:
        # Create new "books" dir
        books_root = os.path.join(root_path, "books")
        os.makedirs(books_root, exist_ok=True)

        # Get, quote and sort alphabetically all sources
        sources_apa = sorted([get_endnotes(source).apa for source in sources])
        sources_mla = sorted([get_endnotes(source).mla for source in sources])

        # Get paths to new .txt files
        apa_file_path = os.path.join(books_root, "books_apa.txt")
        mla_file_path = os.path.join(books_root, "books_mla.txt")

        # Create two new .txt files
        with open(apa_file_path, "w") as apa_file, open(mla_file_path, "w") as mla_file:
            source_counter = 1
            for i in range(len(sources)):
                # Write sources arrays into both files
                apa_file.write(f"{source_counter}. {sources_apa[i]}\n\n")
                mla_file.write(f"{source_counter}. {sources_mla[i]}\n\n")
                source_counter += 1

        # Get array with only sources which files were uploaded
        sources_with_files = [source for source in sources if source.file]

        if any(sources_with_files):
            # Create new "sources-files" dir
            sources_files_root = os.path.join(books_root, "files")
            os.makedirs(sources_files_root, exist_ok=True)

            for source in sources_with_files:
                # Copy original source file into new "sources-file" dir
                destination = os.path.join(sources_files_root, source.file_name())
                original_file = source.get_path_to_file()
                shutil.copyfile(original_file, destination)

        # Get array with only sources with quotes
        sources_with_quotes = [source for source in sources if source.quotes.all()]

        if any(sources_with_quotes):
            # Get paths to new .txt file
            quotes_file = os.path.join(books_root, "quotes.txt")

            # Create file and write in all quotes
            with open(quotes_file, "w") as file:
                for source in sources_with_quotes:
                    # Write every source title
                    file.write(f"\t{source}\n\n\n")
                    source_quotes = source.quotes.all()
                    # Write all its quotes
                    for quote in source_quotes:
                        file.write(f"{quote}\n\n")
                    file.write("\n\n")
    if comments:
        # Get path to new comments.txt file
        comments_file_path = os.path.join(root_path, "comments.txt")

        # Create file and write in all comments
        with open(comments_file_path, "w") as comment_file:
            for comment in comments:
                comment_file.write(f"{comment}\n\n")

    # Return path to the whole dir
    return original_path

            if option == "download":
            # Add user to space in order to download it
            original_work_space.add_guest(request.user)
            donwload_url = reverse("work_space:download_space", args=(original_work_space.pk,))
            try:
                return redirect(donwload_url)
            finally:
                # Delete user form space after downloading its sources
                #original_work_space.remove_guest(request.user)
                print("success!")

@post_request_required
@comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):


    form = AlterCommentForm(request.POST)

    if form.is_valid():
        comment = check_comment(comment_id, request.user)
        form.save_altered_comment(comment)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(comment.work_space.pk,)))

    @note_authorship_required
@login_required(redirect_field_name=None)
def alter_note(request, note_id):

    
    form = AlterNoteForm(request.POST)

    if form.is_valid():
        note = check_note(note_id, request.user)
        form.save_altered_note(note)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(note.work_space.pk,)))

                <button onclick="return alter_comment('{{ comment.pk }}')" type="button">Alter Comment</button>


    @link_ownership_required
@login_required(redirect_field_name=None)
def alter_link(request, link_id):


    form = AlterLinkForm(request.POST)

    if form.is_valid():
        link = check_space_link(link_id, request.user)
        form.save_altered_link(link)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(link.work_space.pk,)))


    @comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):

    form = AlterCommentForm(request.POST or None)
    comment = check_comment(comment_id, request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save_altered_comment(comment)
            return JsonResponse({"status": "ok", "comment": comment})
        else:
            return JsonResponse({"status": "error"})
        
    return HttpResponse(form.set_initial(comment).as_p())

    author_papers = papers.filter(user=author)


    def create_friendly_papers_dir(papers, users, root_path: str) -> None:
    
    papers_root = os.path.join(root_path, "papers")
    os.makedirs(papers_root, exist_ok=True)

    # Get all users
    authors = [paper.user for paper in papers]
    
    for author in authors:
        if len(set(authors)) != 1:
            # Create new "user" dirs inside "papers" dir if there are multiple users
            author_name = f"{author.last_name} {author.first_name}"
            author_root = os.path.join(papers_root, author_name)
            os.makedirs(author_root, exist_ok=True)
        else:
            # Don't create author dir if there is only one user
            author_root = papers_root

        # Get all user papers
        author_papers = [paper for paper in papers if paper.user == author]
        for author_paper in author_papers:
            # Create new "paper" dirs inside "user" dir
            path_to_paper = os.path.join(author_root, author_paper.title)
            os.makedirs(path_to_paper, exist_ok=True)

            # Get all paper-related files
            versions = author_paper.versions.all()
            for version in versions:
                # Create new "paper-file" dirs inside "paper" dir
                path_to_paper_version = os.path.join(path_to_paper, version.get_saving_time())
                os.makedirs(path_to_paper_version, exist_ok=True)

                # Copy original paper file into new "paper-file" dir
                destination = os.path.join(path_to_paper_version, version.file_name())
                original_file = version.get_path_to_file()
                shutil.copyfile(original_file, destination)    


                @post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):


    form = PaperPublicationForm(request.POST)

    if form.is_valid():
        # Check if user has right to publish this paper
        paper = check_paper(paper_id, request.user)

        # Check if paper file wsa uploaded
        if paper.get_number_of_files() != 0:
            # Publish paper
            paper.publish()
    
            if form.cleaned_data["share_sources"] == True:
                # TODO ! What after?
                return redirect(reverse("work_space:share_space", args=(paper.work_space.pk,)))
            
            display_success_message(request)
        else:
            display_error_message(request, "no files were uploaded")
    else:
        display_error_message(request)

    # Redirect to profile page
    return redirect(reverse("profile_page:profile_view", args=(get_profile_id(request.user),)))  

    class PaperPublicationForm(forms.Form):
    share_sources = forms.BooleanField()

    # TODO?


    def generate_invitation(space: WorkSpace, invite=False) -> str:
    
    # Make sure invitation texts never repeat
    while True:
        # Generate random string
        invitation_code = "".join([SystemRandom().choice(POPULATION) for _ in range(LENGTH_OF_STRING)])
        try:
            if invite:
                code_obj = Invitation(code=invitation_code, work_space=space)
            else:
                # TODO
                code_obj = ShareSourcesCode(code=invitation_code, work_space=space)
                space.share_sources = True
                space.save(update_fields=("share_sources",))

        except IntegrityError:
            # Generate new code in case of repetition
            continue
        else:
            code_obj.save()
            return invitation_code


            @post_request_required
@login_required(redirect_field_name=None)
def leave_comment(request, space_id):


    form = NewCommentForm(request.POST)

    if form.is_valid():
        # Create new comment obj
        space = check_work_space(space_id, request.user)
        new_comment = form.save_comment(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)

    return redirect(reverse("work_space:space_view", args=(space.pk,)))


    @login_required(redirect_field_name=None)
def leave_note(request, space_id):


    form = NewNoteForm(request.POST)

    if form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        form.save_note(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(space.pk,)))


    @login_required(redirect_field_name=None)
def add_link(request, space_id):


    form = NewLinkForm(request.POST)

    if form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        form.save_link(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(space.pk,)))


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
        display_success_message(request)
    else:
        display_error_message(request)
        
    return redirect(reverse("bookshelf:source_space", args=(source_id,)))


    @login_required(redirect_field_name=None)
def set_source_endnotes(request, source_id):
    # TODO
    

    pass
    
    <a href="{% url 'bookshelf:delete_quote' quote.pk %}">Delete quote</a>

    def check_endnote(endnote_id: int, user: User) -> Endnote | Http404:

    try:
        endnote = Endnote.objects.get(pk=endnote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(endnote.source.work_space.pk, user)
    return endnote


    def endnote_ownership_required(func: Callable) -> Callable | PermissionDenied:

    def wrapper(request, endnote_id):
        endnote = check_endnote(endnote_id, request.user)
        if endnote.source.user != request.user:
            raise PermissionDenied
        return func(request, endnote_id)
    return wrapper

    
    action="{% url 'user_management:reset_password' reset_code %}"

                    user = authenticate(request, username=request.user.username, password=request.user.password)
                if user and new_password == confirmation:
                

form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "first_form"}))

document.addEventListener('DOMContentLoaded', function() {

    const change_form_button = document.querySelector('#change_forms_button');

    change_form_button.addEventListener('click', () => change_forms(change_form_button))

});


class ForgetPasswordForm(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "first_form"}))
    username = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    

class ForgetPasswordForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)
    
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "second_form"}))


    def check_forget_password_form_data(request) -> Callable | None:


    if "first_form" in request.POST["form_type"]:
        print("first_form")
        return check_first_form_data(ForgetPasswordForm(request.POST), request.user)
    if "second_form" in request.POST["form_type"]:
        return check_second_form_data(ForgetPasswordForm2(request.POST), request.user)
    return None

def check_first_form_data(form: ForgetPasswordForm, user: User) -> bool:

    if form.is_valid():
        if form.cleaned_data["username"] == user.username:
            return True
    return False


def check_second_form_data(form: ForgetPasswordForm2, user: User) -> bool:

    if form.is_valid():
        if form.cleaned_data["first_name"] != user.first_name:
            return False
        if form.cleaned_data["last_name"] != user.last_name:
            return False
        if form.cleaned_data["email"] != user.email:
            return False
    return True

    
    def check_forget_password_form_data(request) -> Callable | None:


    if "first_form" in request.POST["form_type"]:
        return check_first_form_data(ForgetPasswordForm(request.POST), request.user)
    if "second_form" in request.POST["form_type"]:
        return check_second_form_data(ForgetPasswordForm2(request.POST), request.user)
    return None

def check_first_form_data(form: ForgetPasswordForm, user: User) -> bool:

    if form.is_valid():
        return check_user_by_username(form.cleaned_data["username"], form.cleaned_data["email"])
    return False


def check_second_form_data(form: ForgetPasswordForm2, user: User) -> bool:

    if form.is_valid():
        return check_user_by_name(form.cleaned_data["first_name"], form.cleaned_data["last_name"], form.cleaned_data["email"])
    return False



    class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs=ATTRS))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs=ATTRS))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs=ATTRS))

    
def confirm_email(request, email_code):

    
    user = get_user_buy_email_code(email_code)
    email_code_obj = check_email_confirmation_code(email_code, user)
    if not email_code_obj:
        # Error case (wrong reset code)
        display_error_message(request, "This url is no longer valid")
        return redirect(LOGIN_URL)


    # Do I need it?
    # Delete!


def check_email_confirmation_code(email_code: str, user: User) -> EmailConformationCode | None:

    try:
        return EmailConformationCode.objects.get(code=email_code, user=user)
    except ObjectDoesNotExist:
        return None

        
        def get_user_buy_email_code(code: str) -> User | None:

    try:
        return EmailConformationCode.objects.get(code=code).user
    except ObjectDoesNotExist:
        return None
            path("email_conformation/<str:email_code>", views.confirm_email, name="confirm_email")


            function redirect(url) {
    // Imitate django redirect func
    window.location.replace(url)
}

function handleErrors(response, url) {
    if (!response.ok) {
        if (response.statusText === 'Forbidden') {
            redirect(url)
        }

        // TODO: other errors 
    }
    return response;
}


export { redirect }
export { handleErrors }

*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}
body{
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #c1f7f5;
}


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    # Delete later
    
    source = check_source(source_id, request.user)
    quotes = source.quotes.all()

    endnotes = get_endnotes(source)

    endnote_form = AlterEndnoteForm().set_initials(endnotes)

    upload_form = UploadSourceForm()
    quote_form = NewQuoteForm()
    link_form = AddLinkForm()

    alter_form = get_and_set_alter_form(source)
    
    return render(request, "bookshelf/source_space.html", {"source": source, 
                                                         "upload_form": upload_form, 
                                                         "alter_form": alter_form, 
                                                         "quote_form": quote_form,
                                                         "quotes": quotes,
                                                         "endnotes": endnotes,
                                                         "endnote_form": endnote_form,
                                                         "link_form": link_form})



@login_required(redirect_field_name=None)
def test_source_space(request, source_id):
    # Delete later

    source = check_source(source_id, request.user)
    endnotes = get_endnotes(source)

    source_data = {
            "source": model_to_dict(source),
            "quotes": source.quotes.all(),
            "endnotes": endnotes,
            "alter_source_form": get_and_set_alter_form(source),
            "upload_file_form": UploadSourceForm(),
            "link_form": AddLinkForm(),
            "new_quote_form": NewQuoteForm(),
            "alter_endnotes_form": AlterEndnoteForm().set_initials(endnotes)
    }

    return JsonResponse(source_data)

    @login_required(redirect_field_name=None)
def paper_space(request, paper_id):

    # TODO

    # Delete later?

    paper = check_paper(paper_id, request.user)

    all_sources = paper.work_space.sources.all()

    sources_form = ChooseSourcesForm().set_initials(all_sources)

    paper_versions = PaperVersion.objects.filter(paper=paper).order_by("saving_time")

    endnotes = sorted([get_endnotes(source) for source in paper.sources.all()])

    links = [reverse("file_handling:display_file", args=(version.pk,)) for version in paper_versions]

    # TODO

    return render(request, "paper_work/paper_space.html", {"form": NewPaperVersionForm(), 
                                                           "paper": paper, "paper_versions": paper_versions, 
                                                           "links": links, "rename_form": RenamePaperForm(),
                                                           "citation_form": CitationStyleForm(),
                                                           "sources_form": sources_form,
                                                           "endnotes": endnotes})


                                                           

                                                           import os
from django.db import models 
from django.contrib.contenttypes.models import ContentType
from research_engine.settings import MEDIA_ROOT
from user_management.models import User
from work_space.models import WorkSpace


def saving_path(instance, filename):
 
    space_path = instance.work_space.get_base_dir()
    user_id, source_id = instance.user.pk, instance.pk
    return os.path.join(space_path, "sources", f"user_{user_id}", f"source_{source_id}", filename)


class Source(models.Model):

    real_type = models.ForeignKey(ContentType, editable=False, on_delete=models.CASCADE)
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="sources")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sources")
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=70, blank=True)
    year = models.CharField(max_length=5, blank=True)
    file = models.FileField(upload_to=saving_path, blank=True)
    link = models.CharField(max_length=40, blank=True)
    

    def __str__(self):
        '''Display book title'''
        return self.title


    def save(self, *args, **kwargs):
  
        if self._state.adding:
            self.real_type = self.get_real_type()
        return super(Source, self).save(*args, **kwargs)


    def get_real_type(self):

        return ContentType.objects.get_for_model(type(self))
    

    def cast(self):

        return self.real_type.get_object_for_this_type(pk=self.pk)
    

    def file_name(self):

        return os.path.basename(self.file.name)
    

    def get_path(self):

        return os.path.join(self.work_space.get_path(), "sources", f"user_{self.user.pk}", f"source_{self.pk}")


    def get_path_to_file(self):

        if self.file:
            return os.path.join(MEDIA_ROOT, str(self.file))
        else:
            return None

            @post_request_required
@login_required(redirect_field_name=None)
def upload_source_file(request, source_id):


    form = UploadSourceForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        source = check_source(source_id, request.user)

        # In case user already uploaded a file - delete it first
        if source.file:
            shutil.rmtree(source.get_path())
        # Upload file
        source.file = request.FILES["file"]
        source.save(update_fields=("file",))
        display_success_message(request)
    else:
        display_error_message(request)

    # TODO
    return redirect(reverse("bookshelf:source_space", args=(source_id,)))


@login_required(redirect_field_name=None)
def display_source_file(request, source_id):

    # Get and check source
    source = check_source(source_id, request.user)

    source_file = source.get_path_to_file()
    if not source_file:
        display_error_message(request, "no file was uploaded")
        return redirect(reverse("bookshelf:source_space", args=(source_id,)))
    
    # Open source file and send it
    return FileResponse(open(source_file, "rb"))

    from django.contrib.auth.forms import UserCreationForm
    class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    @post_request_required
@login_required(redirect_field_name=None)
def add_source(request, space_id):

    
    # TODO
    # instead of redirecting to space view - load it with js and open its modal window

    # Figure out which of four forms was uploaded
    form = get_type_of_source_form(request.POST)
    
    if form and form.is_valid():
        space = check_work_space(space_id, request.user)

        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            # Error case
            pass
        else:
            if type(form) == ChapterForm:
                chapter_author = clean_author_data(request.POST, chapter_author=True)
                if not chapter_author:
                    # Error case
                    pass
                else:
                    display_success_message(request)
                    new_source_pk = create_source(request.user, space, form, author, chapter_author=chapter_author)
                    return redirect(reverse("bookshelf:source_space", args=(new_source_pk,)))
            else:
                display_success_message(request)
                new_source_pk = create_source(request.user, space, form, author)
                return redirect(reverse("bookshelf:source_space", args=(new_source_pk,)))

    # Redirect back to work space
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})
    return redirect(reverse("work_space:space_view", args=(space_id,)))



    @post_request_required
@login_required(redirect_field_name=None)
def create_paper(request, space_id):
    
    form = NewPaperForm(request.POST)

    if form.is_valid():
        # Save new paper to db
        space = check_work_space(space_id, request.user)
        new_paper = form.save_paper(space, request.user)
        display_success_message(request)

        # Redirect user to the new paper-space
        return redirect(reverse("paper_work:paper_space", args=(new_paper.pk,)))
    
    display_error_message(request)
    return JsonResponse({"status": "ok", "url": reverse("work_space:space_view", args=(space_id,))})
    return redirect(reverse("work_space:space_view", args=(space_id,)))



    # Do I need this?
    class FieldClass:
    book_class = "book"
    article_class = "article"
    chapter_class = "chapter"
    webpage_class = "webpage"
    


    class AlterBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = EXCLUDE_FIELDS
    
    source_type = SourceTypes.book

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
    
    source_type = SourceTypes.article

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

    source_type = SourceTypes.chapter

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

    source_type = SourceTypes.webpage

    def set_initials(self, webpage: Webpage):
        for field in self.fields:
            if field != "source_type":
                self.fields[field].initial = webpage.__getattribute__(field)
        return self


        EXCLUDE_FIELDS = ("user", "work_space", "real_type", "file", "link",)


    class Endnote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    apa = models.CharField(max_length=50)
    mla = models.CharField(max_length=50)

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import Endnote, Source
from .source_citation import make_source_endnote_apa, make_source_endnote_mla


def create_endnotes(source: Source):

    endnotes = Endnote(source=source, apa=make_source_endnote_apa(source), mla=make_source_endnote_mla(source))
    return endnotes.save()


def update_endnotes(source: Source):

    endnotes = get_endnotes(source)
    endnotes.apa = make_source_endnote_apa(source)
    endnotes.mla = make_source_endnote_mla(source)
    return endnotes.save(update_fields=("apa", "mla",))


def get_endnotes(source: Source) -> Endnote | Http404:

    try:
        return Endnote.objects.get(source=source)
    except ObjectDoesNotExist:
        raise Http404


class Endnote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    apa = models.CharField(max_length=50)
    mla = models.CharField(max_length=50)

    
    class Comment(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    reply_to = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def get_creation_time(self):

        return self.created.strftime(SAVING_TIME_FORMAT)


    def __str__(self):

        if self.work_space.guests.all():
            return f'{self.user}: "{self.text}" ({self.get_creation_time()})'
        return f'"{self.text}" ({self.get_creation_time()})'


class Note(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="notes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=50)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.text


        @post_request_required
@login_required(redirect_field_name=None)
def leave_comment(request, space_id):

    
    form = NewCommentForm(request.POST)

    if form and form.is_valid():
        # Create new comment obj
        space = check_work_space(space_id, request.user)
        new_comment = form.save_comment(space, request.user)
        return JsonResponse({"status": "ok", "comment": model_to_dict(new_comment)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})


@post_request_required
@comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):


    form = AlterCommentForm(request.POST)
    comment = check_comment(comment_id, request.user)

    if form and form.is_valid():
        altered_comment = form.save_altered_comment(comment)
        return JsonResponse({"status": "ok", "altered_comment": model_to_dict(altered_comment)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(comment.work_space.pk,))})


@comment_authorship_required
@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):


    # Check comment and delete it from the db
    comment = check_comment(comment_id, request.user)
    comment.delete()
    return JsonResponse({"status": "ok"})


@post_request_required
@login_required(redirect_field_name=None)
def leave_note(request, space_id):


    form = NewNoteForm(request.POST)

    if form and form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        new_note = form.save_note(space, request.user)
        return JsonResponse({"status": "ok", "new_note": model_to_dict(new_note)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})


@post_request_required
@note_authorship_required
@login_required(redirect_field_name=None)
def alter_note(request, note_id):
  
    
    form = AlterNoteForm(request.POST)
    note = check_note(note_id, request.user)

    if form and form.is_valid():
        altered_note = form.save_altered_note(note)
        return JsonResponse({"status": "ok", "altered_note": model_to_dict(altered_note)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(note.work_space.pk,))})


@note_authorship_required
@login_required(redirect_field_name=None)
def delete_note(request, note_id):


    # Check note and delete it from the db
    note = check_note(note_id, request.user)
    note.delete()
    return JsonResponse({"status": "ok"})


    def comment_authorship_required(func: Callable) -> Callable | PermissionDenied:

    def wrapper(request, comment_id):
        comment = check_comment(comment_id, request.user)
        if comment.user != request.user:
            raise PermissionDenied
        return func(request, comment_id)
    return wrapper


def note_authorship_required(func: Callable) -> Callable | PermissionDenied:

    def wrapper(request, note_id):
        note = check_note(note_id, request.user)
        if note.user != request.user:
            raise PermissionDenied
        return func(request, note_id)
    return wrapper


    def check_comment(comment_id: int, user: User) -> Comment | Http404:

    try:
        comment = Comment.objects.get(pk=comment_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(comment.work_space.pk, user)
    return comment


def check_note(note_id: int, user: User) -> Note | Http404:

    try:
        note = Note.objects.get(pk=note_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(note.work_space.pk, user)
    return note

    
    def create_friendly_notes_dir(notes, authors: list, root_path: str) -> None:


    notes_root = os.path.join(root_path, "notes")
    os.makedirs(notes_root, exist_ok=True)

    # Get all users
    for author in authors:
        if len(authors) == 1:
            # Don't create author dir if there is only one user
            author_root = notes_root
        else:
            # Create new "user" dirs inside "notes" dir if there are multiple users
            author_name = f"{author.last_name} {author.first_name}"
            author_root = os.path.join(notes_root, author_name)
            os.makedirs(author_root, exist_ok=True)

        # Get all user notes
        author_notes = [note for note in notes if note.user == author]
        for author_note in author_notes:
            # Get path to new note .txt file
            path_to_note = os.path.join(author_root, f"{author_note.title}.txt")

            # Create file and write in note text
            with open(path_to_note, "w") as note_file:
                note_file.write(author_note.text)


def create_friendly_comments_file(comments, root_path: str) -> None:


    # Get path to new comments.txt file
    comments_file_path = os.path.join(root_path, "comments.txt")

    # Create file and write in all comments
    with open(comments_file_path, "w") as comment_file:
        for comment in comments:
            comment_file.write(f"{comment}\n\n")


            @post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):


    # Check if user has right to publish this paper
    paper = check_paper(paper_id, request.user)

    # Check if paper file wsa uploaded
    if paper.get_number_of_files() != 0:
        # Publish paper
        paper.publish()
        display_success_message(request)
    else:
        display_error_message(request, "no files were uploaded")
        # TODO redirect back

    # Redirect to profile page
    return redirect(reverse("profile_page:profile_view", args=(get_profile_id(request.user),)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def hide_published_paper(request, paper_id):


    # Check if user has right to hide this paper
    paper = check_paper(paper_id, request.user)

    # Error case
    if paper.published:
        # Mark paper as not published
        paper.unpublish()
        display_success_message(request)
    else:
        display_error_message(request)
        # TODO
        pass

    # TODO
    # Redirect back to profile page? Maybe Json would be better!
    return redirect(reverse("profile_page:profile_view", args=(get_profile_id(request.user),)))


    def profile_ownership_required(func: Callable) -> Callable | PermissionDenied:

    def wrapper(request, profile_id):
        profile_page = check_profile(profile_id)
        if profile_page.user != request.user:
            raise PermissionDenied
        return func(request, profile_id)
    return wrapper

            return JsonResponse({"status": "ok", "reference": model_to_dict(altered_reference)})


    if not file:
        display_error_message(request, "no file was uploaded")
        return redirect(reverse("bookshelf:source_space", args=(file.source.pk,)))


        def check_link(link: str) -> bool:

    try: 
        response = requests.get(link)
    except RequestException:
        return False
    else:
        return response.ok


                        elif field == "page_url":
                    if not check_link(info):
                        # TODO
                        pass
                        

        if not check_link(link):
            return False

            import requests
from requests.exceptions import RequestException


@post_request_required
@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_reference(request, source_id):

    form = AlterReferenceForm(request.POST)
    source = check_source(source_id, request.user)
    reference = get_source_reference(source)

    if form and form.is_valid():
        form.save_altered_reference(reference)
        return JsonResponse({"status": "ok"})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


class AlterReferenceForm(forms.Form):
    apa = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "apa-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "APA"})
    )

    mla = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "mla-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "MLA"})
    )

    def set_initials(self, reference: Reference):

        self.fields["apa"].initial = reference.endnote_apa
        self.fields["mla"].initial = reference.endnote_mla
        return self
        

    def save_altered_reference(self, reference: Reference) -> Reference:
        reference.endnote_apa = clean_text_data(self.cleaned_data["apa"])
        reference.endnote_mla = clean_text_data(self.cleaned_data["mla"])
        reference.save(update_fields=("endnote_apa", "endnote_mla",))
        return reference
    
        
@login_required(redirect_field_name=None)
@source_ownership_required
def delete_source_link(request, source_id):
    "Delete previously added source link"
    
    source = check_source(source_id, request.user)
    source.link = None
    source.save(update_fields=("link",))

    return JsonResponse({"status": "ok"})


    @post_request_required
@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_info(request, source_id):

    form = get_type_of_source_form(request.POST, alter_source=True)

    if form and form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Alter and save source obj
        altered_source = alter_source(source, form)
        return JsonResponse({"status": "ok", "source": model_to_dict(altered_source)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@post_request_required
@login_required(redirect_field_name=None)
def add_link_to_source(request, source_id):

    form = AddLinkForm(request.POST)

    if form and form.is_valid():
        source = check_source(source_id, request.user)
        form.save_link(source)
        return JsonResponse({"status": "ok"})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


    @post_request_required
@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_info(request, source_id):

    form = get_type_of_source_form(request.POST, alter_source=True)

    if form and form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Alter and save source obj
        altered_source = alter_source(source, form)
        return JsonResponse({"status": "ok", "source": model_to_dict(altered_source)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@post_request_required
@login_required(redirect_field_name=None)
def add_link_to_source(request, source_id):

    form = AddLinkForm(request.POST)

    if form and form.is_valid():
        source = check_source(source_id, request.user)
        form.save_link(source)
        return JsonResponse({"status": "ok"})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@login_required(redirect_field_name=None)
def render_author_form_fields(request, author_number, chapter):
    
    # Chapter parameter is boolean (0/1). In case of True: pass "chapter-" as prefix to html tag ids, classes and names
    if chapter:
       chapter = "chapter-"
    else:
        chapter = ""
    return render(request, "bookshelf/author_fields.html", {"author_number": author_number, "chapter": chapter})



    class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

    # TODO
    # Maybe regular form?

class AccountSettingsForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs=ATTRS))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs=ATTRS))
    email = forms.EmailField(widget=forms.EmailInput)


@login_required
@post_request_required
def change_password(request):

    form = ChangePasswordForm(request.POST or None)

    if request.method == "POST":
        if form and form.is_valid():
            # Get input
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            confirmation = form.cleaned_data["confirmation"]

            # Check old password and confirmation
            user = authenticate(request, username=request.user.username, password=old_password)
            if user and new_password == confirmation:
                # Update password
                user.set_password(new_password)
                user.save(update_fields=("password",))
                display_success_message(request, "Password was successfully updated!")
                return redirect(LOGIN_URL)
            
        # Redirect back in case of error
        display_error_message(request)
        return redirect(reverse("user_management:change_password"))
    
    return render(request, "user_management/change_password.html", {"change_password_form": form})


ATTRS = {"class": "form-control", "autocomplete": "off"}

        # Error case
        display_error_message(request)
        return redirect(reverse("user_management:account_settings"))


                  display_success_message(request, "Account details were successfully updated!")
                return redirect(LOGIN_URL)


    def validate_date(date: str) -> bool:
    try:
        year, month, day = date.split("-")
    except IndexError:
        return False
    else:
        try:
            year_num, month_num, day_num = int(year), int(month), int(day)
        except ValueError:
            return False

    if len(year) != 4:
        return False
    elif int(year[0]) > 2:
        return False
    elif year_num < INTERNET_BIRTHDAY:
        return False
    elif len(month) != 2:
        return False
    elif month_num < 1 or month_num > 12:
        return False
    elif len(day) != 2:
        return False
    if day_num < 1 or day_num > 31:
        return False
    else:
        return True


class AlterLinkForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()

    def set_initial(self, link: Link):
        self.fields["name"].initial = link.name
        self.fields["url"].initial = link.url
        return self

    def save_altered_link(self, link: Link) -> Link:
        link.name = self.cleaned_data["name"]
        link.url = self.cleaned_data["url"]
        link.save(update_fields=("name", "url",))
        return link


@post_request_required
@link_ownership_required
@login_required(redirect_field_name=None)
def alter_link(request, link_id):

    form = AlterLinkForm(request.POST)
    link = check_space_link(link_id, request.user)

    if form and form.is_valid():
        altered_link = form.save_altered_link(link)
        return JsonResponse({"status": "ok", "altered_link": model_to_dict(altered_link)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(link.work_space.pk,))})

@login_required(redirect_field_name=None)
def account_settings(request):

    if request.method == "POST": 
        settings_form = AccountSettingsForm(request.POST)

        if settings_form.is_valid():
            user = authenticate(request, username=request.user.username, password=settings_form.cleaned_data["password"])
            if user is not None and user == request.user:
                # Save all changes
                settings_form.update_user_info(user)
                # Redirect to login-view
                display_success_message(request, "Account details were successfully updated!")
                return JsonResponse({"status": "ok"})

        # Error case
        display_error_message(request)
        return JsonResponse({"status": "error"})

    data = {
        "change_password_form": ChangePasswordForm(),
        "settings_form": AccountSettingsForm().set_initials(request.user),
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user)
    }
    return render(request, "user_management/account_settings.html", data)


@login_required(redirect_field_name=None)
def account_settings_view(request):

    data = {
        "change_password_form": ChangePasswordForm(),
        "settings_form": AccountSettingsForm().set_initials(request.user),
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user)
    }
    return render(request, "user_management/account_settings.html", data)


@login_required
@post_request_required
def edit_account_info(request):

    form = AccountSettingsForm(request.POST)

    if form.is_valid():
        user = authenticate(request, username=request.user.username, password=form.cleaned_data["password"])
        if user is not None and user == request.user:
            # Save all changes
            form.update_user_info(user)
            # Redirect to login-view
            display_success_message(request, "Account details were successfully updated!")
            return JsonResponse({"status": "ok"})

    # Error case
    display_error_message(request)
    return JsonResponse({"status": "error"})


@login_required
@post_request_required
def change_password(request):

    form = ChangePasswordForm(request.POST)

    if form.is_valid():
        old_password = form.cleaned_data["old_password"]
        new_password = form.cleaned_data["new_password"]
        confirmation = form.cleaned_data["confirmation"]

        # Check old password and confirmation
        user = authenticate(request, username=request.user.username, password=old_password)
        if user and new_password == confirmation:
            # Update password
            user.set_password(new_password)
            user.save(update_fields=("password",))
            display_success_message(request, "Password was successfully updated!")
            return JsonResponse({"status": "ok"})
        
    # Redirect back in case of error
    display_error_message(request)
    return JsonResponse({"status": "error"})


@post_request_required
@space_ownership_required
@login_required(redirect_field_name=None)
def delete_work_space(request, space_id):

    form = None

    if form and form.is_valid():

        # Check if user has right to delete this work space
        space = check_work_space(space_id, request.user)

        # Delete work pace directory with all files inside
        shutil.rmtree(space.get_path())

        # Delete workspace from the db
        space.delete()

        return JsonResponse({"message": "ok"})
    
    # TODO
    # Return to index?
    return JsonResponse({"message": "error"})

path("delete_space/<int:space_id>", views.delete_work_space, name="delete_space"),



@paper_authorship_required
@login_required(redirect_field_name=None)
def delete_paper(request, paper_id):

    # Check if user has right to delete this paper
    paper = check_paper(paper_id, request.user)
    
    # Delete paper directory with all files inside
    if paper.files.all():
        shutil.rmtree(paper.get_path())

    # Delete paper from the db
    paper.delete()
    return JsonResponse({"message": "ok"})

path("delete_paper/<int:paper_id>", views.delete_paper, name="delete_paper"),


    def save_work_space(self, user: User) -> int:
        new_work_space = WorkSpace(owner=user, title=self.cleaned_data["title"])
        new_work_space.save()
        return new_work_space.pk
    
        
def show_error_page(request):
    # TODO

    # Do I need it at all?

    return render(request, "website/error_page.html")
    path("error_page", views.show_error_page, name="error_page"),

@login_required(redirect_field_name=None)
def load_index_content(request):

    data = {
        "work_spaces": get_user_work_spaces(request.user),
        "new_space_form": NewSpaceForm(),
        "invitation_form": ReceiveInvitationForm(),
        "shared_sources_form": ReceiveSourcesForm()

    }
    return render(request, "website/index_navbar.html", data)


    path("index_loader", views.load_index_content, name="TODO"),


@space_ownership_required
@login_required(redirect_field_name=None)
def stop_sharing_space_sources(request, space_id):

    space = check_work_space(space_id, request.user)
    stop_sharing_sources(space)
     
    return JsonResponse({"status": "ok"})





    def stop_sharing_sources(space: WorkSpace) -> None:


    # Mark that space sources are not shared
    if space.share_sources:
        space.share_sources = False
        space.save(update_fields=("share_sources",))

    # Delete sharing code if it was already made
    sharing_code = get_space_sharing_code(space)
    if sharing_code:
        sharing_code.delete()


    option = forms.ChoiceField(choices=SOURCES_RECEIVING_OPTIONS, widget=forms.RadioSelect(attrs={
        #"class": "form-check-input",
    }))

    SOURCES_RECEIVING_OPTIONS = (("copy", "Create New Work Space"), ("download", "Download sources"),)


class UploadPaperFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))

    def save_new_paper_file(self, paper: Paper, user: User):
        new_file = PaperFile(user=user, paper=paper, file=self.cleaned_data["file"])
        new_file.save()


class UploadSourceFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "accept": ACCEPTED_UPLOAD_FORMATS,
        "id": "file-field",
        "class": CLASS_,
        "placeholder": "File"})
    )

    def save_new_source_file(self, source: Source):
        new_file = SourceFile(source=source, file=self.cleaned_data["file"])
        new_file.save()

    # Copy the given source and alter its key fields
    source.pk, source.id = None, None
    source.work_space, source.user = new_space, new_owner
    source._state.adding = True
    source.save()

    # Change file info, if file was uploaded
    source_file: SourceFile | None = source.get_file()
    if source_file:
        save_new_source_file(source_file.file, source)

    # Copy all quotes related to original source if necessary
    if source_quotes:
        for quote in source_quotes:
            quote.pk, quote.source = None, source
            quote._state.adding = True
            quote.save()

    # Create new Reference obj based on new source
    create_source_reference(source)
    return source

    
    # Get array with only sources which files were uploaded
    sources_with_files = [source for source in original_sources if source.get_file()]

    # Copy all files if necessary
    if any(sources_with_files):

        pass



    # Copy all files if necessary
    if any(sources_with_files):
        # Create new "sources" dir
        new_sources_root = os.path.join(new_space.get_path(), "sources", f"user_{new_owner.pk}")
        os.makedirs(new_sources_root, exist_ok=True)

        for source in sources_with_files:
            # Copy original source file into new "sources-files" dir
            new_source_id = new_sources_id[source.pk]
            source_id_root = os.path.join(new_sources_root, f"source_{new_source_id}")
            os.makedirs(source_id_root, exist_ok=True)
            destination = os.path.join(source_id_root, source.get_file().file_name())
            original_file = source.get_file().get_path_to_file()
            shutil.copyfile(original_file, destination)

# Do I need it?
def copy_source_file_info(source: Source, new_space: WorkSpace, new_owner_id: int) -> str:

    space_path = new_space.get_base_dir()
    source_id, user_id = source.pk, new_owner_id
    filename = source.file_name()
    return f"{space_path}/sources/user_{user_id}/source_{source_id}/{filename}"


# Do I need it?
def copy_source_file_test(original_file: SourceFile, new_source=Source):

    new_copy = SourceFile(source=new_source)
    new_copy.file = ContentFile(original_file.file.read(), name=original_file.file.name)
    new_copy.save()


        # Copy all sources into db and keep track of new sources id
    new_sources_id: dict = {}
    for source in original_sources:
        new_source = copy_source(source, new_space, new_owner)
        new_sources_id[source.pk] = new_source.pk


class RenamePaperForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    def set_initial(self, paper: Paper):
        self.fields["title"].initial = paper.title
        return self

    def save_new_name(self, paper: Paper) -> Paper:
        paper.title = self.cleaned_data["title"]
        paper.save(update_fields=("title",))
        return paper



class CitationStyleForm(forms.Form):
    citation_style = forms.ChoiceField(choices=CITATION_STYLES, widget=forms.Select(attrs={"class": CLASS_}))

    def save_citation_style(self, paper: Paper):
        "Update citation_style field in Workspace obj"
        paper.citation_style = self.cleaned_data["citation_style"]
        return paper.save(update_fields=("citation_style",))


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):

    form = RenamePaperForm(request.POST)

    if form and form.is_valid():
        # Update papers name
        paper = check_paper(paper_id, request.user)
        renamed_paper = form.save_new_name(paper)
        return JsonResponse({"status": "ok", "new_title": renamed_paper.title})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("paper_work:paper_space", args=(paper_id,))})

@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def set_citation_style(request, paper_id):

    form = CitationStyleForm(request.POST)

    if form.is_valid():
        paper = check_paper(paper_id, request.user)
        form.save_citation_style(paper)
        return JsonResponse({"status: ok"})

    return JsonResponse({"status": "error"})


class NewPaperForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "title-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Paper title"})
    )

    citation_style = forms.ChoiceField(choices=CITATION_STYLES, widget=forms.RadioSelect(attrs={"class": CLASS_}))

    def save_paper(self, space: WorkSpace, user: User):

        new_paper = Paper(work_space=space, user=user, title=self.cleaned_data["title"])
        new_paper.save()
        return new_paper


    




class PaperSettingsForm(NewPaperForm):

    def set_initial(self, paper: Paper):

        self.fields["title"].initial = paper.title
        self.fields["citation_style"].initial = paper.citation_style
        return self
    
    def save_changes(self, paper: Paper):

        paper.title = self.cleaned_data["title"]
        paper.citation_style = self.cleaned_data["citation_style"]
        return paper.save(update_fields=("title", "citation_style",))


    def rename_paper(self, paper: Paper):
        "Change paper title"
        paper.title = self.cleaned_data["title"]
        return paper.save(update_fields=("title",))



    def save_new_title(self, space: WorkSpace) -> WorkSpace:
        space.title = self.cleaned_data["new_title"]
        space.save(update_fields=("title",))
        return space

        
@login_required
def work_space_view(request, space_id):

    space = check_work_space(space_id, request.user)

    # Add in each source its number in order to enable toggle between bootstrap modal
    sources: list = []
    source_number = 1
    for source in space.sources.all():
        if source.has_file:
            file_id = source.get_file().pk
        else:
            file_id = None
        source = model_to_dict(source)
        source["number"] = source_number
        source["file_id"] = file_id
        sources.append(source)
        source_number += 1

    # Get user status
    if request.user == space.owner:
        user_status = "owner"
    else:
        user_status = "guest"

    # Get all needed source-related data
    work_space_data = {
        "space": space, 
        "space_papers": space.papers.all(),
        "sources": sources,
        "number_of_sources": len(sources),
        "links": space.links.all(),
        "new_paper_form": NewPaperForm(),
        "book_form": BookForm(),
        "article_form": ArticleForm(),
        "chapter_form": ChapterForm(),
        "webpage_form": WebpageForm(),
        "link_form": NewLinkForm(),
        "rename_form": RenameSpaceForm().set_initial(space),
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user),
        "user_status": user_status
    }
    return render(request, "work_space.html", work_space_data)


def link_ownership_required(func: Callable) -> Callable | PermissionDenied:
    def wrapper(request, link_id):
        link = check_space_link(link_id, request.user)
        if link.user != request.user:
            raise PermissionDenied
        return func(request, link_id)
    return wrapper


    sources: list = []
    for source in space.sources.all():
        if source.has_file:
            file_id = source.get_file().pk
        else:
            file_id = None
        if source.quotes.all():
            quotes = True
        else:
            quotes = False
        source = model_to_dict(source)
        source["file_id"] = file_id
        source["has_quotes"] = quotes



        sources.append(source)

        def invitation_view(request, code):


    # Check type of invitation and if it exists
    invitation_code = check_invitation(code)
    source_sharing_code = check_share_sources_code(code)

    # Invitation page can be shown shown both for logged in and not logged in users
    
    if request.user.is_authenticated:
        data = {"work_spaces": get_user_work_spaces(request.user), "papers": get_user_papers(request.user)}
    else:
        data = {}

    # Figure out which of two codes it might be
    if invitation_code:
        data["invitation_form"] = ReceiveInvitationForm()
        data["invitation_code"] = invitation_code.code

    if source_sharing_code:
        data["shared_sources_form"] = ReceiveSourcesForm()
        data["share_sources_code"] = source_sharing_code.code

    return render(request, "website/invitation.html", data)


path("add_link_to_space/<int:space_id>", views.add_link, name="add_link"),
path("delete_link/<int:link_id>", views.delete_link, name="delete_link"),

@post_request_required
@login_required(redirect_field_name=None)
def add_link(request, space_id):


    # TODO ???

    form = NewLinkForm(request.POST)

    if form and form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        new_link = form.save_link(space)
        return JsonResponse({"status": "ok", "link_name": new_link.name, "url": model_to_dict(new_link)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})


@login_required(redirect_field_name=None)
def delete_link(request, link_id):


    # Check link and delete if from the db
    link = check_space_link(link_id, request.user)
    link.delete()
    return JsonResponse({"status": "ok"})

class Link(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="links")
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name

class NewLinkForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "name-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Name"})
    )

    url = forms.URLField()

    def save_link(self, space: WorkSpace) -> Link:
        new_link = Link(work_space=space, name=self.cleaned_data["name"], url=self.cleaned_data["url"])
        new_link.save()
        return new_link
        
def check_space_link(link_id: int, user: User) -> Link | Http404:
    try:
        link = Link.objects.get(pk=link_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(link.work_space.pk, user)
    return link

    def create_friendly_links_file(links, root_path: str) -> None:

    # Get path to new links.txt file
    links_file_path = os.path.join(root_path, "links.txt")

    # Create file and write in all links
    with open(links_file_path, "w") as link_file:
        for link in links:
            link_file.write(f"{link}:\n{link.url}\n\n")

def get_number_of_members(space: WorkSpace) -> int:

    return len(space.guests.all()) + 1

    from django.http import Http404
from user_management.models import User
from .models import WorkSpace


def get_user_status(user: User, space: WorkSpace) -> str | Http404:

    if user == space.owner:
        return "owner"
    elif user in space.members.all():
        return "member"
    else:
        raise Http404

from django.forms.models import model_to_dict
from work_space.models import WorkSpace
from .models import Article, Book, Chapter, Source, Webpage


def get_work_space_sources(space: WorkSpace) -> list:

    sources: list = []
    for source in space.sources.all():
        source: Source
        source_dict: dict = model_to_dict(source)

        source_dict["type"] = get_source_type(source)

        if source.has_file:
            source_dict["file_id"] = source.get_file().pk
        else:
            source_dict["file_id"] = None
        if source.quotes.all():
            source_dict["has_quotes"] = True
        else:
            source_dict["has_quotes"] = False
        sources.append(source_dict)

    return sources


def get_source_type(source: Source) -> str:


    source_type = source.cast()
    match source_type:
        case Book():
            return "book"
        case Article():
            return"article"
        case Chapter():
            return "chapter"
        case Webpage():
            return "webpage"

def get_work_space_papers(space: WorkSpace) -> list:

    papers: list = []
    for paper in space.papers.filter(archived=False):
        paper: Paper
        paper_dict: dict = model_to_dict(paper)
        paper_dict["number_of_commits"] = paper.get_number_of_files()
        papers.append(paper_dict)

    return papers

"""





