import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindtrack.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from analysis.models import MoodAnalysis
from datetime import datetime, timedelta
import json

# Create test user
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
if created:
    user.set_password('testpass')
    user.save()

# Create some test data
moods = ['happy', 'sad', 'angry', 'fear', 'neutral', 'surprise']
for i in range(20):
    MoodAnalysis.objects.get_or_create(
        user=user,
        text=f"Test text {i}",
        detected_mood=moods[i % len(moods)],
        confidence=0.8,
        emotions={mood: 0.1 for mood in moods},
        created_at=datetime.now() - timedelta(days=i % 30)
    )

# Test the view
client = Client()
client.login(username='testuser', password='testpass')
response = client.get('/analysis/analytics/')
print('Status code:', response.status_code)
print('Contains Mood Analytics:', 'Mood Analytics' in response.content.decode())
print('Contains canvas:', 'canvas' in response.content.decode())
print('Contains Chart.js:', 'chart.js' in response.content.decode())

# Check context data
from analysis.views import analytics_view
from django.test import RequestFactory
rf = RequestFactory()
request = rf.get('/analysis/analytics/')
request.user = user
response_view = analytics_view(request)
pie_labels = json.loads(response_view.context['pie_labels'])
pie_data = json.loads(response_view.context['pie_data'])
trend_labels = json.loads(response_view.context['trend_labels'])
trend_datasets = json.loads(response_view.context['trend_datasets'])

print('Pie labels:', pie_labels)
print('Pie data:', pie_data)
print('Trend labels length:', len(trend_labels))
print('Trend datasets length:', len(trend_datasets))

# Test data accuracy
total_analyses = sum(pie_data)
print('Total analyses from pie:', total_analyses)
actual_total = MoodAnalysis.objects.filter(user=user).count()
print('Actual total analyses:', actual_total)
print('Data matches:', total_analyses == actual_total)

# Test empty state
empty_user, _ = User.objects.get_or_create(username='emptyuser', defaults={'email': 'empty@example.com'})
empty_user.set_password('emptypass')
empty_user.save()
client.login(username='emptyuser', password='emptypass')
empty_response = client.get('/analysis/analytics/')
print('Empty user status:', empty_response.status_code)
print('Empty user contains empty chart:', 'No Data Yet' in empty_response.content.decode())
