# chatbot/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .services import MindTrackChatbot
from .models import ChatMessage

from django.utils import timezone
import pytz

# Default timezone for Nepal
NEPAL_TZ = pytz.timezone('Asia/Kathmandu')


@login_required
def chat_view(request):
    """Main chat interface"""
    # Get recent chat history (last 50 messages)
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('created_at')[:50]

    return render(request, 'chatbot/chat.html', {
        'user': request.user,
        'chat_history': chat_history,
    })


@login_required
@require_POST
@csrf_exempt
def send_message(request):
    """Handle sending and receiving chat messages"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        mood_context = data.get('mood_context', None)

        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Message cannot be empty'
            })

        # Save user message
        user_chat = ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            is_user=True,
            mood_context=mood_context
        )

        # Detect mood if not provided
        if not mood_context:
            mood_context = MindTrackChatbot.analyze_mood_from_text(user_message)

        # Get bot response
        bot_response = MindTrackChatbot.get_response(user_message, mood_context)

        # Save bot response
        bot_chat = ChatMessage.objects.create(
            user=request.user,
            message=bot_response,
            is_user=False,
            mood_context=mood_context
        )

        # Convert bot timestamp to Nepal timezone
        local_time = timezone.localtime(bot_chat.created_at, NEPAL_TZ)

        return JsonResponse({
            'success': True,
            'response': bot_response,
            'mood_context': mood_context,
            'timestamp': local_time.strftime('%H:%M'),
            'message_id': user_chat.id
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
def get_chat_history(request):
    """Get chat history for the user"""
    try:
        # Get last 50 messages in chronological order
        chat_history = ChatMessage.objects.filter(user=request.user).order_by('created_at')[:50]

        history_data = []
        for chat in chat_history:
            # Convert timestamp to Nepal timezone
            local_time = timezone.localtime(chat.created_at, NEPAL_TZ)

            history_data.append({
                'id': chat.id,
                'message': chat.message,
                'is_user': chat.is_user,
                'mood_context': chat.mood_context,
                'timestamp': local_time.strftime('%H:%M'),
                'date': local_time.strftime('%Y-%m-%d')
            })

        return JsonResponse({
            'success': True,
            'history': history_data,
            'total_messages': len(history_data)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_POST
@csrf_exempt
def clear_chat_history(request):
    """Clear user's chat history"""
    try:
        deleted_count = ChatMessage.objects.filter(user=request.user).delete()[0]
        return JsonResponse({
            'success': True,
            'message': f'Cleared {deleted_count} messages',
            'deleted_count': deleted_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
