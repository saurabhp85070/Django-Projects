from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = HTMLField()
    
    def __str__(self):
        return self.question