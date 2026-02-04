# analysis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_text_view, name='analyze_text'),
    path('analyze-ajax/', views.analyze_text_ajax, name='analyze_ajax'),
    path('history/', views.history_view, name='history'),
]