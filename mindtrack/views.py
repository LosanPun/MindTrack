from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from accounts.models import Profile


def home_view(request):
    """Home page view"""
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    """Dashboard view for logged in users"""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.is_premium and profile.premium_until and timezone.now() > profile.premium_until:
        profile.is_premium = False
        profile.premium_until = None
        profile.save(update_fields=["is_premium", "premium_until"])

    # Get analysis history count
    try:
        from analysis.models import MoodAnalysis

        user_analyses = MoodAnalysis.objects.filter(user=request.user).order_by('-created_at')
        analyses_count = user_analyses.count()
        if profile.is_premium:
            free_remaining = "Unlimited"
        else:
            free_remaining = max(0, 3 - analyses_count)
        recent_analyses = user_analyses[:5]
        last_analysis = user_analyses.first()

        mood_counts = (
            MoodAnalysis.objects.filter(user=request.user)
            .values('detected_mood')
            .annotate(count=Count('id'))
            .order_by('-count', 'detected_mood')
        )

        if mood_counts:
            mood_key = mood_counts[0]['detected_mood']
            most_common_mood = mood_key.capitalize()
        else:
            most_common_mood = '--'
    except Exception:
        analyses_count = 0
        free_remaining = "Unlimited" if profile.is_premium else 3
        recent_analyses = []
        last_analysis = None
        most_common_mood = '--'

    return render(request, 'dashboard/index.html', {
        'user': request.user,
        'free_analyses_remaining': free_remaining,
        'analysis_history': recent_analyses,
        'total_analyses': analyses_count,
        'last_analysis': last_analysis,
        'most_common_mood': most_common_mood,
        'is_locked': False if profile.is_premium else analyses_count >= 3,
        'is_premium': profile.is_premium,
    })
