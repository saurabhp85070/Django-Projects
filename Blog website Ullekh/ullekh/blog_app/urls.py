from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_blog_post, name='createblog'),
    path('detail/<uuid:post_id>/', views.detail_blog_post, name='detailblog'),
    path('update/<uuid:post_id>/', views.update_blog_post, name='updateblog'),
    path('delete/<uuid:post_id>/', views.delete_blog_post, name='deleteblog'),
    path('profile/<uuid:pk>/', views.author_profile, name='profile'),
    
    path('blog/<uuid:post_id>/download/', views.download_pdf, name='download_pdf'),
]