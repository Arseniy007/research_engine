from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_page_is_opened = models.BooleanField(default=True)
    followers = models.ManyToManyField("self")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def follow(self, follower):
        """Add new follower"""
        return self.followers.add(follower)
    
    
    def unfollow(self, follower):
        """Remove follower"""
        return self.followers.remove(follower)