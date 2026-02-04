# chatbot/urls.py
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('history/', views.get_chat_history, name='get_history'),
    path('clear/', views.clear_chat_history, name='clear_history'),
]