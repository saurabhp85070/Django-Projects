from django.db import models
import uuid
from django.contrib.auth.models import User
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify



# Create your models here.


def user_profile_pic_path(instance, filename):
    """
    Generate a secure file path for user profile pictures.
    """
    ext = filename.split('.')[-1]
    filename = f"{instance.profile_id}_{slugify(instance.user.username)}.{ext}"
    return os.path.join('profile_pics', filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # if we do like this: oberve the change in signals.py
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile") 
    
    profession = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    kaggle = models.URLField(blank=True, null=True)
    X = models.URLField(blank=True, null=True)
    other_link = models.URLField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    

    def get_follower_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()
    
    def __str__(self):
        return self.user.username

@receiver(pre_save, sender=UserProfile)
def delete_old_profile_pic(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_profile = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        return False

    new_profile_pic = instance.profile_pic
    if old_profile.profile_pic and old_profile.profile_pic != new_profile_pic:
        if os.path.isfile(old_profile.profile_pic.path):
            os.remove(old_profile.profile_pic.path)

