from django.db import models

from user_management.models import User
from work_space.models import WorkSpace


class Author(models.Model):

    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    initials = models.CharField(max_length=10)

    
    def __str__(self):
        """Display authors name"""
        return f"{self.last_name} {self.first_name}"
    

class CommonInfo(models.Model):

    title = models.CharField(max_length=100)
    year = models.IntegerField(blank=True)

    link_to_text = models.CharField(max_length=40, blank=True)

    class Meta:
        abstract = True

    
    def __str__(self):
        """Display book title"""
        return self.title


class Book(CommonInfo):

    related_name = "books"

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name=related_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)

    author = models.ManyToManyField(Author, related_name=related_name)

    publishing_house = models.CharField(max_length=20)
    city = models.CharField(max_length=20, blank=True)

    is_edited = models.BooleanField(default=False)


class Chapter(Book):

    pages = models.CharField(max_length=20)


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
        """Display quotes text"""
        return self.text


"""
class EditedBook(CommonInfo):

    pass
"""


# Page - Integerfield??
