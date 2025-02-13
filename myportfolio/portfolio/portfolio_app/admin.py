from django.contrib import admin
from .models import Tech, Skill, Project, Certificate, CV

# Register your models here.
admin.site.register((Tech, Skill, Project, Certificate, CV))