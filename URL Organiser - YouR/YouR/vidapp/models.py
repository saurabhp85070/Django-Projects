from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class VideoBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='videos', blank=True)
    
    def __str__(self):
        return self.title
    
    def get_source(self):
        """Determine the source of the video based on URL"""
        if re.search(r'youtube|youtu\.be', self.url):
            return 'YouTube'
        elif 'instagram' in self.url:
            return 'Instagram'
        elif 'linkedin' in self.url:
            return 'LinkedIn'
        elif 'x.com' in self.url:
            return 'X'
        elif 'threads' in self.url:
            return 'Threads'
        elif 'vimeo' in self.url:
            return 'Vimeo'
        else:
            return 'Other'
    
    class Meta:
        ordering = ['-created_at']