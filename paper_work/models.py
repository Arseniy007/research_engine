from django.db import models

from user_management.models import User


class Paper(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass
