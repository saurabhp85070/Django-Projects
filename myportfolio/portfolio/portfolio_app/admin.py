from django.contrib import admin
from .models import Tech, Skill, Project, Certificate, CV

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_priority')  # Display title and display_priority

# Register other models normally
admin.site.register((Tech, Skill, Certificate, CV))
