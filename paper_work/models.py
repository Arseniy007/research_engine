from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import format_html
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
    saving_date = models.DateTimeField(auto_now_add=True)


    def file_link(self):
        
        return format_html("<a href='%s'>download</a>" % (f"file/uploads/papers/{self.file.url}",))
    
    file_link.allow_tags = True


    """
    def __str__(self):
        return f"uploads/papers/{str(self.file)}"
    """