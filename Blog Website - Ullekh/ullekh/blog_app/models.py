from django.db import models
from django.contrib.auth.models import User
import uuid
from user_app.models import UserProfile
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from django.core.files.storage import default_storage
from tinymce.models import HTMLField
from django.utils.text import slugify

# Create your models here.

def blog_post_image_path(instance, filename):
    """
    Generate a secure file path for blog post images.
    """
    ext = filename.split('.')[-1]
    filename = f"{instance.post_id}_{slugify(instance.title)}.{ext}"
    return os.path.join('blog_images', filename)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    image = models.ImageField(upload_to=blog_post_image_path, blank=True, null=True)
    body = HTMLField() 
    post_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='blog_posts')
    
    def __str__(self):
        return self.title
    
@receiver(pre_save, sender=BlogPost)
def delete_old_blog_image(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_post = BlogPost.objects.get(pk=instance.pk)
    except BlogPost.DoesNotExist:
        return False

    new_image = instance.image
    if old_post.image and old_post.image != new_image:
        if os.path.isfile(old_post.image.path):
            os.remove(old_post.image.path)
            
            
            
# COMMENT SECTION
class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username} commented: {self.comment[:50]}"
        
    
class SavedPost(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.user.username} saved {self.post.title}"