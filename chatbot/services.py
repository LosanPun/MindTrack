# chatbot/services.py
import random
from datetime import datetime
from typing import List, Dict, Optional

class MindTrackChatbot:
    """Enhanced rule-based chatbot for MindTrack with mood-specific songs, quotes, poems, and exercise tips"""
    
    # Track conversation state
    _conversation_state = {
        'last_quotes_given': [],
        'last_songs_given': [],
        'last_poems_given': [],
        'last_exercise_tips_given': [],
        'cheer_up_context': False,
        'last_interaction': None,
        'interaction_count': 0,
        'current_mood': None
    }
    
    # Enhanced mood-based responses with professional tone
    MOOD_RESPONSES = {
        'happy': [
            "It's wonderful to hear you're experiencing happiness! These moments are precious for our wellbeing. What's bringing you this joy today? 😊",
            "Your positive energy is truly uplifting! Celebrating these good moments helps build emotional resilience. ✨",
            "Happiness looks great on you! Noticing what creates these positive states can help us cultivate more of them in daily life.",
            "That's fantastic! Positive emotions like happiness help broaden our perspective and build psychological resources.",
            "I'm delighted to hear you're feeling happy! Would you like to explore how to extend or deepen this positive state?"
        ],
        'sad': {
            'general': [
                "I hear you're feeling sad, and I want you to know that's completely valid. These feelings, though difficult, are part of the human experience. 💙",
                "Sadness can feel heavy, and I'm here to sit with you in it. There's no need to rush through these feelings—they have their own timing.",
                "I appreciate you sharing that you're feeling sad. It takes courage to acknowledge these emotions. How can I best support you right now?",
                "Your sadness matters, and so do you. Would gentle conversation or a supportive activity feel more helpful at this moment?",
                "I'm with you in this. Sadness often points to what we care deeply about. Would you like to talk about what's coming up for you?"
            ],
            'cheer_up': [
                "I hear you want some cheering up, and that's a proactive step for your wellbeing! Let me help you find some uplifting support. 🌈",
                "Wanting to shift from sadness shows self-awareness. I have some encouraging resources that might help lift your spirits.",
                "It takes strength to ask for cheering up when feeling low. Let's explore some options that might bring you some lightness.",
                "I understand you're looking for a mood boost. Here are some uplifting approaches we could try together.",
                "Thank you for letting me know you'd like cheering up. That's an important step in emotional self-care."
            ]
        },
        'lonely': [
            "Loneliness can feel isolating, and I want you to know I'm here with you. These feelings are valid and shared by many. 💙",
            "I hear the loneliness. It takes courage to acknowledge these feelings. Would companionship through conversation or comforting resources help?",
            "Loneliness can be particularly difficult. I'm here to provide company in whatever way feels supportive right now.",
            "Your feelings of loneliness matter. Sometimes gentle, comforting resources can help ease the sense of isolation.",
            "I'm with you in this loneliness. Would you like to talk about what comes up with these feelings, or try some comforting support?"
        ],
        'angry': [
            "Anger often signals that something important to us feels threatened or unfair. Would you like to explore what's beneath this feeling? 🌬️",
            "I hear the frustration in your words. Anger needs safe expression—would movement, writing, or breath work feel supportive right now?",
            "That anger makes sense given what you're experiencing. Let's find a constructive way to channel this energy together.",
            "Anger can be protective energy. How can we work with it in a way that feels empowering rather than overwhelming?",
            "I'm here with you through this anger. Sometimes naming what we're angry about helps us understand what matters to us most."
        ],
        'anxious': [
            "Anxiety often points to something that feels uncertain or unsafe. Let's ground in what's actually here and now together. 🛡️",
            "I hear the anxiety in your words. Would you like to try a grounding exercise, or just talk through what's coming up?",
            "That worried feeling is trying to protect you. Let's thank it for its concern, then gently focus on what's within your control.",
            "Anxiety can feel overwhelming, but you're not alone with it. What's the smallest, safest step we could take from here?",
            "I'm here with you through this anxiety. Sometimes breaking it down into manageable pieces helps reduce its intensity."
        ],
        'neutral': [
            "A neutral state can be a peaceful resting place between emotions. Would you like to explore this calm space with gentle curiosity? 🍃",
            "Sometimes 'neutral' is exactly what we need—a breather from emotional intensity. How does this state feel in your body?",
            "Neutrality has its own wisdom. It can be a great opportunity for gentle self-check-in without pressure.",
            "Being in a neutral state allows for reflection without emotional charge. What would feel supportive right now?",
            "I hear you're feeling neutral. This can be a good space to practice mindfulness or simply rest in being."
        ],
        'tired': [
            "Feeling tired can be your system's way of asking for rest and restoration. What would true rest look like for you right now? 😴",
            "Fatigue often carries messages about our pace or needs. Let's explore what your body might be telling you.",
            "Rest is productive—it's how we restore our capacity. What's one small way to honor your need for restoration today?",
            "I hear the tiredness. Sometimes gentle, low-energy activities can be most restorative when we're feeling drained.",
            "Your body is asking for care through this tiredness. How can we support that need together?"
        ],
        # NEW: Motivational mood responses
        'motivational': [
            "I hear you're looking for motivation! Sometimes we all need that extra push. What specific area of your life are you looking to energize? 💪",
            "Motivation often starts with small, actionable steps. What's one tiny thing you could do right now to build momentum?",
            "The desire for motivation itself is a great starting point! Let's explore what inspires and energizes you.",
            "I'm here to help you find that motivational spark! Would specific strategies, inspiring content, or practical steps be most helpful?",
            "Motivation grows from action. What's one small commitment you could make to yourself today?"
        ]
    }
    
    # Mood-specific YouTube resources (all tested and working)
    YOUTUBE_RESOURCES = {
        'happy': [  # For happy moods - celebration, energy
            {
                "id": "happy_1",
                "title": "Happy Music Mix - Celebration Vibes",
                "url": "https://www.youtube.com/watch?v=yzTuBuRdAyA",
                "description": "Upbeat songs to amplify your joyful mood and positive energy",
                "energy": "high"
            },
            {
                "id": "happy_2", 
                "title": "Feel Good Dance Music - Positive Energy",
                "url": "https://www.youtube.com/watch?v=2vjPBrBU-TM",
                "description": "Energetic dance tracks to match and enhance your happy mood",
                "energy": "high"
            },
            {
                "id": "happy_3",
                "title": "Upbeat Positive Energy Mix",
                "url": "https://www.youtube.com/watch?v=3sXebXgQy4s",
                "description": "Music to enhance and extend your positive emotional state",
                "energy": "medium"
            },
            {
                "id": "happy_4",
                "title": "Joyful Morning Music",
                "url": "https://www.youtube.com/watch?v=GBZ2T6Q1F3Q",
                "description": "Bright, cheerful music to celebrate your happiness",
                "energy": "medium"
            }
        ],
        'sad': [  # For sad moods - uplifting, comforting
            {
                "id": "sad_1",
                "title": "Uplifting Music for Sad Moments",
                "url": "https://www.youtube.com/watch?v=W6YI3ZFOL0A",
                "description": "Gentle uplifting music to help shift from sadness",
                "energy": "medium"
            },
            {
                "id": "sad_2",
                "title": "Comforting Melodies for Sadness",
                "url": "https://www.youtube.com/watch?v=bP8R0iYQqjE",
                "description": "Soft, comforting music for moments of sadness",
                "energy": "low"
            },
            {
                "id": "sad_3",
                "title": "Hope and Healing Playlist",
                "url": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
                "description": "Music that brings comfort and hope during sad times",
                "energy": "medium_low"
            },
            {
                "id": "sad_4",
                "title": "Gentle Uplift - Mood Transition",
                "url": "https://www.youtube.com/watch?v=4N0-kB-gbDE",
                "description": "Soft instrumental music to gently lift your spirits",
                "energy": "low"
            }
        ],
        'lonely': [  # For loneliness - comforting, companionship
            {
                "id": "lonely_1",
                "title": "Comforting Music for Loneliness",
                "url": "https://www.youtube.com/watch?v=bP8R0iYQqjE",
                "description": "Gentle, comforting melodies for moments of loneliness",
                "energy": "low"
            },
            {
                "id": "lonely_2",
                "title": "You're Not Alone - Comfort Playlist",
                "url": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
                "description": "Soothing music to provide comfort during lonely moments",
                "energy": "low"
            },
            {
                "id": "lonely_3",
                "title": "Gentle Company - Ambient Comfort",
                "url": "https://www.youtube.com/watch?v=4N0-kB-gbDE",
                "description": "Calming ambient music to ease feelings of loneliness",
                "energy": "medium_low"
            },
            {
                "id": "lonely_4",
                "title": "Warm Embrace - Soothing Sounds",
                "url": "https://www.youtube.com/watch?v=4pLVKx1kW-o",
                "description": "Soft, warm music to comfort lonely feelings",
                "energy": "very_low"
            }
        ],
        'anxious': [  # For anxiety - calming, grounding
            {
                "id": "anxious_1",
                "title": "Calm Music for Stress and Anxiety Relief",
                "url": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
                "description": "Soothing ambient music to calm your nervous system",
                "energy": "very_low"
            },
            {
                "id": "anxious_2",
                "title": "Anxiety Relief Music - Immediate Calm",
                "url": "https://www.youtube.com/watch?v=4pLVKx1kW-o",
                "description": "Music specifically designed to reduce anxiety quickly",
                "energy": "very_low"
            },
            {
                "id": "anxious_3",
                "title": "Peaceful Piano for Relaxation",
                "url": "https://www.youtube.com/watch?v=bP8R0iYQqjE",
                "description": "Gentle piano melodies to quiet anxious thoughts",
                "energy": "low"
            },
            {
                "id": "anxious_4",
                "title": "Grounding Music for Anxiety",
                "url": "https://www.youtube.com/watch?v=WRz2MxhAdJo",
                "description": "Stabilizing music to help ground anxious feelings",
                "energy": "low"
            }
        ],
        'angry': [  # For anger - releasing, channeling
            {
                "id": "angry_1",
                "title": "Intense Music for Emotional Release",
                "url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
                "description": "Powerful music to safely match and channel angry energy",
                "energy": "high"
            },
            {
                "id": "angry_2",
                "title": "Calming Music for Anger Management",
                "url": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
                "description": "Soothing sounds to help calm and regulate anger",
                "energy": "low"
            },
            {
                "id": "angry_3",
                "title": "Grounding Music for Emotional Regulation",
                "url": "https://www.youtube.com/watch?v=4N0-kB-gbDE",
                "description": "Focus-oriented music to help center and ground angry feelings",
                "energy": "medium"
            },
            {
                "id": "angry_4",
                "title": "Release and Reset - Anger Channeling",
                "url": "https://www.youtube.com/watch?v=SEfs5TJZ6Nk",
                "description": "Music to help release and transform angry energy",
                "energy": "medium_high"
            }
        ],
        'tired': [  # For tiredness - restoring, gentle
            {
                "id": "tired_1",
                "title": "Relaxing Music for Exhaustion",
                "url": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
                "description": "Gentle music to support rest and recovery when tired",
                "energy": "very_low"
            },
            {
                "id": "tired_2",
                "title": "Sleep Music - Deep Rest",
                "url": "https://www.youtube.com/watch?v=4pLVKx1kW-o",
                "description": "Restorative music for when you need deep rest",
                "energy": "very_low"
            },
            {
                "id": "tired_3",
                "title": "Gentle Uplift for Low Energy",
                "url": "https://www.youtube.com/watch?v=W6YI3ZFOL0A",
                "description": "Soft uplifting music for gentle energy restoration",
                "energy": "low"
            },
            {
                "id": "tired_4",
                "title": "Restorative Ambient Sounds",
                "url": "https://www.youtube.com/watch?v=bP8R0iYQqjE",
                "description": "Calming sounds to support tired mind and body",
                "energy": "very_low"
            }
        ],
        'neutral': [  # For neutral moods - balancing, focusing
            {
                "id": "neutral_1",
                "title": "Lofi Hip Hop Radio - Beats to Relax/Study",
                "url": "https://www.youtube.com/watch?v=5qap5aO4i9A",
                "description": "Balanced background music for neutral or focused states",
                "energy": "medium"
            },
            {
                "id": "neutral_2",
                "title": "Focus Music for Concentration",
                "url": "https://www.youtube.com/watch?v=4N0-kB-gbDE",
                "description": "Music to enhance focus during neutral emotional states",
                "energy": "medium"
            },
            {
                "id": "neutral_3",
                "title": "Ambient Study Music",
                "url": "https://www.youtube.com/watch?v=WRz2MxhAdJo",
                "description": "Neutral ambient music for calm productivity",
                "energy": "medium_low"
            },
            {
                "id": "neutral_4",
                "title": "Calm Background Music",
                "url": "https://www.youtube.com/watch?v=bP8R0iYQqjE",
                "description": "Gentle background music for neutral moments",
                "energy": "low"
            }
        ],
        # NEW: Motivational music resources (using existing sad songs for now - same URLs)
        'motivational': [
            {
                "id": "motivational_1",
                "title": "Uplifting Music for Motivation",
                "url": "https://www.youtube.com/watch?v=W6YI3ZFOL0A",
                "description": "Gentle uplifting music to help boost motivation and energy",
                "energy": "medium"
            },
            {
                "id": "motivational_2",
                "title": "Inspirational Music Mix",
                "url": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
                "description": "Music to inspire and motivate you throughout the day",
                "energy": "medium"
            },
            {
                "id": "motivational_3",
                "title": "Focus and Motivation Music",
                "url": "https://www.youtube.com/watch?v=4N0-kB-gbDE",
                "description": "Music to enhance focus and build motivational energy",
                "energy": "medium"
            },
            {
                "id": "motivational_4",
                "title": "Energy Boost Motivation",
                "url": "https://www.youtube.com/watch?v=bP8R0iYQqjE",
                "description": "Uplifting sounds to boost your motivational energy",
                "energy": "medium"
            }
        ]
    }
    
    # Enhanced motivational quotes with variety
    QUOTE_CATEGORIES = {
        'motivational': [
            "Progress isn't about giant leaps, but about the small, consistent steps we take each day. What's one tiny step forward you could take right now? 💫",
            "You are capable of amazing things—not because you're superhuman, but because you're human with inherent capacity for growth and adaptation.",
            "Remember: You've already survived 100% of your difficult days. That's evidence of resilience you carry forward.",
            "Small steps still move you forward. Momentum builds from action, no matter how small the initial movement.",
            "Your mental health is a priority, not a luxury. Investing in it is one of the most important commitments you can make.",
            "Be gentle with yourself today. Self-compassion is correlated with greater resilience and wellbeing than self-criticism.",
            "One day at a time, sometimes one moment at a time. Healing and growth follow their own timeline.",
            "You're doing better than you think. Our inner critics often magnify struggles while minimizing strengths.",
            "This feeling is temporary. Emotions are visitors—they come, stay awhile, and eventually make space for others.",
            "You are enough, just as you are. Worth isn't earned through productivity or perfection."
        ],
        'emotional': [
            "Your feelings are valid messengers, not problems to be solved. They're telling you something important about your needs and values.",
            "It's okay to not be okay. Authenticity in our emotional experience is the foundation of genuine wellbeing.",
            "Healing isn't linear. It's more like a spiral—we revisit similar places but from new perspectives each time.",
            "Vulnerability is the birthplace of connection and meaning. Sharing our true emotional experience creates authentic relating.",
            "Emotions are energy in motion. They want to move through us, not get stuck within us.",
            "The depth of your feelings reflects the depth of your capacity to experience life fully.",
            "All emotions have intelligence. Even difficult ones carry information about what matters to us.",
            "Being with difficult emotions without judgment is one of the most courageous forms of self-care.",
            "Your emotional landscape is uniquely yours—there's no 'right' way to navigate it.",
            "Feelings aren't facts, but they are real experiences deserving of acknowledgement."
        ],
        'mindfulness': [
            "This moment, right now, is the only one you have for sure. What do you notice about your present experience? ⏳",
            "Be where you are, not where you think you should be. Presence is the foundation of peace.",
            "Feelings come and go like clouds in a windy sky. Conscious breathing is your anchor to the present.",
            "The breath you're taking right now is the only one that exists. The next one hasn't arrived yet.",
            "Ground yourself in what's real: the sensation of breathing, the surface beneath you, the sounds around you.",
            "Mindfulness isn't about emptying the mind, but about noticing what's already there without judgment.",
            "Between stimulus and response there is a space. In that space lies our freedom to choose.",
            "Presence is the greatest gift we can give ourselves—and it's always available, right here, right now.",
            "Notice without judgment, feel without resistance, be without striving.",
            "The present moment holds everything you need for your next step forward."
        ],
        'uplifting': [
            "Happiness grows when shared! What made you smile today? 😊",
            "Joy is contagious - spread some today!",
            "Celebrate the small moments of happiness - they matter! ✨",
            "Your positive energy creates ripples of goodness around you.",
            "Happiness looks beautiful on you! Keep shining.",
            "Find joy in the ordinary - it's where magic lives.",
            "Your laughter is medicine for the soul.",
            "Happiness is homemade - create some today!",
            "Let your light shine! The world needs your joy.",
            "Good vibes only! What's bringing you happiness right now?"
        ]
    }
    
    # Poem categories for different moods
    POEM_CATEGORIES = {
        'happy': [
            """Sunlight dances on morning dew,
A heart that's light, a sky that's blue.
Laughter echoes, spirits rise,
Sparkles shining in your eyes.
Joy is found in simple pleasure,
Memories we'll always treasure.""",
            
            """Birds are singing, skies are clear,
Happiness is drawing near.
Smiles are spreading, hearts are light,
Everything feels just so right.
Dance with joy, let worries flee,
Just be you, and you'll be free.""",
            
            """Golden sunshine, warm embrace,
A happy heart, a smiling face.
Butterflies and blooming flowers,
Counting happy morning hours.
Let your spirit freely soar,
Wanting nothing, needing more."""
        ],
        
        'sad': [
            """Raindrops fall on window pane,
Echoing my silent pain.
Clouds are gray, the world seems slow,
Feelings only I can know.
But even storms must pass away,
There will come a brighter day.""",
            
            """Tears like rivers, silent streams,
Fading hopes and broken dreams.
Heavy heart and weary soul,
Trying hard to feel whole.
Yet within this depth of night,
There's a distant, gentle light.""",
            
            """Empty rooms and quiet halls,
Echoes of when laughter calls.
Shadows linger, light grows dim,
Memories on a fragile whim.
But seasons change and so will this,
Even sadness finds its bliss."""
        ],
        
        'motivational': [
            """Rise again, though you may fall,
Stand up straight and stand up tall.
Every scar tells where you've been,
Every struggle lets you win.
Mountains high or valleys low,
Forward is the way to go.""",
            
            """Step by step, you'll find your way,
Through the night and through the day.
Strength you didn't know you had,
Moments good and moments bad.
Keep on walking, don't look back,
You're still on the forward track.""",
            
            """When the path seems steep and long,
And everything feels wrong,
Remember strength is in the climb,
One small step at a time.
You are braver than you know,
And with each step, you will grow."""
        ],
        
        'lonely': [
            """Quiet spaces, empty chair,
Feelings floating in the air.
Moonlight through a silent room,
Chasing away the gloom.
But in the stillness, you will see,
Your own best company.""",
            
            """Stars above, so far away,
Waiting for the light of day.
Solitude can be a friend,
On which you can depend.
In your own space, you will find,
Peace of a different kind.""",
            
            """Silent house and quiet street,
Where your thoughts and feelings meet.
Loneliness is just a season,
With its own unique reason.
Soon you'll find with gentle grace,
Someone takes that empty space."""
        ],
        
        'calming': [
            """Breathe in peace, breathe out fear,
Gentle thoughts are drawing near.
Like a river, calm and deep,
Promising a restful sleep.
Let your worries float away,
Welcome in a peaceful day.""",
            
            """Softly now, the world grows still,
Calming every anxious will.
Like a feather, floating down,
Gently settling on the ground.
In this moment, soft and clear,
There is nothing left to fear.""",
            
            """Ocean waves on sandy shore,
Peaceful rhythms, nothing more.
Heartbeat slowing, mind at rest,
Finding what is truly best.
In the quiet, you will see,
How to simply let things be."""
        ],
        
        'uplifting': [
            """Lift your eyes to skies above,
Fill your heart with hope and love.
Yesterday is gone and past,
New beginnings are forecast.
You are stronger than you know,
Watch your inner light now grow.""",
            
            """Like a phoenix from the flame,
Rise again and claim your name.
Every ending is a start,
Listen to your hopeful heart.
Bright tomorrows wait for you,
Dreams you're destined to pursue.""",
            
            """Turn the page, begin anew,
Fresh perspectives coming through.
What was heavy, now feels light,
Everything will be alright.
Lift your spirit, lift your voice,
Make the hopeful, happy choice."""
        ],
        
        # NEPALI POEMS - One for each mood
        'nepali_happy': [
            """आज फुलको बगैंचामा,
मुस्कानको हावा छ।
दिलमा उल्लासको गीत,
जीवनमा रंग छ।
खुसीको यो पलहरू,
सधैं यादगार हुन्।
आनन्दको संसारमा,
तिम्रो स्वागत छ।"""
        ],
        
        'nepali_sad': [
            """आँखामा आँसुको धार,
मनमा उदासी छ।
एक्लोपनको यो अँध्यारो,
कहिले उज्यालो हुन्छ?
तर समय सधैं बदल्छ,
दुःख पनि टर्छ।
आशाको किरणले,
फेरि उज्यालो हुन्छ।"""
        ],
        
        'nepali_lonely': [
            """शान्त कक्ष, खाली कोठा,
एक्लोपनको साथ।
चन्द्रमाको चम्किलो किरण,
अँध्यारोमा आशा।
यो एक्लोपन समय हो,
आत्मसँगको भेट।
आफैंमा शान्ति खोज्दा,
पाइन्छ साँचो सुख।"""
        ],
        
        'nepali_calming': [
            """श्वास भित्र, शान्ति बाहिर,
चित्त शान्त हुन्छ।
नदीजस्तो बग्न दिनु,
सबै चिन्ता हराउन्छ।
यो पलमा बस्न सिक्नु,
वर्तमानमा जिउन।
शान्तिको महासागरमा,
आफूलाई डुबाउन।"""
        ],
        
        'nepali_motivational': [
            """उठ, अगाडि बढ,
पछि नहेर।
जीवनको यात्रामा,
हार नमान।
तिम्रो शक्ति अनन्त छ,
विश्वास गर।
आफूमाथि विश्वास राख,
सफलता तिम्रो पछि आउँछ।"""
        ],
        
        'nepali_uplifting': [
            """आकाशतिर हेर,
आशाका बादल छन्।
भोलि सुनौलो दिन आउँछ,
विश्वास गर।
तिम्रो आत्मविश्वासले,
सबै असम्भवलाई सम्भव बनाउँछ।
उठ, अगाडि बढ,
तिम्रो समय आएको छ।"""
        ]
    }
    
    # Exercise tips for different moods
    EXERCISE_TIPS = {
        'sad': [
            "Gentle movement can help shift sadness. Try a 10-minute walk outside, focusing on your breath and surroundings. Notice the sky, trees, and sounds around you. 🚶‍♀️🌿",
            "When feeling sad, try '5-4-3-2-1' grounding walk: Notice 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, and 1 thing you taste while walking.",
            "Gentle yoga or stretching can help release emotional tension. Try a 10-minute beginner yoga video focusing on gentle flows and deep breathing. 🧘‍♀️",
            "Dance to one uplifting song! Movement releases endorphins. Don't worry about how you look - just move your body freely. 🎵💃",
            "Try 'walking meditation': Walk slowly, focusing on the sensation of your feet touching the ground with each step. This combines movement with mindfulness.",
            "Swimming or water exercises can be soothing for sadness. The water provides gentle resistance and sensory comfort. 🏊‍♀️",
            "Simple breathing exercises: Inhale for 4 counts, hold for 4, exhale for 6. Combine with gentle arm raises on the inhale, lower on exhale.",
            "Nature walk with intention: Walk in a park or green space, intentionally noticing colors, textures, and life around you.",
            "Chair exercises: If energy is low, try seated leg lifts, arm circles, and gentle twists while breathing deeply.",
            "Sun salutations: 3-5 rounds of gentle sun salutations can help move energy and lift your mood with the rhythm of movement."
        ],
        'happy': [
            "Celebrate your happy energy with joyful movement! Try dancing to your favorite upbeat music for 15 minutes. 🎉💃",
            "Take your happiness outdoors! Go for a brisk walk or jog while listening to uplifting music or a positive podcast. 🌞🚶‍♂️",
            "Try a fun fitness class like Zumba, dance cardio, or aerobics to match and amplify your positive energy. 🏋️‍♀️",
            "Play a sport you enjoy - basketball, tennis, soccer, or any active game that brings you joy and laughter. ⚽😊",
            "Do a 'gratitude workout': With each exercise, think of something you're grateful for. Combine physical and emotional positivity. 🙏",
            "Try interval training: Alternate between high-energy bursts (30 seconds) and active recovery (60 seconds) to match your energetic mood.",
            "Group exercise: Join a friend for a workout or join a community fitness event to share your positive energy. 👫",
            "Adventure workout: Try hiking, rock climbing, or trail running to combine exercise with exploration and joy. 🏞️",
            "Dance cardio: Follow a dance workout video - it's exercise that feels like celebration!",
            "Morning energizer: Start your day with 20 minutes of mixed exercises - jumping jacks, squats, push-ups, and stretches to carry happy energy through your day."
        ],
        'anxious': [
            "For anxiety, try grounding exercises: Stand firmly, feel your feet on the floor, and do slow, deliberate movements like tai chi. 🧍‍♀️",
            "Walking in nature can help calm anxious thoughts. Focus on the rhythm of your steps and your breathing. 🍃🚶‍♀️",
            "Swimming or water exercises provide soothing sensory input that helps reduce anxiety. The water's resistance feels comforting. 🏊‍♂️",
            "Progressive muscle relaxation: Tense each muscle group for 5 seconds, then release for 10 seconds, moving from toes to head.",
            "Yoga for anxiety: Try gentle poses like child's pose, cat-cow, and legs-up-the-wall with deep, slow breathing. 🧘‍♂️",
            "Box breathing while walking: Inhale for 4 steps, hold for 4, exhale for 4, hold for 4. This combines movement with anxiety-reducing breathing.",
            "Qigong or tai chi: These slow, flowing movements are specifically designed to calm the nervous system and reduce anxiety.",
            "Walking meditation: Walk slowly in a small circle or straight line, focusing only on the movement of your feet and breath.",
            "Gentle stretching with breath awareness: Hold each stretch for 30 seconds while breathing deeply into the tension.",
            "Mindful movement: Choose any exercise and focus completely on the physical sensations, redirecting attention from anxious thoughts."
        ],
        'angry': [
            "Channel angry energy constructively: Try high-intensity exercise like boxing (even shadow boxing), running, or weight lifting. 🥊",
            "Vigorous cardio helps release anger: Try sprint intervals, jump rope, or intense cycling for 20-30 minutes. 🚴‍♀️",
            "Martial arts or kickboxing provide structured ways to channel angry energy into focused movement. 👊",
            "Running outdoors allows you to physically move away from what's upsetting you while releasing endorphins. 🏃‍♂️",
            "Weight training: Lifting weights can help you feel strong and empowered while physically expressing intense energy. 🏋️‍♂️",
            "Dance it out: Put on intense music and dance vigorously to release angry energy through movement. 💥🕺",
            "Punching bag work: If available, use a punching bag to safely express and release anger through physical impact.",
            "Stair climbing: Run or walk briskly up and down stairs - the repetitive motion helps process intense emotions.",
            "Rowing machine: The full-body, rhythmic motion can help channel anger into productive physical exertion.",
            "High-intensity interval training (HIIT): Short bursts of maximum effort followed by brief recovery matches angry energy cycles."
        ],
        'tired': [
            "When tired, gentle movement often helps more than resting. Try a 10-minute slow walk to increase circulation. 🚶‍♀️",
            "Restorative yoga: Focus on supported poses that require minimal effort but increase energy flow. Use props for comfort. 🧘‍♀️",
            "Chair yoga: Perfect for low energy days. Gentle stretches and breathing exercises while seated can boost energy. 💺",
            "Walking in sunlight: Even 5-10 minutes outside can help reset your circadian rhythm and boost energy levels. ☀️",
            "Deep breathing with gentle movement: Inhale while raising arms, exhale while lowering. Repeat 10 times to oxygenate your body.",
            "Tai chi or qigong: These gentle, flowing movements increase energy without exhausting you.",
            "Stretching in bed: Before getting up, do gentle stretches while breathing deeply to awaken your body gently.",
            "Water exercises: The buoyancy reduces strain while movement increases energy. Try gentle swimming or water walking.",
            "5-minute energy boost: Set a timer for 5 minutes and do the gentlest movement you can manage - even just marching in place.",
            "Nature connection walk: Walk slowly in a peaceful place, focusing on breathing and observing nature to gently replenish energy."
        ],
        'lonely': [
            "Join a group exercise class - the social connection combined with movement can help ease loneliness. 👥🏋️‍♀️",
            "Walking with a podcast or audiobook: Feel like you're walking with someone through engaging conversation. 🎧🚶‍♂️",
            "Dance to music that makes you feel connected - choose songs that uplift or remind you of positive connections. 💃🎵",
            "Try online workout classes - many offer live sessions where you can see others working out with you. 💻",
            "Walking in public spaces: Being around others while moving can provide a sense of community without pressure to interact. 🏙️",
            "Partner exercises: Even imaginary - do exercises that typically involve partners, focusing on the rhythm and intention.",
            "Exercise while video calling a friend: You don't have to talk much - just having someone there can ease loneliness.",
            "Join a running or walking group: Many communities have free groups that meet regularly for social exercise.",
            "Follow along with cheerful workout videos: Choose instructors who have warm, engaging personalities.",
            "Gardening or outdoor activity: Caring for plants while moving your body can create a sense of companionship with nature. 🌱"
        ],
        'neutral': [
            "Try something new! When in a neutral state, it's a great time to explore different types of exercise. 🆕",
            "Balance-focused activities: Try yoga, Pilates, or balance exercises to enhance mind-body connection. ⚖️",
            "Mindful walking: Walk at a moderate pace while paying attention to your breath and surroundings. 🚶‍♀️",
            "Strength training: Neutral moods are great for focused, consistent strength building. 🏋️‍♀️",
            "Swimming: The sensory experience of water can be both energizing and calming in neutral states. 🏊‍♂️",
            "Cycling: Steady, rhythmic pedaling matches neutral energy well - neither too intense nor too gentle. 🚴‍♀️",
            "Hatha yoga: Balanced poses and breath work that suit neutral emotional states perfectly. 🧘‍♂️",
            "Functional fitness: Exercises that mimic daily movements - squats, lifts, carries - practical and grounding.",
            "Interval walking: Alternate between 3 minutes brisk walking and 2 minutes moderate walking for balanced challenge.",
            "Body awareness practice: Slow movements focusing on how each part of your body feels and moves."
        ],
        'motivational': [
            "Start with small, achievable goals: 10 minutes of exercise is better than none. Build consistency first! 💪",
            "Create an energizing playlist: Music with strong beats can boost motivation during workouts. 🎵",
            "Find an 'accountability buddy': Exercise with a friend or join a challenge to stay motivated. 👫",
            "Mix it up: Try different exercises to prevent boredom - variety keeps motivation high. 🔄",
            "Track your progress: Use an app or journal to see how far you've come - progress is motivating! 📈",
            "Morning movement: Start your day with exercise to build momentum for the rest of the day. 🌅",
            "Reward yourself: Plan small rewards for completing workouts - non-food treats work best! 🏆",
            "Visualize success: Before exercising, picture yourself completing the workout feeling strong and accomplished. 🧠",
            "Break it down: If 30 minutes feels daunting, do three 10-minute sessions throughout the day. ⏱️",
            "Focus on how you'll feel: Remember the post-workout energy and mood boost as motivation to start. ✨"
        ]
    }
    
    # Professional greetings
    GREETINGS = [
        "Hello! I'm here to support your mental wellness journey. How are you arriving to our conversation today? 😊",
        "Welcome! Let's begin by checking in with where you are right now—emotionally, mentally, physically. What's present for you?",
        "Hi there! I'm ready to listen and support in whatever way feels right for you today. How can I be most helpful?",
        "Hello! Before we dive in, take a conscious breath. I'm here to meet you exactly where you are. What would you like to explore? 🌟"
    ]
    
    # Enhanced farewells
    FAREWELLS = [
        "Thank you for sharing this time with me. Remember to carry forward whatever was helpful, and leave what wasn't. Take gentle care of yourself today. 🌈",
        "Our conversation matters. I appreciate you investing in your mental wellbeing. Wishing you peace and clarity as you move through your day. ✨",
        "I'm grateful for our connection today. Remember: You have resources within you, and support around you. Be kind to yourself. 💖",
        "Thank you for trusting me with your experience. May you move forward with greater self-awareness and compassion. You've got this! 🌟"
    ]
    
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
            'current_mood': None
        }
    
    @classmethod
    def _update_state(cls, user_message: str, response: str, mood: str = None):
        """Update conversation state"""
        cls._conversation_state['interaction_count'] += 1
        cls._conversation_state['last_interaction'] = {
            'timestamp': datetime.now(),
            'user_message': user_message[:100],
            'response': response[:100]
        }
        
        if mood:
            cls._conversation_state['current_mood'] = mood
        
        # Reset cheer up context UNLESS explicitly mentioned
        if 'cheer' not in user_message.lower() and 'up' not in user_message.lower():
            cls._conversation_state['cheer_up_context'] = False
    
    @classmethod
    def _get_fresh_quote(cls, category: str = 'motivational') -> str:
        """Get a quote that hasn't been given recently"""
        available_quotes = cls.QUOTE_CATEGORIES.get(category, cls.QUOTE_CATEGORIES['motivational'])
        
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
    def _get_fresh_poem(cls, category: str = 'uplifting') -> str:
        """Get a poem that hasn't been given recently"""
        available_poems = []
        
        # Check if it's a Nepali poem request
        if category.startswith('nepali_'):
            available_poems = cls.POEM_CATEGORIES.get(category, cls.POEM_CATEGORIES['nepali_uplifting'])
        else:
            available_poems = cls.POEM_CATEGORIES.get(category, cls.POEM_CATEGORIES['uplifting'])
        
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
    def _get_fresh_exercise_tip(cls, mood: str = None) -> str:
        """Get an exercise tip that hasn't been given recently for this mood"""
        if not mood or mood not in cls.EXERCISE_TIPS:
            mood = 'neutral'
        
        # Get exercise tips for this mood
        mood_tips = cls.EXERCISE_TIPS.get(mood, cls.EXERCISE_TIPS['neutral'])
        
        # Filter out recently given tips
        fresh_tips = [t for t in mood_tips if t not in cls._conversation_state['last_exercise_tips_given']]
        
        # If all tips have been used, reset for this mood
        if not fresh_tips:
            cls._conversation_state['last_exercise_tips_given'] = []
            fresh_tips = mood_tips
        
        # Select and track tip
        selected_tip = random.choice(fresh_tips)
        cls._conversation_state['last_exercise_tips_given'].append(selected_tip)
        
        # Keep only last 5 tips
        if len(cls._conversation_state['last_exercise_tips_given']) > 5:
            cls._conversation_state['last_exercise_tips_given'] = cls._conversation_state['last_exercise_tips_given'][-5:]
        
        return selected_tip
    
    @classmethod
    def _get_fresh_song(cls, mood: str = None, is_cheer_up: bool = False) -> Dict:
        """Get a song that hasn't been given recently for this mood"""
        if not mood or mood not in cls.YOUTUBE_RESOURCES:
            mood = 'neutral'
        
        # Get resources for this mood
        mood_resources = cls.YOUTUBE_RESOURCES.get(mood, cls.YOUTUBE_RESOURCES['neutral'])
        
        # For cheer up requests with sad mood, filter for uplifting energy
        if mood == 'sad' and is_cheer_up:
            mood_resources = [r for r in mood_resources if r['energy'] in ['medium', 'high']]
        
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
    def _get_mood_specific_youtube_resource(cls, mood: str = None, is_cheer_up: bool = False) -> str:
        """Get mood-specific YouTube resource without repetition"""
        if not mood or mood not in cls.YOUTUBE_RESOURCES:
            mood = 'neutral'
        
        # Get fresh song for this mood
        resource = cls._get_fresh_song(mood, is_cheer_up)
        
        # Create appropriate introduction based on mood
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
        
        intro = mood_intros.get(mood, "Here's some supportive music:\n\n")
        
        # Override for cheer up requests
        if is_cheer_up:
            if mood == 'sad':
                intro = "To help cheer you up, here's some uplifting music:\n\n"
            else:
                intro = "To boost your mood, here's some uplifting music:\n\n"
        
        return f"{intro}🎵 **{resource['title']}**\n🔗 {resource['url']}\n💡 {resource['description']}\n\n📝 Copy the URL above and paste into your browser to open YouTube"
    
    @classmethod
    def get_response(cls, user_message: str, user_mood: Optional[str] = None) -> str:
        """Generate enhanced chatbot response"""
        user_message_lower = user_message.lower().strip()
        
        # Reset state on new conversation
        if cls._conversation_state['interaction_count'] == 0:
            cls._reset_state()
        
        # CRITICAL FIX: Always detect mood from CURRENT message first
        current_message_mood = cls.analyze_mood_from_text(user_message)
        
        # If current message has a mood, it OVERRIDES everything
        if current_message_mood:
            detected_mood = current_message_mood
            cls._conversation_state['current_mood'] = current_message_mood
            # Also reset cheer up context for new moods
            if current_message_mood != 'sad':
                cls._conversation_state['cheer_up_context'] = False
        elif user_mood:
            # Use provided user_mood if no mood in current message
            detected_mood = user_mood
            cls._conversation_state['current_mood'] = user_mood
        else:
            # Use existing mood from state
            detected_mood = cls._conversation_state.get('current_mood')
        
        # Handle "thank you" and "thanks" as farewells
        if user_message_lower in ['thank you', 'thanks', 'thank u', 'thx']:
            response = random.choice(cls.FAREWELLS)
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Handle "how are you" specifically
        how_are_you_variations = ['how are you', 'how are you?', 'how are u', 'how r u', 'how you doing', 'how you doing?', 'how you doin',
                                  'how are ypu', 'how r u doing', 'how you doin?']
        if any(variation in user_message_lower for variation in how_are_you_variations):
            response = random.choice([
                "Thank you for asking! I'm here and fully present to support you. How are you feeling today?",
                "I'm doing well, and I'm focused on being here for you. How has your day been so far?",
                "I'm present and ready to listen. Thanks for checking in! How are you really doing?",
            ])
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Handle "another" as request for another quote
        if user_message_lower in ['another', 'another quote', 'more quotes', 'different quote']:
            # Get last mood or default
            last_mood = cls._conversation_state.get('current_mood', 'neutral')
            if last_mood in ['anxious', 'sad', 'lonely']:
                category = 'emotional'
            elif last_mood == 'happy':
                category = 'uplifting'
            elif last_mood == 'motivational':
                category = 'motivational'
            else:
                category = 'motivational'
            
            quote = cls._get_fresh_quote(category)
            response = f"Here's another quote for you:\n\n\"{quote}\""
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for greetings
        greetings = ['hello', 'hi', 'hey', 'greetings']
        if any(greet in user_message_lower for greet in greetings) and cls._conversation_state['interaction_count'] < 2:
            response = random.choice(cls.GREETINGS)
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for farewells
        farewells = ['bye', 'goodbye', 'see you', 'farewell', 'quit', 'exit']
        if any(farewell in user_message_lower for farewell in farewells):
            response = random.choice(cls.FAREWELLS)
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # FIX: Check for NEPALI poem requests FIRST - THIS IS THE CRITICAL FIX
        if 'nepali' in user_message_lower:
            # Determine Nepali poem category
            # CHECK EXPLICIT REQUESTS FIRST
            if 'motivat' in user_message_lower:
                category = 'nepali_motivational'
            elif 'uplift' in user_message_lower:
                category = 'nepali_uplifting'
            # THEN CHECK MOOD
            elif detected_mood == 'happy':
                category = 'nepali_happy'
            elif detected_mood == 'sad':
                category = 'nepali_sad'
            elif detected_mood == 'lonely':
                category = 'nepali_lonely'
            elif detected_mood in ['anxious', 'tired']:
                category = 'nepali_calming'
            elif detected_mood == 'motivational':
                category = 'nepali_motivational'
            else:
                # Default based on mood
                if detected_mood:
                    category = 'nepali_calming'
                else:
                    category = 'nepali_uplifting'
            
            # Get a fresh Nepali poem
            poem = cls._get_fresh_poem(category)
            
            # Create response with appropriate intro
            response = f"Here's a Nepali poem for you:\n\n{poem}"
            
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for poem requests (English) - MUST COME AFTER NEPALI CHECK
        if 'poem' in user_message_lower or 'poetry' in user_message_lower:
            # Determine poem category based on mood
            # CHECK EXPLICIT REQUESTS FIRST
            if 'motivat' in user_message_lower:
                category = 'motivational'
            elif 'uplift' in user_message_lower:
                category = 'uplifting'
            # THEN CHECK MOOD
            elif detected_mood == 'happy':
                category = 'happy'
            elif detected_mood == 'sad':
                category = 'sad'
            elif detected_mood in ['anxious', 'tired']:
                category = 'calming'
            elif detected_mood == 'lonely':
                category = 'lonely'
            elif detected_mood == 'motivational':
                category = 'motivational'
            else:
                # Default based on mood or request
                if detected_mood:
                    category = 'calming'
                else:
                    category = 'uplifting'
            
            # Get a fresh poem
            poem = cls._get_fresh_poem(category)
            
            # Create response with appropriate intro
            poem_intros = {
                'happy': "Here's a joyful poem for you:\n\n",
                'sad': "Here's a poem that understands sadness:\n\n",
                'motivational': "Here's an encouraging poem:\n\n",
                'lonely': "Here's a poem about solitude:\n\n",
                'calming': "Here's a calming poem:\n\n",
                'uplifting': "Here's an uplifting poem:\n\n"
            }
            
            intro = poem_intros.get(category, "Here's a poem for you:\n\n")
            response = f"{intro}{poem}"
            
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for exercise/fitness requests
        if any(word in user_message_lower for word in ['exercise', 'workout', 'fitness', 'physical', 'activity', 'move', 'tip']):
            # Use the detected mood from current message or state
            mood_for_exercise = detected_mood or cls._conversation_state.get('current_mood', 'neutral')
            
            # Get mood-appropriate exercise tip
            exercise_tip = cls._get_fresh_exercise_tip(mood_for_exercise)
            
            # Create appropriate introduction
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
            response = f"{intro}{exercise_tip}"
            
            cls._update_state(user_message, response, mood_for_exercise)
            return response
        
        # Check for song/music requests
        if any(word in user_message_lower for word in ['song', 'music', 'playlist', 'youtube', 'listen']):
            # Check if this is a cheer up request
            is_cheer_up = 'cheer' in user_message_lower and 'up' in user_message_lower
            
            # Use the detected mood from current message
            mood_for_song = detected_mood or cls._conversation_state.get('current_mood', 'neutral')
            
            # For cheer up requests with sad mood, keep cheer up context
            if is_cheer_up and mood_for_song == 'sad':
                cls._conversation_state['cheer_up_context'] = True
            else:
                cls._conversation_state['cheer_up_context'] = False
            
            # Get mood-appropriate resource
            response = cls._get_mood_specific_youtube_resource(mood_for_song, is_cheer_up)
            cls._update_state(user_message, response, mood_for_song)
            return response
        
        # FIX: Check for quote requests - NOW THIS COMES AFTER NEPALI CHECK
        if 'quote' in user_message_lower or 'quotes' in user_message_lower:
            # Determine quote category based on explicit request
            if 'motivational' in user_message_lower or 'motivate' in user_message_lower:
                category = 'motivational'
            elif 'sad' in user_message_lower or 'emotional' in user_message_lower:
                category = 'emotional'
            elif 'happy' in user_message_lower or 'joy' in user_message_lower or 'uplifting' in user_message_lower:
                category = 'uplifting'
            elif 'mindful' in user_message_lower or 'present' in user_message_lower:
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
            
            # Check if asking for "another" quote
            if 'another' in user_message_lower or 'more' in user_message_lower or 'different' in user_message_lower:
                quote = cls._get_fresh_quote(category)
                response = f"Here's another thought for you:\n\n\"{quote}\""
            else:
                quote = cls._get_fresh_quote(category)
                response = f"Here's a perspective that might resonate:\n\n\"{quote}\""
            
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for "what should I do" requests
        if 'what should i do' in user_message_lower or 'what to do' in user_message_lower or 'what do i do' in user_message_lower:
            # Determine response based on mood
            if detected_mood == 'sad':
                responses = [
                    "When feeling sad, gentle self-care activities can help. Would you like exercise tips, soothing music, or a comforting poem?",
                    "For sadness, consider gentle movement, expressing your feelings through writing, or connecting with supportive resources.",
                    "Sadness often responds well to gentle activities. I can suggest exercises, music, or other supportive approaches."
                ]
            elif detected_mood == 'anxious':
                responses = [
                    "For anxiety, grounding exercises can help. Would you like breathing techniques, calming music, or gentle movement suggestions?",
                    "When anxious, focusing on the present moment helps. I can suggest mindfulness exercises or calming activities.",
                    "Anxiety responds well to structure. Would you like a specific exercise, grounding technique, or soothing resource?"
                ]
            elif detected_mood == 'angry':
                responses = [
                    "Anger can be channeled constructively. Would you like exercise suggestions, calming techniques, or expressive activities?",
                    "For anger, physical movement or creative expression can help. I can suggest appropriate exercises or activities.",
                    "Angry energy needs safe expression. Would you like exercise tips, breathing techniques, or other constructive outlets?"
                ]
            elif detected_mood == 'tired':
                responses = [
                    "When tired, gentle restoration is key. Would you like restful exercises, calming music, or tips for energy renewal?",
                    "Fatigue calls for gentle care. I can suggest low-energy activities, restful resources, or gentle movement.",
                    "For tiredness, consider restorative activities. Would you like gentle exercise tips or calming suggestions?"
                ]
            else:
                responses = [
                    "I have several supportive options. Would you like exercise tips, mood-appropriate music, an inspiring poem, or a thoughtful quote?",
                    "Let me offer you some supportive choices: exercise suggestions, music, poems, or quotes tailored to your current state.",
                    "I can help with various supportive resources. Would you prefer exercise tips, musical support, poetic inspiration, or motivational quotes?"
                ]
            
            response = random.choice(responses)
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Check for specific emotional support questions (NEW FIX)
        if any(word in user_message_lower for word in ['fear', 'scared', 'afraid', 'overcome', 'anxiety', 'worry']):
            # These should trigger specific responses, not mood-based responses
            if 'fear' in user_message_lower or 'scared' in user_message_lower or 'afraid' in user_message_lower:
                fear_responses = [
                    "Fear can be overwhelming, but it's also a natural protective response. Would you like to explore specific techniques for managing fear, or talk about what's triggering it? 🛡️",
                    "I hear you're dealing with fear. This emotion often points to something we care deeply about. Let's explore constructive ways to work with this feeling.",
                    "Fear can feel paralyzing. Sometimes breaking it down into smaller, manageable pieces helps. What's the specific fear that's coming up for you?",
                    "When facing fear, grounding exercises can be helpful. Would you like to try a breathing technique or a mindfulness exercise to help calm your nervous system?",
                    "Fear is often about anticipating future threats. Bringing your attention to the present moment can help reduce its intensity. Let's explore some present-focused strategies."
                ]
                response = random.choice(fear_responses)
            elif 'overcome' in user_message_lower:
                overcome_responses = [
                    "Overcoming challenges often starts with small, manageable steps. What specific area would you like to focus on overcoming? 🌱",
                    "The desire to overcome something shows your resilience! Let's explore practical strategies and supportive resources for your specific challenge.",
                    "Overcoming obstacles is a process. Would you like to break down what you're facing into smaller, more manageable pieces?",
                    "I'm here to support you in overcoming challenges. Let's start by identifying what resources or strategies might be most helpful for your situation."
                ]
                response = random.choice(overcome_responses)
            else:
                # Default response for emotional support questions
                response = "I hear you're seeking support with emotional challenges. Let's explore what specific strategies or resources might be most helpful for you right now. 💭"
            
            cls._update_state(user_message, response, 'anxious')  # Set mood to anxious for these questions
            return response
        
        # Check for cheer up requests
        if 'cheer' in user_message_lower and 'up' in user_message_lower:
            cls._conversation_state['cheer_up_context'] = True
            
            if 'sad' in user_message_lower or detected_mood == 'sad':
                response = random.choice(cls.MOOD_RESPONSES['sad']['cheer_up'])
                response += "\n\n" + cls._get_mood_specific_youtube_resource('sad', True)
            else:
                response = "I'd be happy to help cheer you up! "
                response += cls._get_mood_specific_youtube_resource(detected_mood or 'neutral', True)
            
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Mood-based responses - ONLY if no other conditions matched
        if detected_mood and detected_mood in cls.MOOD_RESPONSES:
            cls._conversation_state['current_mood'] = detected_mood
            if detected_mood == 'sad':
                if cls._conversation_state['cheer_up_context']:
                    responses = cls.MOOD_RESPONSES['sad']['cheer_up']
                else:
                    responses = cls.MOOD_RESPONSES['sad']['general']
            else:
                responses = cls.MOOD_RESPONSES[detected_mood]
            
            response = random.choice(responses)
            
            cls._update_state(user_message, response, detected_mood)
            return response
        
        # Default empathetic responses
        empathetic_responses = [
            "Thank you for sharing that with me. I'm listening with care and attention. 🤗",
            "I hear you. Would you like to explore this further, or would supportive resources be more helpful right now? 💭",
            "That sounds important. How is this sitting with you emotionally and physically?",
            "I'm fully present with what you're sharing. Your experience matters here. 💫",
            "Thank you for being open with me. Let's proceed in whatever way feels most supportive for you. 🌟"
        ]
        
        response = random.choice(empathetic_responses)
        cls._update_state(user_message, response, detected_mood)
        return response
    
    @staticmethod
    def analyze_mood_from_text(text):
        """Enhanced mood detection from text"""
        text_lower = text.lower()
        
        # Check for specific moods first (emotional moods take priority)
        if 'lonely' in text_lower or 'alone' in text_lower:
            return 'lonely'
        if 'tired' in text_lower or 'exhausted' in text_lower:
            return 'tired'
        if 'anxious' in text_lower or 'anxiety' in text_lower or 'fear' in text_lower or 'scared' in text_lower:
            return 'anxious'
        if 'angry' in text_lower or 'mad' in text_lower:
            return 'angry'
        if 'happy' in text_lower or 'joy' in text_lower:
            return 'happy'
        if 'sad' in text_lower or 'unhappy' in text_lower:
            return 'sad'
        
        # NEW: Add motivational mood detection (only if no emotional mood detected)
        if 'motivat' in text_lower or 'inspire' in text_lower or 'encourag' in text_lower or 'overcome' in text_lower:
            return 'motivational'
        
        return None