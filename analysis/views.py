# analysis/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from collections import defaultdict
from datetime import datetime, timedelta
import json
import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO

from .models import MoodAnalysis

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
def export_data_pdf(request):
    """Generate and return PDF with user's mood analysis data"""
    try:
        # Get user's analysis data
        analyses = MoodAnalysis.objects.filter(user=request.user).order_by('-created_at')

        if not analyses.exists():
            # Create a simple PDF with message
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()

            story = []
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )

            story.append(Paragraph("MindTrack - Mood Analysis Report", title_style))
            story.append(Spacer(1, 12))

            message_style = ParagraphStyle(
                'Message',
                parent=styles['Normal'],
                fontSize=14,
                spaceAfter=20,
                alignment=1
            )

            story.append(Paragraph("No mood analysis data found. Start analyzing your mood to generate reports!", message_style))

            doc.build(story)
            buffer.seek(0)

            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mindtrack_report.pdf"'
            return response

        # Create PDF with data
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("MindTrack - Mood Analysis Report", title_style))
        story.append(Spacer(1, 12))

        # User info
        user_info = f"Report for: {request.user.username} | Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Paragraph(user_info, styles['Normal']))
        story.append(Spacer(1, 12))

        # Summary statistics
        total_analyses = analyses.count()
        mood_counts = analyses.values('detected_mood').annotate(count=Count('id')).order_by('-count')

        summary_data = [
            ['Total Analyses', str(total_analyses)],
            ['Most Common Mood', mood_counts[0]['detected_mood'].capitalize() if mood_counts else 'N/A'],
            ['Date Range', f"{analyses.last().created_at.strftime('%Y-%m-%d')} to {analyses.first().created_at.strftime('%Y-%m-%d')}"],
        ]

        summary_table = Table(summary_data, colWidths=[200, 300])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(Paragraph("Summary Statistics", styles['Heading2']))
        story.append(Spacer(1, 12))
        story.append(summary_table)
        story.append(Spacer(1, 24))

        # Mood distribution
        story.append(Paragraph("Mood Distribution", styles['Heading2']))
        story.append(Spacer(1, 12))

        mood_data = [['Mood', 'Count', 'Percentage']]
        for mood_count in mood_counts:
            percentage = f"{(mood_count['count'] / total_analyses * 100):.1f}%"
            mood_data.append([mood_count['detected_mood'].capitalize(), str(mood_count['count']), percentage])

        mood_table = Table(mood_data, colWidths=[150, 100, 100])
        mood_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(mood_table)
        story.append(Spacer(1, 24))

        # Recent analyses
        story.append(Paragraph("Recent Mood Analyses", styles['Heading2']))
        story.append(Spacer(1, 12))

        analysis_data = [['Date', 'Mood', 'Confidence', 'Text Preview']]
        for analysis in analyses[:20]:  # Limit to last 20 analyses
            text_preview = analysis.text[:100] + "..." if len(analysis.text) > 100 else analysis.text
            analysis_data.append([
                analysis.created_at.strftime('%Y-%m-%d %H:%M'),
                analysis.detected_mood.capitalize(),
                f"{analysis.confidence:.1%}",
                text_preview
            ])

        analysis_table = Table(analysis_data, colWidths=[120, 80, 80, 250])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        story.append(analysis_table)

        # Build PDF
        doc.build(story)
        buffer.seek(0)

        # Create response
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="mindtrack_report_{request.user.username}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'

        return response

    except Exception as e:
        # Return error response
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

@login_required
def export_data_pdf(request):
    """Generate and return a PDF with user's mood analysis data"""
    # Get user's analyses
    analyses = MoodAnalysis.objects.filter(user=request.user).order_by('-created_at')

    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
    )

    normal_style = styles['Normal']

    # Build PDF content
    content = []

    # Title
    content.append(Paragraph("MindTrack - Mood Analysis Report", title_style))
    content.append(Spacer(1, 12))

    # User info
    content.append(Paragraph(f"User: {request.user.username}", subtitle_style))
    content.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    content.append(Paragraph(f"Total Analyses: {analyses.count()}", normal_style))
    content.append(Spacer(1, 20))

    if analyses.exists():
        # Summary statistics
        mood_counts = analyses.values('detected_mood').annotate(count=Count('detected_mood')).order_by('-count')
        content.append(Paragraph("Mood Distribution Summary:", subtitle_style))

        summary_data = [['Mood', 'Count', 'Percentage']]
        total = analyses.count()
        for mood_count in mood_counts:
            mood = mood_count['detected_mood'].capitalize()
            count = mood_count['count']
            percentage = f"{(count/total*100):.1f}%"
            summary_data.append([mood, str(count), percentage])

        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(summary_table)
        content.append(Spacer(1, 20))

        # Individual analyses
        content.append(Paragraph("Detailed Analysis History:", subtitle_style))
        content.append(Spacer(1, 12))

        for analysis in analyses:
            # Analysis header
            content.append(Paragraph(f"Analysis #{analysis.id} - {analysis.created_at.strftime('%Y-%m-%d %H:%M')}", styles['Heading3']))

            # Mood and confidence
            content.append(Paragraph(f"Mood: {analysis.get_detected_mood_display()}", normal_style))
            content.append(Paragraph(f"Confidence: {analysis.confidence:.1%}", normal_style))

            # Text (truncated if too long)
            text = analysis.text
            if len(text) > 200:
                text = text[:200] + "..."
            content.append(Paragraph(f"Text: {text}", normal_style))

            # Emotions
            if analysis.emotions:
                content.append(Paragraph("Emotion Breakdown:", styles['Heading4']))
                emotion_data = [['Emotion', 'Percentage']]
                for emotion, percentage in analysis.emotions.items():
                    emotion_data.append([emotion.capitalize(), percentage])

                emotion_table = Table(emotion_data)
                emotion_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                content.append(emotion_table)

            content.append(Spacer(1, 20))
    else:
        content.append(Paragraph("No mood analyses found for this user.", normal_style))

    # Build PDF
    doc.build(content)

    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mindtrack_report_{request.user.username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'

    return response

@login_required
def history_view(request):
    """View analysis history"""
    return render(request, 'analysis/history.html', {
        'user': request.user,
        'analyses': [],
        'total_analyses': 0,
        'free_analyses_remaining': 3,
    })

@login_required
def analytics_view(request):
    """View mood analytics with pie chart and trends"""
    # Pie chart data: mood distribution
    mood_counts = MoodAnalysis.objects.filter(user=request.user).values('detected_mood').annotate(count=Count('detected_mood')).order_by('-count')
    pie_labels = [item['detected_mood'].capitalize() for item in mood_counts]
    pie_data = [item['count'] for item in mood_counts]

    # Trends data: mood counts over time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    trend_data = MoodAnalysis.objects.filter(
        user=request.user,
        created_at__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date', 'detected_mood').annotate(count=Count('id')).order_by('date')

    # Organize trend data by date
    date_moods = defaultdict(lambda: defaultdict(int))
    for item in trend_data:
        date_moods[item['date']][item['detected_mood']] += item['count']

    # Prepare data for line chart: dates and mood counts
    dates = sorted(date_moods.keys())
    moods = ['happy', 'sad', 'angry', 'fear', 'neutral', 'surprise']
    trend_datasets = []
    colors = {
        'happy': '#FFD700',
        'sad': '#4169E1',
        'angry': '#DC143C',
        'fear': '#8A2BE2',
        'neutral': '#808080',
        'surprise': '#FF69B4'
    }
    for mood in moods:
        data = [date_moods[date].get(mood, 0) for date in dates]
        trend_datasets.append({
            'label': mood.capitalize(),
            'data': data,
            'borderColor': colors.get(mood, '#000000'),
            'fill': False,
        })

    return render(request, 'analysis/analytics.html', {
        'pie_labels': json.dumps(pie_labels),
        'pie_data': json.dumps(pie_data),
        'trend_labels': json.dumps([date.strftime('%Y-%m-%d') for date in dates]),
        'trend_datasets': json.dumps(trend_datasets),
    })

@login_required
@require_POST
@csrf_exempt
def save_analysis_ajax(request):
    """AJAX endpoint to save mood analysis"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        detected_mood = data.get('mood_key', '')
        confidence = data.get('confidence', 0.0)
        emotions = data.get('emotions', {})

        if not text or not detected_mood:
            return JsonResponse({
                'success': False,
                'error': 'Missing required data'
            })

        # Save to database
        analysis = MoodAnalysis.objects.create(
            user=request.user,
            text=text,
            detected_mood=detected_mood,
            confidence=float(confidence.strip('%')) / 100,
            emotions=emotions
        )

        return JsonResponse({
            'success': True,
            'analysis_id': analysis.id,
            'message': 'Analysis saved successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
    