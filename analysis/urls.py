# analysis/urls.py
from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('analyze/', views.analyze_text_view, name='analyze_text'),
    path('analyze-ajax/', views.analyze_text_ajax, name='analyze_ajax'),
    path('save-analysis-ajax/', views.save_analysis_ajax, name='save_analysis_ajax'),
    path('history/', views.history_view, name='history'),
    path('history/<int:analysis_id>/', views.analysis_detail_view, name='history_detail'),
    path('history/<int:analysis_id>/edit/', views.analysis_edit_view, name='history_edit'),
    path('history/<int:analysis_id>/delete/', views.analysis_delete_view, name='history_delete'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('export-pdf/', views.export_data_pdf, name='export_pdf'),
]
