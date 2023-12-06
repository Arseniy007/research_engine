from django.db import models
from django.db.models import signals
from user_management.models import User


class ProfilePage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    followers = models.ManyToManyField(User, related_name="following")
    is_opened = models.BooleanField(default=True)


    def follow(self, follower: User):
        """Add new follower"""
        return self.followers.add(follower)
    
    
    def unfollow(self, follower: User):
        """Remove follower"""
        return self.followers.remove(follower)
    

    def open_page(self):
        self.is_opened = True
        return self.save(update_fields=("is_opened",))


    def close_page(self):
        self.is_opened = False
        return self.save(update_fields=("is_opened",))
        

# Make sure that every time then new User obj is created - new ProfilePage connected to new user is automatically created
def create_ProfilePage_obj(sender, instance, created, **kwargs):
    """Create ProfilePage obj for every new User"""
    if created:
        ProfilePage.objects.create(user=instance)

signals.post_save.connect(create_ProfilePage_obj, sender=User, weak=False,
                          dispatch_uid='models.create_ProfilePage_obj')
