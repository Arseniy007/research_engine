from django.db import models

from user_management.models import User
from work_space.models import WorkSpace


class Book(models.Model):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    city = models.CharField(max_length=20, blank=True)
    year = models.IntegerField(blank=True)


    def __str__(self):
        """Display book title"""
        return self.title








"""
class Article(Book):

    pass
"""
