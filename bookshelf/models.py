from django.db import models

from user_management.models import User


# Create your models here.
class Book(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    city = models.CharField(max_length=20, blank=True)
    year = models.IntegerField(blank=True)



"""
class Article(Book):

    pass
"""
