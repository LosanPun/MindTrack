# Undo Google OAuth Task

## Steps to Complete
- [ ] Remove allauth apps from INSTALLED_APPS in settings.py
- [ ] Remove allauth context processors from TEMPLATES in settings.py
- [ ] Remove allauth middleware from MIDDLEWARE in settings.py
- [ ] Remove allauth.urls from urlpatterns in mindtrack/urls.py
- [ ] Update login.html to remove socialaccount load and make Google buttons non-functional
- [ ] Test the application to ensure no errors and buttons remain unchanged in UI
