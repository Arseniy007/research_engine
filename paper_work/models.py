from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import format_html
from datetime import datetime

from user_management.models import User
from research_engine.settings import MEDIA_ROOT


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/paper_title/date/<filename>

    saving_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"user_{instance.user.id}/{instance.paper_title}/{saving_date}/{filename}"


class Paper(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)


class PaperVersion(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    paper_title = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)
    saving_date = models.DateTimeField(auto_now_add=True)


    def get_path(self):

        #return f"{MEDIA_ROOT}/user_{self.user.pk}/{self.paper_title}/{self.saving_date.strftime('%Y-%m-%d %H:%M:%S')}/{self.file}"
        return  f"{MEDIA_ROOT}/{str(self.file)}"
        


