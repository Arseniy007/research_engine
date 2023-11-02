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


class Book(models.Model):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="books")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    author = models.ManyToManyField(Author, related_name="authors")

    title = models.CharField(max_length=100)

    publishing_house = models.CharField(max_length=20)

    city = models.CharField(max_length=20, blank=True)
    year = models.IntegerField(blank=True)

    link = models.CharField(max_length=40, blank=True)


    def __str__(self):
        """Display book title"""
        return self.title
    


class Journal(Book):

    pass



class Article(Book):

    pass



class Chapter(Book):

    pass


class Website(Book):

    pass






class Quote(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quotes")
    page = models.IntegerField()
    text = models.TextField()

    
    def __str__(self):
        """Display quotes text"""
        return self.text



# Page - Integerfield??