from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('signout/', views.signout, name='signout'),
    path('change-password/', views.change_password, name='changepassword'),
    
    path('account/', views.user_account, name='account'),
    path('update-account/', views.update_user_account, name='updateaccount'),
    path('delete-account/', views.delete_user_account, name='deleteaccount'),
    
    # forgot password:
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='user_app/password_reset_done.html'
        ), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user_app/password_reset_confirm.html"
        ), 
        name='password_reset_confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='user_app/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
]
