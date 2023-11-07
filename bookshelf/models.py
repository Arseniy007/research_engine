import os

from django.db import models 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from user_management.models import User
from work_space.models import WorkSpace


def saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/books/user_<id>/book_<id>/<filename>"""

    space_path = instance.work_space.get_base_dir()
    user_id, book_id = instance.user.pk, instance.pk

    return f"{space_path}/books/user_{user_id}/book_{book_id}/{filename}"


# should be real class! Source! with one verification func and one decorator!

class Source(models.Model):
    """
    An abstract base class for all possible sources: books, articles, chapters, websites etc.
    Using _cast_ method one can access child class of any source-objects
    """

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=70, blank=True)
    multiple_authors = models.BooleanField(default=False)

    year = models.CharField(max_length=5, blank=True)

    file = models.FileField(upload_to=saving_path, blank=True)
    link = models.CharField(max_length=40, blank=True)

    real_type = models.ForeignKey(ContentType, editable=False, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self._state.adding:
            self.real_type = self.get_real_type()
        super(Source, self).save(*args, **kwargs)


    def get_real_type(self):
        return ContentType.objects.get_for_model(type(self))
    

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)


class Book(Source):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="books")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    publishing_house = models.CharField(max_length=20)


    def __str__(self):
        """Display book title"""
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
    

class Article(Source):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="articles")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    journal_title = models.CharField(max_length=50)
    volume_number = models.IntegerField()
    journal_number = models.IntegerField()
    pages = models.CharField(max_length=20)

    is_electronic = models.BooleanField(default=False)
    link_to_journal = models.CharField(max_length=40, blank=True)

    def get_object_type(self):

        return type(self)

 
class Website(Source):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="websites")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")

    has_author = models.BooleanField(default=False)
    website_title = models.CharField(max_length=50)
    page_url = models.CharField(max_length=50)
    date = models.DateField()


class Chapter(Source):

    chapter_title = models.CharField(max_length=50)
    chapter_author = models.CharField(max_length=70)
    edition = models.IntegerField(blank=True)
    pages = models.CharField(max_length=20)


class Quote(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="quotes")
    object_id = models.PositiveIntegerField()
    source = GenericForeignKey("content_type", "object_id")
    page = models.IntegerField()
    text = models.TextField()

    
    def __str__(self):
        '''Display quotes text'''
        return f'"{self.text}" (p. {self.page})'
