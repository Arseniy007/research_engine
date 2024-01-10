import os
from django.db import models 
from django.contrib.contenttypes.models import ContentType
from file_handling.models import SourceFile
from user_management.models import User
from work_space.models import WorkSpace


class Source(models.Model):
    """
    A parent base class for all possible sources: books, articles, chapters, webpages etc.
    Using _cast_ method one can access child class of any source-objects
    """
    real_type = models.ForeignKey(ContentType, editable=False, on_delete=models.CASCADE)
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="sources")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sources")
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=70, blank=True)
    year = models.CharField(max_length=5, blank=True)
    link = models.CharField(max_length=40, blank=True)
    

    def __str__(self):
        '''Display book title'''
        return self.title


    def save(self, *args, **kwargs):
        """Custom save func with obj real type storing"""
        if self._state.adding:
            self.real_type = self.get_real_type()
        return super(Source, self).save(*args, **kwargs)


    def get_real_type(self):
        """Get object type"""
        return ContentType.objects.get_for_model(type(self))
    

    def cast(self):
        """Get object class (Book / Article / Webpage / etc.)"""
        return self.real_type.get_object_for_this_type(pk=self.pk)
    
    
    def get_path(self):
        """Returns a path to the book directory"""
        return os.path.join(self.work_space.get_path(), "sources", f"user_{self.user.pk}", f"source_{self.pk}")
    

    def has_file(self):
        return len(SourceFile.objects.filter(source=self))


class Book(Source):
    publishing_house = models.CharField(max_length=20)


class Article(Source):
    journal_title = models.CharField(max_length=50)
    volume = models.CharField(max_length=10)
    issue = models.CharField(max_length=10)
    pages = models.CharField(max_length=20)
    link_to_journal = models.CharField(max_length=40, blank=True)


class Chapter(Source):
    book_title = models.CharField(max_length=50)
    book_author = models.CharField(max_length=70)
    publishing_house = models.CharField(max_length=20)
    edition = models.CharField(max_length=10)
    pages = models.CharField(max_length=20)
    

class Webpage(Source):
    website_title = models.CharField(max_length=50)
    page_url = models.CharField(max_length=100)
    date = models.CharField(max_length=20)


class Reference(models.Model):
    source = models.OneToOneField(Source, on_delete=models.CASCADE, related_name="reference")
    endnote_apa = models.CharField(max_length=50)
    endnote_mla = models.CharField(max_length=50)


class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="quotes")
    page = models.IntegerField()
    text = models.TextField()
    apa = models.CharField(max_length=20)
    mla = models.CharField(max_length=20) 
    

    def save(self, *args, **kwargs):
        """Custom save method that stores apa & mla in-text citations"""
        author_last_name = self.source.author.split()[0]
        self.apa = f"({author_last_name}, {self.source.year}, p. {self.page})"
        self.mla = f"({author_last_name} {self.page})"
        super(Quote, self).save(*args, **kwargs)


    def apa_formatted(self):
        return f'"{self.text}" {self.apa}'


    def mla_formatted(self):
        return f'"{self.text}" {self.mla}'


    def __str__(self):
        """Display quotes text"""
        return self.apa_formatted()
