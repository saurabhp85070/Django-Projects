from django.db import models
from tinymce.models import HTMLField
import uuid

# Create your models here.

class Tech(models.Model):
    name = models.CharField(max_length=100)
    display_priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    tech = models.ForeignKey(Tech, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    project_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True) 
    display_priority = models.IntegerField(default=0)
    title = models.CharField(max_length=400)
    image = models.ImageField(upload_to='project_img/', blank=True, null=True)
    body = HTMLField() 
    link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    tag1 = models.CharField(max_length=50, null=False, blank=False)
    tag2 = models.CharField(max_length=50, null=True, blank=True)
    tag3 = models.CharField(max_length=50, null=True, blank=True)
    tag4 = models.CharField(max_length=50, null=True, blank=True)
    tag5 = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class Certificate(models.Model):
    name = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='certificate_pdf/', blank=False, null=False)
    image = models.ImageField(upload_to='certificate_img/', blank=False, null=False)
    
    def __str__(self):
        return self.name
    
class CV(models.Model):
    cv = models.FileField(upload_to='resume/', help_text="Upload your PDF file")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uploaded_at)