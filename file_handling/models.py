import os
from django.db import models
from research_engine.settings import MEDIA_ROOT, SAVING_TIME_FORMAT
from user_management.models import User


def saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/papers/user_<id>/paper_<id>/file_<id>/<filename>"""

    space_path, user_id = instance.paper.work_space.get_base_dir(), instance.paper.user.pk
    paper_id, saving_time = instance.paper.pk, instance.get_saving_time()

    return f"{space_path}/papers/user_{user_id}/paper_{paper_id}/{saving_time}/{filename}"


class PaperVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey("paper_work.Paper", on_delete=models.CASCADE, related_name="versions")
    saving_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=saving_path)


    def __str__(self):
        """Display file saving time instead of filename"""
        return self.get_saving_time()
    

    def file_name(self):
        """Returns only the name of file without trailing dirs"""
        return os.path.basename(self.file.name)


    def get_saving_time(self):
        """Return saving time in chosen format"""
        return self.saving_time.strftime(SAVING_TIME_FORMAT)
    

    def get_full_path(self):
        """Returns a full path to the file"""
        return  f"{MEDIA_ROOT}/{str(self.file)}"
    

    def get_directory_path(self):
        """Returns a path to the file directory"""
        return f"{self.paper.get_path()}/{self.get_saving_time()}"
