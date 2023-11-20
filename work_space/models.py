import os

from django.db import models

from research_engine.settings import MEDIA_ROOT, FRIENDLY_TMP_ROOT
from user_management.models import User


class WorkSpace(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    guests = models.ManyToManyField(User, blank=True, related_name="guests")
    title = models.CharField(max_length=50)
    is_archived = models.BooleanField(default=False)


    def __str__(self):
        """Display work space title"""
        return self.title


    def create_dir(self):
        """Creates a directory for a work space"""
        return os.mkdir(self.get_path())
    

    def create_friendly_dir(self):
        """Creates directory for future zip-archiving and downloading"""
        return os.makedirs(self.get_friendly_path(), exist_ok=True)
    

    def get_path(self):
        """Returns a path to the work space directory"""
        return f"{MEDIA_ROOT}/work_space_{self.pk}"
    

    def get_friendly_path(self):
        """Returns a path to the user-friendly version of space directory"""
        return f"{FRIENDLY_TMP_ROOT}/{self.pk}"


    def get_base_dir(self):
        """Returns base directory without MEDIA_ROOT"""
        return f"work_space_{self.pk}"


class Invitation(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, unique=True)


class Comment(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """Disolay comment text"""
        return self.text

    # TODO
