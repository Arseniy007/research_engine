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







from user_management.models import User

from work_space.models import WorkSpace

from bookshelf.models import Author, Book

from bookshelf.quoting import quote_book_apa

user = User.objects.get(pk=1)

space = WorkSpace.objects.get(pk=2)

author = Author.objects.get(pk=1)

book = Book.objects.get(pk=2)



quote_book_apa(book)



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

