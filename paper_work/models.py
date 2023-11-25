import os
from django.db import models
from file_handling.models import PaperVersion
from user_management.models import User
from work_space.models import WorkSpace


class Paper(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="papers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    is_archived = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)


    def __str__(self):
        """Display paper title"""
        return self.title


    def get_path(self):
        """Returns a path to the paper directory"""
        return f"{self.work_space.get_path()}/papers/user_{self.user.pk}/paper_{self.pk}"
    

    def create_directory(self):
        """Create an empty directory for the paper-files"""
        return os.mkdir(self.get_path())
    
    
    def get_number_of_files(self):
        """Returns a number of files (PaperVersion objects) related to this papers"""
        return len(PaperVersion.objects.filter(paper=self))
    

    def get_last_file_id(self):
        """Returns last uploded paper file"""
        return PaperVersion.objects.filter(paper=self).order_by("-pk")[0].pk
    

    def archive(self):
        self.is_archived = True
        return self.save(update_fields=("is_archived"),)
    

    def finish(self):
        self.is_finished = True
        return self.save(update_fields=("is_finished",))
    

    def publish(self):
        self.is_published = True
        return self.save(update_fields=("is_published"),)
    
    
# Maybe add to Paper class needed number of words etc.
