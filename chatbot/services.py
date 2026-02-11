# chatbot/services.py
import random
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from collections import Counter

from .models import UserChatSession
from . import data_resources as resources

class MindTrackChatbot:
    """Enhanced chatbot with user session management and NLP"""
    
    # Track conversation state
    _conversation_state = {
        'last_quotes_given': [],
        'last_songs_given': [],
        'last_poems_given': [],
        'last_exercise_tips_given': [],
        'cheer_up_context': False,
        'last_interaction': None,
        'interaction_count': 0,
        'current_mood': None,
        'last_topic': None
    }
    
    @classmethod
    def _reset_state(cls):
        """Reset conversation state"""
        cls._conversation_state = {
            'last_quotes_given': [],
            'last_songs_given': [],
            'last_poems_given': [],
            'last_exercise_tips_given': [],
            'cheer_up_context': False,
            'last_interaction': None,
            'interaction_count': 0,
            'current_mood': None,
            'last_topic': None
        }
    
    @classmethod
    def _update_state(cls, user_message: str, response: str, mood: str = None, topic: str = None):
        """Update conversation state"""
        cls._conversation_state['interaction_count'] += 1
        cls._conversation_state['last_interaction'] = {
            'timestamp': datetime.now(),
            'user_message': user_message[:100],
            'response': response[:100]
        }
        
        if mood:
            cls._conversation_state['current_mood'] = mood
        
        if topic:
            cls._conversation_state['last_topic'] = topic
        
        # Reset cheer up context UNLESS explicitly mentioned
        if 'cheer' not in user_message.lower() and 'up' not in user_message.lower():
            cls._conversation_state['cheer_up_context'] = False
    
    @staticmethod
    def analyze_mood_from_text(text):
        """Enhanced mood detection from text"""
        text_lower = text.lower()
        
        # Check for motivational requests FIRST (highest priority)
        motivational_keywords = ['motivat', 'inspire', 'encourag', 'need motivation', 'want motivation', 'give me motivation']
        if any(keyword in text_lower for keyword in motivational_keywords):
            return 'motivational'
        
        # Check for specific moods
        if 'lonely' in text_lower or 'alone' in text_lower:
            return 'lonely'
        if 'tired' in text_lower or 'exhausted' in text_lower:
            return 'tired'
        if 'anxious' in text_lower or 'anxiety' in text_lower or 'fear' in text_lower or 'scared' in text_lower or 'nervous' in text_lower:
            return 'anxious'
        if 'angry' in text_lower or 'mad' in text_lower:
            return 'angry'
        if 'happy' in text_lower or 'joy' in text_lower:
            return 'happy'
        if 'sad' in text_lower or 'unhappy' in text_lower:
            return 'sad'
        if 'okay' in text_lower or 'fine' in text_lower or 'ok' in text_lower:
            return 'neutral'
        
        return None
    
    @classmethod
    def _get_fresh_quote(cls, category: str = 'motivational', is_nepali: bool = False) -> str:
        """Get a quote that hasn't been given recently"""
        if is_nepali:
            if category == 'motivational':
                available_quotes = resources.QUOTE_CATEGORIES.get('nepali_motivational', [])
            elif category == 'happy':
                available_quotes = resources.QUOTE_CATEGORIES.get('nepali_happy', [])
            elif category == 'sad':
                available_quotes = resources.QUOTE_CATEGORIES.get('nepali_sad', [])
            elif category == 'calming':
                available_quotes = resources.QUOTE_CATEGORIES.get('nepali_calming', [])
            else:
                available_quotes = resources.QUOTE_CATEGORIES.get('nepali_uplifting', [])
        else:
            available_quotes = resources.QUOTE_CATEGORIES.get(category, resources.QUOTE_CATEGORIES['motivational'])
        
        if not available_quotes:
            return "I don't have quotes in that category yet. How about a poem instead?"
        
        # Remove recently given quotes
        fresh_quotes = [q for q in available_quotes if q not in cls._conversation_state['last_quotes_given']]
        
        # If all quotes have been used, reset and use any
        if not fresh_quotes:
            cls._conversation_state['last_quotes_given'] = []
            fresh_quotes = available_quotes
        
        # Select and track quote
        selected_quote = random.choice(fresh_quotes)
        cls._conversation_state['last_quotes_given'].append(selected_quote)
        
        # Keep only last 5 quotes
        if len(cls._conversation_state['last_quotes_given']) > 5:
            cls._conversation_state['last_quotes_given'] = cls._conversation_state['last_quotes_given'][-5:]
        
        return selected_quote
    
    @classmethod
    def _get_fresh_poem(cls, category: str = 'uplifting', is_nepali: bool = False) -> str:
        """Get a poem that hasn't been given recently"""
        if is_nepali:
            if category == 'happy':
                available_poems = resources.POEM_CATEGORIES.get('nepali_happy', [])
            elif category == 'sad':
                available_poems = resources.POEM_CATEGORIES.get('nepali_sad', [])
            elif category == 'lonely':
                available_poems = resources.POEM_CATEGORIES.get('nepali_lonely', [])
            elif category == 'calming':
                available_poems = resources.POEM_CATEGORIES.get('nepali_calming', [])
            elif category == 'motivational':
                available_poems = resources.POEM_CATEGORIES.get('nepali_motivational', [])
            else:
                available_poems = resources.POEM_CATEGORIES.get('nepali_uplifting', [])
        else:
            available_poems = resources.POEM_CATEGORIES.get(category, resources.POEM_CATEGORIES['uplifting'])
        
        if not available_poems:
            return "I don't have poems in that category yet. How about a quote instead?"
        
        # Remove recently given poems
        fresh_poems = [p for p in available_poems if p not in cls._conversation_state['last_poems_given']]
        
        # If all poems have been used, reset and use any
        if not fresh_poems:
            cls._conversation_state['last_poems_given'] = []
            fresh_poems = available_poems
        
        # Select and track poem
        selected_poem = random.choice(fresh_poems)
        cls._conversation_state['last_poems_given'].append(selected_poem)
        
        # Keep only last 5 poems
        if len(cls._conversation_state['last_poems_given']) > 5:
            cls._conversation_state['last_poems_given'] = cls._conversation_state['last_poems_given'][-5:]
        
        return selected_poem
    
    @classmethod
    def _get_fresh_song(cls, mood: str = None, is_cheer_up: bool = False) -> Dict:
        """Get a song that hasn't been given recently for this mood"""
        if not mood or mood not in resources.YOUTUBE_RESOURCES:
            mood = 'neutral'
        
        # Get resources for this mood
        mood_resources = resources.YOUTUBE_RESOURCES.get(mood, resources.YOUTUBE_RESOURCES['neutral'])
        
        # Filter out recently given songs
        fresh_resources = [r for r in mood_resources if r['id'] not in cls._conversation_state['last_songs_given']]
        
        # If all songs have been used, reset for this mood
        if not fresh_resources:
            # Keep songs from other moods, only reset this mood's songs
            cls._conversation_state['last_songs_given'] = [
                song_id for song_id in cls._conversation_state['last_songs_given']
                if not song_id.startswith(f"{mood}_")
            ]
            fresh_resources = mood_resources
        
        # Select and track song
        selected_resource = random.choice(fresh_resources)
        cls._conversation_state['last_songs_given'].append(selected_resource['id'])
        
        # Keep only last 8 songs
        if len(cls._conversation_state['last_songs_given']) > 8:
            cls._conversation_state['last_songs_given'] = cls._conversation_state['last_songs_given'][-8:]
        
        return selected_resource
    
    @classmethod
    def get_response(cls, user_message: str, user_mood: Optional[str] = None) -> str:
        """Generate enhanced chatbot response - ORIGINAL SIGNATURE"""
        user_message_lower = user_message.lower().strip()
        
        # Reset state on new conversation
        if cls._conversation_state['interaction_count'] == 0:
            cls._reset_state()
        
        # Check for Nepali requests
        is_nepali_request = 'nepali' in user_message_lower or 'नेपाली' in user_message_lower
        
        # CRITICAL FIX: Check mood from CURRENT message
        current_message_mood = cls.analyze_mood_from_text(user_message)
        
        # If current message has a mood, it OVERRIDES everything
        if current_message_mood:
            detected_mood = current_message_mood
            cls._conversation_state['current_mood'] = current_message_mood
        elif user_mood:
            # Use provided user_mood if no mood in current message
            detected_mood = user_mood
            cls._conversation_state['current_mood'] = user_mood
        else:
            # Use existing mood from state
            detected_mood = cls._conversation_state.get('current_mood')
        
        # ========== HANDLE SPECIFIC REQUESTS FIRST ==========
        
        # Check for song/music requests
        if any(word in user_message_lower for word in ['song', 'music', 'youtube', 'playlist', 'listen']):
            # Get song for current mood
            song = cls._get_fresh_song(detected_mood or 'neutral')
            if song:
                mood_intros = {
                    'happy': "To amplify your happy mood, here's some celebratory music:\n\n",
                    'sad': "For your current mood, here's some supportive music:\n\n",
                    'lonely': "For moments of loneliness, here's some comforting music:\n\n",
                    'anxious': "To help calm and ground your anxiety, try this:\n\n",
                    'angry': "To help channel or calm your anger, this might help:\n\n",
                    'tired': "For restorative support when feeling tired:\n\n",
                    'neutral': "For your current state, here's some balanced music:\n\n",
                    'motivational': "To boost your motivation, here's some inspiring music:\n\n"
                }
                
                intro = mood_intros.get(detected_mood or 'neutral', "Here's some music for you:\n\n")
                response = f"{intro}🎵 **{song['title']}**\n🔗 {song['url']}\n💡 {song['description']}\n\n📝 Copy the URL above and paste into your browser to open YouTube"
                cls._update_state(user_message, response, detected_mood, 'music')
                return response
        
        # Check for exercise/activity requests
        if any(word in user_message_lower for word in ['exercise', 'workout', 'activity', 'tip', 'suggestion', 'physical']):
            # Determine mood for exercise
            mood_for_exercise = detected_mood or 'neutral'
            exercise_tips = resources.EXERCISE_TIPS.get(mood_for_exercise, resources.EXERCISE_TIPS['neutral'])
            
            if exercise_tips:
                # Get fresh exercise tip
                fresh_tips = [t for t in exercise_tips if t not in cls._conversation_state['last_exercise_tips_given']]
                if not fresh_tips:
                    cls._conversation_state['last_exercise_tips_given'] = []
                    fresh_tips = exercise_tips
                
                selected_tip = random.choice(fresh_tips)
                cls._conversation_state['last_exercise_tips_given'].append(selected_tip)
                if len(cls._conversation_state['last_exercise_tips_given']) > 5:
                    cls._conversation_state['last_exercise_tips_given'] = cls._conversation_state['last_exercise_tips_given'][-5:]
                
                exercise_intros = {
                    'happy': "To celebrate your happy mood, here's an energizing exercise idea:\n\n",
                    'sad': "For moments of sadness, gentle movement can be particularly helpful:\n\n",
                    'lonely': "When feeling lonely, these exercises might help create connection:\n\n",
                    'anxious': "For anxiety relief, try this grounding exercise:\n\n",
                    'angry': "To safely channel angry energy, consider this exercise:\n\n",
                    'tired': "When feeling tired, gentle movement can actually boost energy:\n\n",
                    'neutral': "For your current state, here's a balanced exercise suggestion:\n\n",
                    'motivational': "To build motivation, start with this achievable exercise:\n\n"
                }
                
                intro = exercise_intros.get(mood_for_exercise, "Here's an exercise tip for you:\n\n")
                response = f"{intro}{selected_tip}"
                cls._update_state(user_message, response, detected_mood, 'exercise')
                return response
        
        # Handle "how to" questions - ADD THIS SECTION HERE
        if user_message_lower.startswith('how to') or 'how do i' in user_message_lower:
            # Extract the topic
            if 'share' in user_message_lower and 'happiness' in user_message_lower:
                response = "Sharing happiness with others is wonderful! Here are some ways:\n\n1. **Express gratitude** - Thank people who make you happy\n2. **Share positive stories** - Tell others about good things happening\n3. **Give compliments** - Spread positivity with kind words\n4. **Invite others** - Include people in your happy activities\n5. **Smile genuinely** - Your smile can brighten someone's day 😊\n\nWhat aspect of sharing happiness interests you most?"
                cls._update_state(user_message, response, detected_mood, 'advice')
                return response
            elif 'overcome' in user_message_lower and 'fear' in user_message_lower:
                response = "Overcoming fear takes courage. Here are constructive approaches:\n\n" + resources.CONSTRUCTIVE_WAYS['anxious'][0]
                cls._update_state(user_message, response, detected_mood, 'advice')
                return response
            elif 'deal' in user_message_lower and 'nervous' in user_message_lower:
                response = "Dealing with nervousness:\n\n" + resources.CONSTRUCTIVE_WAYS['anxious'][1]
                cls._update_state(user_message, response, detected_mood, 'advice')
                return response
            elif any(word in user_message_lower for word in ['happy', 'happiness', 'joy']):
                response = "To cultivate more happiness:\n\n" + resources.CONSTRUCTIVE_WAYS['happy'][2]
                cls._update_state(user_message, response, detected_mood, 'advice')
                return response
            elif any(word in user_message_lower for word in ['sad', 'sadness', 'unhappy']):
                response = "When feeling sad:\n\n" + resources.CONSTRUCTIVE_WAYS['sad'][1]
                cls._update_state(user_message, response, detected_mood, 'advice')
                return response
            else:
                # General "how to" response
                response = "That's a great question! Could you tell me more about what specific area you'd like guidance on? I can help with emotional management, constructive strategies, or specific techniques."
                cls._update_state(user_message, response, detected_mood, 'advice')
                return response
        
        # Handle Nepali quote requests
        if is_nepali_request and 'quote' in user_message_lower:
            # Determine Nepali quote category
            if 'motivat' in user_message_lower:
                category = 'motivational'
            elif 'happy' in user_message_lower:
                category = 'happy'
            elif 'sad' in user_message_lower:
                category = 'sad'
            elif 'calm' in user_message_lower:
                category = 'calming'
            else:
                category = 'motivational'
            
            quote = cls._get_fresh_quote(category, is_nepali=True)
            response = f"Here's a Nepali quote for you:\n\n\"{quote}\""
            cls._update_state(user_message, response, detected_mood, 'quote')
            return response
        
        # Handle Nepali poem requests
        if is_nepali_request and ('poem' in user_message_lower or 'poetry' in user_message_lower):
            # Determine Nepali poem category
            if 'happy' in user_message_lower:
                category = 'happy'
            elif 'sad' in user_message_lower:
                category = 'sad'
            elif 'lonely' in user_message_lower:
                category = 'lonely'
            elif 'calm' in user_message_lower:
                category = 'calming'
            elif 'motivat' in user_message_lower:
                category = 'motivational'
            else:
                category = 'uplifting'
            
            poem = cls._get_fresh_poem(category, is_nepali=True)
            response = f"Here's a Nepali poem for you:\n\n{poem}"
            cls._update_state(user_message, response, detected_mood, 'poem')
            return response
        
        # Handle regular quote requests
        if 'quote' in user_message_lower or 'quotes' in user_message_lower:
            # Determine quote category
            if 'motivational' in user_message_lower or 'motivate' in user_message_lower:
                category = 'motivational'
            elif 'sad' in user_message_lower or 'emotional' in user_message_lower:
                category = 'emotional'
            elif 'happy' in user_message_lower or 'uplifting' in user_message_lower:
                category = 'uplifting'
            elif 'mindful' in user_message_lower:
                category = 'mindfulness'
            else:
                # Determine quote category based on mood
                if detected_mood in ['anxious', 'sad', 'lonely']:
                    category = 'emotional'
                elif detected_mood == 'happy':
                    category = 'uplifting'
                elif detected_mood == 'motivational':
                    category = 'motivational'
                else:
                    category = 'mindfulness'
            
            quote = cls._get_fresh_quote(category)
            response = f"Here's a quote for you:\n\n\"{quote}\""
            cls._update_state(user_message, response, detected_mood, 'quote')
            return response
        
        # Handle poem requests
        if 'poem' in user_message_lower or 'poetry' in user_message_lower:
            # Determine poem category
            if 'motivat' in user_message_lower:
                category = 'motivational'
            elif 'uplift' in user_message_lower:
                category = 'uplifting'
            elif 'happy' in user_message_lower:
                category = 'happy'
            elif 'sad' in user_message_lower:
                category = 'sad'
            elif 'lonely' in user_message_lower:
                category = 'lonely'
            elif 'calm' in user_message_lower:
                category = 'calming'
            else:
                # Default based on mood
                if detected_mood == 'happy':
                    category = 'happy'
                elif detected_mood == 'sad':
                    category = 'sad'
                elif detected_mood == 'lonely':
                    category = 'lonely'
                elif detected_mood in ['anxious', 'tired']:
                    category = 'calming'
                elif detected_mood == 'motivational':
                    category = 'motivational'
                else:
                    category = 'uplifting'
            
            poem = cls._get_fresh_poem(category)
            response = f"Here's a poem for you:\n\n{poem}"
            cls._update_state(user_message, response, detected_mood, 'poem')
            return response
        
        # Check for "how are you" specifically
        if 'how are you' in user_message_lower:
            response = random.choice([
                "Thank you for asking! I'm here and fully present to support you. How are you feeling today?",
                "I'm doing well, and I'm focused on being here for you. How has your day been so far?",
                "I'm present and ready to listen. Thanks for checking in! How are you really doing?",
            ])
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for greetings
        greetings = ['hello', 'hi', 'hey', 'greetings', 'hey buddy']
        if any(greet in user_message_lower for greet in ['hello', 'hi', 'hey', 'greetings', 'how you doing', 'how you doin', 'how ya doing']) and cls._conversation_state['interaction_count'] < 2:
            response = random.choice(resources.GREETINGS)
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Mood-based responses
        mood_responses = resources.MOOD_RESPONSES
        
        if detected_mood and detected_mood in mood_responses:
            if detected_mood == 'sad':
                if cls._conversation_state['cheer_up_context']:
                    responses = mood_responses['sad']['cheer_up']
                else:
                    responses = mood_responses['sad']['general']
            else:
                responses = mood_responses[detected_mood]
            
            response = random.choice(responses)
            cls._update_state(user_message, response, detected_mood, 'mood')
            return response
        
        # Default empathetic responses
        empathetic_responses = [
            "Thank you for sharing that with me. I'm listening with care and attention. 🤗",
            "I hear you. Would you like to explore constructive ways to work with what you're feeling?",
            "That sounds important. How is this sitting with you emotionally and physically?",
            "I'm fully present with what you're sharing. Your experience matters here. 💫",
            "Thank you for being open with me. Let's proceed in whatever way feels most supportive for you. 🌟"
        ]
        
        response = random.choice(empathetic_responses)
        cls._update_state(user_message, response, detected_mood)
        return response
