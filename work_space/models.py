import os
from django.db import models
from research_engine.constants import FRIENDLY_TMP_ROOT
from research_engine.settings import MEDIA_ROOT
from user_management.models import User


class WorkSpace(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_spaces")
    members = models.ManyToManyField(User, related_name="guest_work_spaces")
    title = models.CharField(max_length=50)
    archived = models.BooleanField(default=False)


    def __str__(self):
        """Display work space title"""
        return self.title


    def get_path(self):
        """Returns a path to the work space directory"""
        return os.path.join(MEDIA_ROOT, f"work_space_{self.pk}")


    def get_friendly_path(self):
        """Returns a path to the user-friendly version of space directory"""
        return os.path.join(FRIENDLY_TMP_ROOT, str(self.pk))


    def create_dir(self):
        """Creates a directory for a work space"""
        return os.mkdir(self.get_path())


    def create_friendly_dir(self):
        """Creates directory for future zip-archiving and downloading"""
        return os.makedirs(self.get_friendly_path(), exist_ok=True)


    def get_base_dir(self):
        """Returns base directory without MEDIA_ROOT"""
        return f"work_space_{self.pk}"


    def get_user_status(self, user: User) -> str | None:
        """;)"""
        if user == self.owner:
            return "owner"
        if user in self.members.all():
            return "member"
        return None


    def archive(self):
        """Mark space as archived"""
        self.archived = True
        return self.save(update_fields=("archived",))


    def unarchive(self):
        """Mark space as unarchived"""
        self.archived = False
        return self.save(update_fields=("archived",))


    def add_member(self, member: User):
        """Add new member to a space"""
        return self.members.add(member)


    def remove_member(self, member: User):
        """Remove given user from a space"""
        return self.members.remove(member)


class Invitation(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, unique=True)


class ShareSourcesCode(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, unique=True)
