from django.db import models
from user_management.models import User


class ProfilePage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="followers")
    is_opened = models.BooleanField(default=True)


    def follow(self, follower: User):
        """Add new follower"""
        return self.followers.add(follower)
    
    
    def unfollow(self, follower: User):
        """Remove follower"""
        return self.followers.remove(follower)
