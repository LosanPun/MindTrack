# mindtrack/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')

@login_required
def dashboard_view(request):
    """Dashboard view for logged in users"""
    # Get analysis history count
    try:
        from analysis.models import MoodAnalysis
        analyses_count = MoodAnalysis.objects.filter(user=request.user).count()
        free_remaining = max(0, 3 - analyses_count)
        recent_analyses = MoodAnalysis.objects.filter(user=request.user).order_by('-created_at')[:5]
    except:
        analyses_count = 0
        free_remaining = 3
        recent_analyses = []
    
    return render(request, 'dashboard/index.html', {
        'user': request.user,
        'free_analyses_remaining': free_remaining,
        'analysis_history': recent_analyses,
    })