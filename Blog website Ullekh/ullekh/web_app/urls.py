from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send-contact-email/', views.send_contact_email, name='send_contact_email'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('terms-of-use/', views.terms, name='terms'),
]