from django.db import models
from datetime import datetime

from user_management.models import User


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    saving_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"user_{instance.user.id}/{instance.paper_title}/{saving_date}/{filename}"


class Paper(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)


class PaperVersion(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    paper_title = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)
