from django.db import models
from datetime import datetime

from user_management.models import User
from research_engine.settings import MEDIA_ROOT


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/paper_<id>/<saving_date>/<filename>

    saving_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"user_{instance.user.id}/paper_{instance.paper.pk}/{saving_date}/{filename}"


class Paper(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)


class PaperVersion(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    saving_date = models.DateTimeField(auto_now_add=True)


    def get_path(self):
        """Returns a full path to the file"""
        return  f"{MEDIA_ROOT}/{str(self.file)}"
    

# Does PaperVersion class realy needs to have user reference? Paper model already has!