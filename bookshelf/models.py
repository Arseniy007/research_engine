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


class Quote(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quotes")
    page = models.IntegerField()
    text = models.TextField()

    
    def __str__(self):
        '''Display quotes text'''
        return f'"{self.text}" (p. {self.page})'
