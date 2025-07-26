from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),  # http://127.0.0.1:8000/chats/
    path('home/', views.chat_home, name='chat-home'),  # http://127.0.0.1:8000/chats/home/
]
