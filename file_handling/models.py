import os
from django.db import models
from research_engine.constants import SAVING_TIME_FORMAT
from research_engine.settings import MEDIA_ROOT
from user_management.models import User


def paper_saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/papers/user_<id>/paper_<id>/file_<id>/<filename>"""
    space_path, user_id = instance.paper.work_space.get_base_dir(), instance.paper.user.pk
    paper_id, saving_time = instance.paper.pk, instance.get_saving_time()
    return os.path.join(space_path, "papers", f"user_{user_id}", f"paper_{paper_id}", saving_time, filename)


def source_saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/books/user_<id>/source_<id>/<filename>"""
    space_path = instance.source.work_space.get_base_dir()
    source_id = instance.source.pk
    return os.path.join(space_path, "sources", f"source_{source_id}", filename)


class PaperFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey("paper_work.Paper", on_delete=models.CASCADE, related_name="files")
    saving_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=paper_saving_path)


    def __str__(self):
        """Display file saving time instead of filename"""
        return self.get_saving_time()


    def file_name(self):
        """Returns only the name of file without trailing dirs"""
        return os.path.basename(self.file.name)


    def get_saving_time(self):
        """Return saving time in chosen format"""
        return self.saving_time.strftime(SAVING_TIME_FORMAT)


    def get_path_to_file(self):
        """Returns a full path to the file"""
        return os.path.join(MEDIA_ROOT, str(self.file))


    def get_directory_path(self):
        """Returns a path to the file directory"""
        return os.path.join(self.paper.get_path(), self.get_saving_time())


class SourceFile(models.Model):
    source = models.OneToOneField("bookshelf.Source", on_delete=models.CASCADE, related_name="file")
    file = models.FileField(upload_to=source_saving_path, blank=True)


    def file_name(self):
        """Returns only the name of file without trailing dirs"""
        return os.path.basename(self.file.name)


    def get_path_to_file(self):
        """Returns a path to the source file"""
        if self.file:
            return os.path.join(MEDIA_ROOT, str(self.file))
        return None
