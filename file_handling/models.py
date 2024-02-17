import os
from django.db import models
from research_engine.settings import MEDIA_ROOT
from user_management.models import User


def paper_saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/papers/user_<id>/paper_<id>/file.str()/<filename>"""
    space_path, paper_id = instance.paper.work_space.get_base_dir(), instance.paper.pk
    user_id, dir_name = instance.paper.user.pk, instance.version_number
    return os.path.join(space_path, "papers", f"user_{user_id}", f"paper_{paper_id}", dir_name, filename)


def source_saving_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/work_space_<id>/books/user_<id>/source_<id>/<filename>"""
    space_path = instance.source.work_space.get_base_dir()
    source_id = instance.source.pk
    return os.path.join(space_path, "sources", f"source_{source_id}", filename)


class PaperFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey("paper_work.Paper", on_delete=models.CASCADE, related_name="files")
    commit_text = models.CharField(max_length=100, blank=True)
    version_number = models.CharField(max_length=50)
    file = models.FileField(upload_to=paper_saving_path)


    def save(self, *args, **kwargs):
        """Custom save method with storing version number"""
        previous_versions = PaperFile.objects.filter(paper=self.paper)
        self.version_number = f"file #{len(previous_versions) + 1}"
        return super(PaperFile, self).save(*args, **kwargs)


    def __str__(self):
        """Display either commit text if given or number of current paper file"""
        if self.commit_text:
            return self.commit_text
        return f"{self.paper} #{self.version_number}"


    def file_name(self):
        """Returns only the name of file without trailing dirs"""
        return os.path.basename(self.file.name)


    def get_path_to_file(self):
        """Returns a full path to the file"""
        return os.path.join(MEDIA_ROOT, str(self.file))


    def get_directory_path(self) -> str:
        """Returns a path to the file directory"""
        return os.path.join(self.paper.get_path(), self.version_number)


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
