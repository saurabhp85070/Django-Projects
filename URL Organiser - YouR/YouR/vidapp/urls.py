from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='vidapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/add/', views.add_video, name='add_video'),
    path('videos/<int:pk>/', views.video_detail, name='video_detail'),
    path('videos/<int:pk>/edit/', views.edit_video, name='edit_video'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='vidapp/password_reset.html', html_email_template_name='vidapp/email_template/password_reset_email.html', subject_template_name='vidapp/email_template/password_reset_subject.txt'), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='vidapp/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='vidapp/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='vidapp/password_reset_complete.html'), name='password_reset_complete'),
]