from django.contrib import admin
from .models import VideoBookmark, Tag

# Register your models here.


@admin.register(VideoBookmark)
class VideoBookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'get_source')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)