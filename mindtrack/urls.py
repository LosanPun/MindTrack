# mindtrack/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

admin.site.site_header = "MindTrack Administration"
admin.site.site_title = "MindTrack Admin"
admin.site.index_title = "MindTrack Control Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    # Keep custom auth routes first so /accounts/login/ uses accounts.views.login_view
    path('accounts/', include('allauth.urls')),
    path('analysis/', include('analysis.urls', namespace='analysis')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('chatbot/', include('chatbot.urls')),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

