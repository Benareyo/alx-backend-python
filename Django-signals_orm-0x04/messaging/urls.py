from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.delete_user, name='delete_user'),
    path('my-messages/', views.get_user_messages, name='get_user_messages'),
]
