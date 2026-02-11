# analysis/urls.py
from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('analyze/', views.analyze_text_view, name='analyze_text'),
    path('analyze-ajax/', views.analyze_text_ajax, name='analyze_ajax'),
    path('save-analysis-ajax/', views.save_analysis_ajax, name='save_analysis_ajax'),
    path('history/', views.history_view, name='history'),
    path('analytics/', views.analytics_view, name='analytics'),
]
