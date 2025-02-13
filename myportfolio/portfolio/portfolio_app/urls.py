from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<uuid:project_id>/', views.project_detail, name='projectdetail'),
    path('send-contact-email/', views.send_contact_email, name='send_contact_email'),
]