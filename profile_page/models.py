from django.db import models
from django.db.models import signals
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


# TODO LEAVE COMMENT
def create_ProfilePage_obj(sender, instance, created, **kwargs):
    """Create ProfilePage obj for every new User"""
    if created:
        ProfilePage.objects.create(user=instance)

signals.post_save.connect(create_ProfilePage_obj, sender=User, weak=False,
                          dispatch_uid='models.create_ProfilePage_obj')
