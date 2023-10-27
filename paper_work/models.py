from django.db import models

from research_engine.settings import MEDIA_ROOT, SAVING_TIME_FORMAT
from user_management.models import User


def user_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/user_<id>/paper_<id>/file_<id>/<filename>"""

    return f"user_{instance.paper.user.pk}/paper_{instance.paper.pk}/{instance.get_saving_time()}/{filename}"


class Paper(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)


    def get_path(self):
        """Returns a path to the paper directory"""
        return f"{MEDIA_ROOT}/user_{self.user.pk}/paper_{self.pk}"
    

    def get_number_of_files(self):
        """Returns a number of files (PaperVersion objects) related to this papers"""
        return len(PaperVersion.objects.filter(paper=self))


class PaperVersion(models.Model):

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    saving_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=user_directory_path)


    def get_saving_time(self):
        """Return saving time in chosen format"""
        return self.saving_time.strftime(SAVING_TIME_FORMAT)
    

    def get_full_path(self):
        """Returns a full path to the file"""
        return  f"{MEDIA_ROOT}/{str(self.file)}"
    

    def get_directory_path(self):
        """Returns a path to the file directory"""
        return f"{self.paper.get_path()}/{self.get_saving_time()}"
    

class Invitation(models.Model):

    code = models.CharField(max_length=15, unique=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)


# Maybe add to Paper class needed number of words etc.
# If i invite someone, than i need to have Many to Many relation
