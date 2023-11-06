import os

from django.db import models 

from user_management.models import User
from work_space.models import WorkSpace


def saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/books/user_<id>/book_<id>/<filename>"""

    space_path = instance.work_space.get_base_dir()
    user_id, book_id = instance.user.pk, instance.pk

    return f"{space_path}/books/user_{user_id}/book_{book_id}/{filename}"


class Book(models.Model):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="books")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    title = models.CharField(max_length=100)

    author = models.CharField(max_length=70)
    #multiple_authors = models.BooleanField(default=False)

    year = models.CharField(max_length=5, blank=True)
    publishing_house = models.CharField(max_length=20)

    file = models.FileField(upload_to=saving_path, blank=True)
    link = models.CharField(max_length=40, blank=True)

    
    def __str__(self):
        return self.title
    

    def file_name(self):
        """Returns only the name of file without trailing dirs"""
        return os.path.basename(self.file.name)
    

    def get_path(self):
        """Returns a path to the book directory"""
        return f"{self.work_space.get_path()}/books/user_{self.user.pk}/book_{self.pk}"
    

    def get_path_to_file(self):
        """Returns a path to the book file"""
        return os.path.join(self.get_path(), os.path.basename(self.file.name))


class Quote(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quotes")
    page = models.IntegerField()
    text = models.TextField()

    
    def __str__(self):
        '''Display quotes text'''
        return f'"{self.text}" (p. {self.page})'






















   




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



# Page - Integerfield??
# on delete models cascade?
