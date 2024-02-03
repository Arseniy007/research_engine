import os
import shutil
from django.db import models
from bookshelf.models import Source
from file_handling.models import PaperFile
from user_management.models import User
from work_space.models import WorkSpace


class Paper(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="papers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="papers")
    title = models.CharField(max_length=50, unique=True)
    sources = models.ManyToManyField(Source, related_name="papers")
    archived = models.BooleanField(default=False)


    def __str__(self):
        """Display paper title"""
        return self.title


    def get_path(self):
        """Returns a path to the paper directory"""
        return os.path.join(self.work_space.get_path(), "papers", f"user_{self.user.pk}", f"paper_{self.pk}")
    

    def create_directory(self):
        """Create an empty directory for the paper-files"""
        return os.mkdir(self.get_path())
    
    
    def get_number_of_files(self) -> int:
        """Returns a number of files (PaperFile objects) related to this papers"""
        return len(PaperFile.objects.filter(paper=self))
    

    def get_last_file_id(self) -> int:
        """Returns last uploaded paper file"""
        try:
            return PaperFile.objects.filter(paper=self).order_by("-pk")[0].pk
        except IndexError:
            return None
        
        # TODO?
    

    def clear_file_history(self):
        """Delete all files related to paper"""

        # Delete paper directory and recreate new empty one
        shutil.rmtree(self.get_path())
        self.create_directory()

        # Remove files from the db
        return PaperFile.objects.filter(paper=self).delete()

    
    def archive(self):
        """Mark paper as archived or vice versa"""
        self.archived = True
        return self.save(update_fields=("archived",))
    

    def unarchive(self):
        """Return paper in its work_space"""
        self.archived = False
        return self.save(update_fields=("archived",))
