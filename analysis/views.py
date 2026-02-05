# analysis/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
import random
from datetime import datetime

@login_required
def analyze_text_view(request):
    """Handle mood analysis request (form submission)"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if not text:
            messages.error(request, 'Please enter some text to analyze.')
            return redirect('dashboard')
        
        # Simulate analysis
        mood_emojis = {
            'happy': '😊',
            'sad': '😢', 
            'angry': '😠',
            'fear': '😨',
            'neutral': '😐',
            'surprise': '😲'
        }
        
        moods = list(mood_emojis.keys())
        detected_mood = random.choice(moods)
        confidence = round(random.uniform(0.7, 0.95), 2)
        
        messages.success(request, f'Analysis complete: {detected_mood.capitalize()} ({confidence:.0%} confidence)')
        return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
@require_POST
@csrf_exempt
def analyze_text_ajax(request):
    """AJAX endpoint for mood analysis"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({
                'success': False,
                'error': 'Please enter some text'
            })
        
        if len(text) < 3:
            return JsonResponse({
                'success': False,
                'error': 'Text is too short (minimum 3 characters)'
            })
        
        # Simulate mood analysis based on keywords
        text_lower = text.lower()
        
        # Keyword detection
        mood_keywords = {
            'happy': ['happy', 'joy', 'good', 'great', 'wonderful', 'excited', 'love', 'amazing', 'fantastic'],
            'sad': ['sad', 'unhappy', 'depressed', 'cry', 'tears', 'lonely', 'miserable', 'bad', 'terrible'],
            'angry': ['angry', 'mad', 'hate', 'annoyed', 'furious', 'rage', 'angry', 'frustrated'],
            'fear': ['fear', 'scared', 'afraid', 'anxious', 'worried', 'nervous', 'panic', 'anxiety'],
            'neutral': ['okay', 'fine', 'normal', 'alright', 'meh', 'whatever', 'ok', 'average'],
            'surprise': ['surprise', 'wow', 'shocked', 'unexpected', 'amazing', 'astonishing']
        }
        
        # Count keyword matches
        scores = {mood: 0 for mood in mood_keywords}
        
        for mood, keywords in mood_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[mood] += 1
        
        # If no matches, use weighted random
        if all(score == 0 for score in scores.values()):
            # Default probabilities
            weights = {'happy': 0.3, 'neutral': 0.3, 'sad': 0.15, 'angry': 0.1, 'fear': 0.1, 'surprise': 0.05}
            detected_mood = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
            confidence = round(random.uniform(0.5, 0.7), 2)
        else:
            # Find dominant mood
            detected_mood = max(scores, key=scores.get)
            total_score = sum(scores.values())
            confidence = round(scores[detected_mood] / total_score, 2)
            confidence = max(0.6, min(0.95, confidence))  # Keep between 0.6-0.95
        
        # Generate emotion percentages
        emotions = {}
        base_emotions = ['happy', 'sad', 'angry', 'fear', 'neutral', 'surprise']
        
        # Give highest score to detected mood
        for emotion in base_emotions:
            if emotion == detected_mood:
                emotions[emotion] = confidence
            else:
                # Other emotions get smaller, random percentages
                remaining = 1 - confidence
                other_count = len(base_emotions) - 1
                avg_other = remaining / other_count
                emotions[emotion] = round(avg_other * random.uniform(0.5, 1.5), 3)
        
        # Normalize to ensure total = 1
        total = sum(emotions.values())
        emotions = {k: round(v/total, 3) for k, v in emotions.items()}
        
        # Format percentages for display
        emotion_percentages = {k: f"{v*100:.1f}%" for k, v in emotions.items()}
        
        return JsonResponse({
            'success': True,
            'data': {
                'mood': detected_mood.capitalize(),
                'mood_key': detected_mood,
                'confidence': f"{confidence:.0%}",
                'emotions': emotion_percentages,
                'emotion_scores': emotions,
                'free_remaining': 2,  # Hardcoded for demo
                'timestamp': datetime.now().strftime('%H:%M'),
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def history_view(request):
    """View analysis history"""
    return render(request, 'analysis/history.html', {
        'user': request.user,
        'analyses': [],
        'total_analyses': 0,
        'free_analyses_remaining': 3,
    })
    