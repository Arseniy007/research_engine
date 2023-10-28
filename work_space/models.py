from django.db import models

from user_management.models import User


class WorkSpace(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    guests = models.ManyToManyField(User, blank=True, related_name="guests")
    title = models.CharField(max_length=50)
    is_archived = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Invitation(models.Model):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, unique=True)
