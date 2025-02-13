from django.contrib import admin
from .models import BlogPost, BlogComment, Category, SavedPost

# Register your models here.


    
admin.site.register((BlogPost, BlogComment, Category, SavedPost))
