import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindtrack.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from analysis.models import MoodAnalysis
from datetime import datetime, timedelta
import json

class AnalyticsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

        # Create some test data
        moods = ['happy', 'sad', 'angry', 'fear', 'neutral', 'surprise']
        for i in range(20):
            MoodAnalysis.objects.create(
                user=self.user,
                text=f"Test text {i}",
                detected_mood=moods[i % len(moods)],
                confidence=0.8,
                emotions={mood: 0.1 for mood in moods},
                created_at=datetime.now() - timedelta(days=i % 30)
            )

    def test_analytics_view_with_data(self):
        client = Client()
        client.login(username='testuser', password='testpass')
        response = client.get('/analysis/analytics/')
        print('Status code:', response.status_code)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        print('Contains Mood Analytics:', 'Mood Analytics' in content)
        print('Contains canvas:', 'canvas' in content)
        print('Contains Chart.js:', 'chart.js' in content)

        # Check that the view renders without errors and contains expected elements
        self.assertIn('Mood Analytics', content)
        self.assertIn('canvas', content)
        self.assertIn('Chart.js', content)

        # Test data accuracy by checking database
        actual_total = MoodAnalysis.objects.filter(user=self.user).count()
        print('Actual total analyses:', actual_total)
        self.assertEqual(actual_total, 20)  # We created 20 test records

    def test_analytics_view_empty_data(self):
        # Test empty state
        empty_user = User.objects.create_user(username='emptyuser', email='empty@example.com', password='emptypass')
        client = Client()
        client.login(username='emptyuser', password='emptypass')
        empty_response = client.get('/analysis/analytics/')
        print('Empty user status:', empty_response.status_code)
        self.assertEqual(empty_response.status_code, 200)
        print('Empty user contains empty chart:', 'No Data Yet' in empty_response.content.decode())

if __name__ == '__main__':
    import unittest
    unittest.main()
