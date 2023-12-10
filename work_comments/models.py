from django.db import models
from research_engine.settings import SAVING_TIME_FORMAT
from user_management.models import User
from work_space.models import WorkSpace


class Comment(models.Model):
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def get_creation_time(self):
        """Return saving time in chosen format"""
        return self.created.strftime(SAVING_TIME_FORMAT)


    def __str__(self):
        """Display comment text"""
        if self.work_space.guests.all():
            return f'{self.user}: "{self.text}" ({self.get_creation_time()})'
        return f'"{self.text}" ({self.get_creation_time()})'
