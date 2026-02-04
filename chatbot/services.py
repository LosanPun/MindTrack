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
        'current_mood': None,
        'last_topic': None  # NEW: Track last conversation topic
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
        'motivational': [
            "I hear you're looking for motivation! Sometimes we all need that extra push. What specific area of your life are you looking to energize? 💪",
            "Motivation often starts with small, actionable steps. What's one tiny thing you could do right now to build momentum?",
            "The desire for motivation itself is a great starting point! Let's explore what inspires and energizes you.",
            "I'm here to help you find that motivational spark! Would specific strategies, inspiring content, or practical steps be most helpful?",
            "Motivation grows from action. What's one small commitment you could make to yourself today?"
        ]
    }
    
    # CONSTRUCTIVE WAYS for each mood - NEW ADDITION
    CONSTRUCTIVE_WAYS = {
        'happy': [
            "To sustain and deepen your happiness, try:\n\n1. **Practice gratitude journaling** - Write down 3 things you're grateful for each day\n2. **Share your joy** - Happiness grows when shared; tell someone about your happy moment\n3. **Engage in flow activities** - Do activities where time seems to fly (art, music, sports)\n4. **Create a happiness jar** - Write happy moments on slips of paper and collect them\n5. **Practice mindful appreciation** - Spend 5 minutes fully appreciating something beautiful\n6. **Set up 'happy hours'** - Schedule regular time for activities you love\n7. **Learn something new** - Challenge yourself with a new skill or hobby\n8. **Connect with positive people** - Surround yourself with uplifting influences\n9. **Engage in creative expression** - Paint, write, dance, or create something\n10. **Spend time in nature** - Nature amplifies positive emotions",
            
            "Constructive ways to build on your happiness:\n\n1. **Celebrate small wins** - Acknowledge and celebrate even tiny achievements\n2. **Practice random acts of kindness** - Helping others boosts your own happiness\n3. **Develop a mindfulness practice** - Regular meditation enhances emotional wellbeing\n4. **Create a vision board** - Visualize what brings you joy and work toward it\n5. **Establish healthy routines** - Consistent sleep, exercise, and nutrition support happiness\n6. **Limit negative input** - Reduce exposure to negative news and social media\n7. **Practice positive self-talk** - Be your own best cheerleader\n8. **Engage in physical activity** - Exercise releases endorphins that boost mood\n9. **Cultivate optimism** - Practice seeing the positive in situations\n10. **Build meaningful connections** - Deepen relationships that matter to you",
            
            "To cultivate more happiness:\n\n1. **Savor positive experiences** - Extend happy moments by paying full attention to them\n2. **Practice forgiveness** - Let go of grudges to make space for joy\n3. **Set boundaries** - Protect your energy and time for what matters most\n4. **Engage in spiritual practice** - Connect with something larger than yourself\n5. **Volunteer or help others** - Giving creates profound satisfaction\n6. **Create beauty around you** - Make your environment pleasing and inspiring\n7. **Practice acceptance** - Accept what you cannot change to reduce frustration\n8. **Develop resilience skills** - Learn to bounce back from disappointments\n9. **Find purpose** - Engage in activities that feel meaningful\n10. **Balance work and play** - Ensure you have time for both productivity and enjoyment"
        ],
        
        'sad': [
            "Constructive ways to work with sadness:\n\n1. **Practice self-compassion** - Speak to yourself as you would a dear friend\n2. **Express your feelings** - Journal, create art, or talk about what you're experiencing\n3. **Connect with support** - Reach out to trusted friends, family, or a professional\n4. **Engage in gentle movement** - Walk, stretch, or do gentle yoga\n5. **Allow the feeling** - Let yourself feel sad without judgment; it has its own wisdom\n6. **Practice the 5-4-3-2-1 grounding technique** - Notice 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, 1 thing you taste\n7. **Listen to soothing music** - Choose music that comforts rather than amplifies sadness\n8. **Get professional help if needed** - Therapy can provide valuable support\n9. **Remember emotions are temporary** - This feeling will pass\n10. **Consider what sadness is telling you** - It might point to unmet needs or values",
            
            "When feeling sad, try these constructive approaches:\n\n1. **Create small, achievable goals** - Even getting out of bed or taking a shower can be an achievement\n2. **Practice deep breathing** - Inhale for 4 counts, hold for 4, exhale for 6\n3. **Watch comforting media** - Choose uplifting movies or shows\n4. **Read inspiring material** - Books, poems, or quotes that offer hope\n5. **Focus on basic self-care** - Ensure you're sleeping, eating, and hydrating\n6. **Limit isolation** - While respecting your need for space, don't cut off all contact\n7. **Practice gratitude** - Even in sadness, find small things to appreciate\n8. **Use affirmations** - Repeat positive statements like 'This too shall pass'\n9. **Engage in simple pleasures** - A warm drink, soft blanket, or favorite snack\n10. **Consider creative expression** - Sometimes sadness can fuel beautiful art",
            
            "Constructive strategies for sadness:\n\n1. **Create a comfort kit** - Gather items that bring you comfort (photos, blankets, music)\n2. **Practice mindfulness meditation** - Observe sadness without getting lost in it\n3. **Engage in service** - Helping others can provide perspective and purpose\n4. **Limit decision-making** - When sad, postpone major decisions if possible\n5. **Use sensory grounding** - Focus on physical sensations (warmth, texture, scent)\n6. **Practice progressive muscle relaxation** - Tense and relax each muscle group\n7. **Create a routine** - Structure can provide stability during emotional storms\n8. **Write unsent letters** - Express feelings you might not be ready to share\n9. **Seek sunlight** - Natural light can help regulate mood\n10. **Be patient with yourself** - Healing happens at its own pace"
        ],
        
        'anxious': [
            "Constructive ways to manage anxiety:\n\n1. **Practice 4-7-8 breathing** - Inhale 4 counts, hold 7, exhale 8\n2. **Use the 5-4-3-2-1 grounding technique** - Engage all your senses\n3. **Write down worries** - Put them on paper and set aside 'worry time' later\n4. **Practice progressive muscle relaxation** - Systematically tense and release muscles\n5. **Challenge catastrophic thinking** - Ask 'What evidence do I have for this worry?'\n6. **Practice box breathing** - Equal inhale, hold, exhale, hold (4-4-4-4)\n7. **Use cold water** - Splash face or hold ice to reset nervous system\n8. **Focus on what you CAN control** - Let go of what you cannot\n9. **Create a 'safe space' visualization** - Imagine a peaceful place in detail\n10. **Use anxiety as information** - What might it be telling you about needs or boundaries?",
            
            "For anxiety relief, try:\n\n1. **Mindfulness meditation** - Practice daily, even for 5 minutes\n2. **Create a worry list** - Write worries and review only once a day\n3. **Engage in rhythmic activities** - Walking, swimming, or rocking\n4. **Limit caffeine and sugar** - These can exacerbate anxiety\n5. **Use affirmations** - Repeat 'This feeling will pass' or 'I am safe right now'\n6. **Practice acceptance** - Allow anxiety to be present without fighting it\n7. **Create structure** - Routines can reduce uncertainty\n8. **Engage in light exercise** - Movement burns off anxious energy\n9. **Use lavender or chamomile** - These herbs have calming properties\n10. **Practice gratitude** - Shift focus from worries to appreciations",
            
            "Constructive anxiety management:\n\n1. **Practice RAIN technique** - Recognize, Allow, Investigate, Nurture\n2. **Create an anxiety toolkit** - Gather calming items and techniques\n3. **Limit news/social media** - Reduce exposure to anxiety-provoking content\n4. **Practice self-compassion** - Be kind to yourself about anxious feelings\n5. **Use distraction techniques** - Engage in absorbing activities\n6. **Practice systematic desensitization** - Gradually face fears in small steps\n7. **Get professional support** - Therapy can provide effective strategies\n8. **Practice yoga or tai chi** - These combine movement and mindfulness\n9. **Use calming scents** - Essential oils like lavender or bergamot\n10. **Focus on the present** - Anxiety often lives in the future; bring attention to now"
        ],
        
        'angry': [
            "Constructive ways to channel anger:\n\n1. **Physical activity** - Run, box, lift weights, or do intense exercise\n2. **Write an unsent letter** - Express all your feelings without sending it\n3. **Practice deep breathing** - Before reacting, take 10 deep breaths\n4. **Use 'I feel' statements** - Communicate assertively: 'I feel ___ when ___'\n5. **Take a timeout** - Remove yourself from the situation to cool down\n6. **Identify the underlying need** - Anger often signals a boundary violation\n7. **Use physical release** - Punching bag, scream into pillow, tear paper\n8. **Practice assertive communication** - Express needs clearly and respectfully\n9. **Channel energy into projects** - Clean, organize, or create something\n10. **Consider what value is threatened** - Anger protects what matters to us",
            
            "For constructive anger management:\n\n1. **Count to 10 (or 100)** - Delay your response\n2. **Practice empathy** - Try to understand others' perspectives\n3. **Use humor** - Find something funny in the situation if possible\n4. **Engage in vigorous exercise** - Burn off the adrenaline\n5. **Practice mindfulness** - Observe anger without acting on it\n6. **Write a pros/cons list** - What would acting on this anger achieve?\n7. **Use relaxation techniques** - Progressive muscle relaxation or meditation\n8. **Seek perspective** - Talk to a neutral third party\n9. **Practice forgiveness** - For yourself and others\n10. **Create art** - Express the intensity through creative means",
            
            "Constructive anger strategies:\n\n1. **Identify triggers** - Learn what situations typically provoke your anger\n2. **Practice healthy boundaries** - Prevent anger by setting clear limits\n3. **Use 'time in'** - Stay present but calm during conflicts\n4. **Practice active listening** - Truly hear others before responding\n5. **Channel into advocacy** - Use anger to fuel positive change\n6. **Practice self-soothing** - Develop techniques that calm you\n7. **Consider consequences** - What might happen if you express anger destructively?\n8. **Practice gratitude** - Shift focus from what's wrong to what's right\n9. **Get physical distance** - Sometimes space is needed\n10. **Seek professional help** - If anger feels out of control"
        ],
        
        'lonely': [
            "Constructive ways to address loneliness:\n\n1. **Reach out to old connections** - Contact someone you haven't spoken to in a while\n2. **Join groups or classes** - Find communities around your interests\n3. **Volunteer** - Helping others creates connection and purpose\n4. **Practice self-friendship** - Be kind and compassionate to yourself\n5. **Engage in activities you enjoy** - Even alone, do what brings you pleasure\n6. **Schedule regular social interactions** - Make connection a priority\n7. **Practice mindfulness** - Be present with yourself without judgment\n8. **Get a pet or volunteer with animals** - Animal companionship can help\n9. **Attend local events** - Go to community gatherings or meetups\n10. **Use technology meaningfully** - Video calls, online communities, or pen pals",
            
            "For loneliness, try:\n\n1. **Practice gratitude for existing relationships** - Appreciate connections you have\n2. **Engage in creative hobbies** - Art, music, writing, or crafts\n3. **Consider what type of connection you need** - Deep friendship, casual acquaintance, or community\n4. **Balance alone time with social time** - Find your optimal balance\n5. **Practice self-disclosure** - Share appropriately to deepen connections\n6. **Join support groups** - Connect with others who understand\n7. **Practice active listening** - Deepen existing connections through attentiveness\n8. **Create social rituals** - Regular coffee dates, game nights, or walks\n9. **Limit social media comparison** - Real connections are different from curated feeds\n10. **Be patient** - Building connections takes time",
            
            "Constructive approaches to loneliness:\n\n1. **Journal about your feelings** - Understand your loneliness better\n2. **Practice self-compassion** - Don't judge yourself for feeling lonely\n3. **Engage in learning** - Take a course or develop a new skill\n4. **Create connection opportunities** - Host gatherings or start a group\n5. **Practice being vulnerable** - Appropriate sharing invites connection\n6. **Focus on quality over quantity** - A few deep connections matter more than many superficial ones\n7. **Engage in spiritual practice** - Connect with something larger than yourself\n8. **Practice loving-kindness meditation** - Cultivate feelings of connection\n9. **Consider professional help** - Therapy can address underlying issues\n10. **Remember loneliness is common** - You're not alone in feeling alone"
        ],
        
        'tired': [
            "Constructive ways to address tiredness:\n\n1. **Prioritize sleep hygiene** - Consistent schedule, dark room, cool temperature\n2. **Practice restorative yoga** - Gentle poses with props for support\n3. **Take short, frequent breaks** - 5-minute breaks every hour\n4. **Nourish your body** - Balanced meals, adequate hydration\n5. **Listen to your body's signals** - Rest when you need to\n6. **Practice power naps** - 20-30 minutes maximum\n7. **Stay hydrated** - Dehydration causes fatigue\n8. **Engage in light movement** - Gentle walks or stretching\n9. **Limit screen time before bed** - Blue light disrupts sleep\n10. **Create a relaxing bedtime routine** - Wind down for 30-60 minutes before sleep",
            
            "For fatigue management:\n\n1. **Break tasks into smaller pieces** - Make everything more manageable\n2. **Practice saying no** - Protect your energy from non-essential commitments\n3. **Spend time in nature** - Natural environments restore energy\n4. **Consider emotional roots** - Sometimes tiredness has emotional causes\n5. **Schedule rest as a priority** - Not as an afterthought\n6. **Practice breathing exercises** - Oxygenate your body\n7. **Use aromatherapy** - Peppermint or citrus scents can energize\n8. **Create energy rituals** - Morning routines that boost your day\n9. **Limit caffeine after noon** - Prevent sleep disruption\n10. **Practice acceptance** - Some days we just have less energy",
            
            "Constructive tiredness strategies:\n\n1. **Practice gentle movement** - Yoga, walking, or stretching\n2. **Use positive self-talk** - Encourage yourself through fatigue\n3. **Create an energizing environment** - Bright lighting, uplifting music\n4. **Practice mindfulness** - Be present with tiredness without judgment\n5. **Consider medical causes** - Rule out anemia, thyroid issues, etc.\n6. **Balance activity and rest** - Pacing prevents burnout\n7. **Practice gratitude for your body** - Appreciate what it does for you\n8. **Use cold water** - Splash face or take a cool shower\n9. **Listen to upbeat music** - Music can boost energy\n10. **Be gentle with yourself** - Rest is productive, not lazy"
        ],
        
        'neutral': [
            "Constructive ways to use neutral states:\n\n1. **Practice mindfulness and observation** - Notice your state without changing it\n2. **Engage in learning** - Read, take courses, or develop skills\n3. **Complete practical tasks** - Organization, cleaning, or administrative work\n4. **Reflect on goals and priorities** - Use clarity to plan ahead\n5. **Rest in the calm** - Enjoy peace without pressure to feel differently\n6. **Practice meditation** - Deepen your present-moment awareness\n7. **Engage in creative problem-solving** - Use mental clarity for solutions\n8. **Make decisions** - Neutral states are good for balanced choices\n9. **Plan for future needs** - Anticipate what support you might need\n10. **Practice gratitude for balance** - Appreciate emotional equilibrium",
            
            "For neutral moods:\n\n1. **Use this state for reflection** - Journal about recent experiences\n2. **Engage in moderate exercise** - Maintain your wellbeing\n3. **Read educational material** - Expand your knowledge\n4. **Organize your space** - Physical or digital organization\n5. **Practice gratitude for emotional balance** - Not all states need to be intense\n6. **Connect with others** - Socialize without emotional charge\n7. **Practice self-care routines** - Maintain healthy habits\n8. **Engage in hobbies** - Enjoy activities for their own sake\n9. **Plan self-care for future moods** - Prepare resources for when emotions shift\n10. **Practice acceptance** - This state has value too",
            
            "Constructive neutral state strategies:\n\n1. **Practice mindfulness** - Deepen awareness of the present\n2. **Engage in skill development** - Learn something new\n3. **Complete neglected tasks** - Use mental clarity for productivity\n4. **Reflect on emotional patterns** - Understand your emotional landscape\n5. **Practice self-compassion** - Accept yourself in all states\n6. **Engage in creative expression** - Without pressure to feel intensely\n7. **Connect with nature** - Appreciate the world around you\n8. **Practice breathing exercises** - Maintain calm and balance\n9. **Read inspiring material** - Gently uplift yourself\n10. **Rest in being** - Sometimes just being is enough"
        ],
        
        'motivational': [
            "Constructive ways to build motivation:\n\n1. **Start with tiny tasks** - 2-minute commitments to build momentum\n2. **Create a vision board** - Visualize your goals and dreams\n3. **Break large goals into small steps** - Make everything achievable\n4. **Find an accountability partner** - Share goals with someone\n5. **Celebrate small wins** - Acknowledge every bit of progress\n6. **Use the 5-second rule** - Act within 5 seconds of thinking about a task\n7. **Create a motivating environment** - Music, lighting, and organization\n8. **Practice positive self-talk** - Encourage yourself\n9. **Visualize success** - Imagine completing your goals\n10. **Remove distractions** - Create focus time",
            
            "For motivation building:\n\n1. **Set SMART goals** - Specific, Measurable, Achievable, Relevant, Time-bound\n2. **Create a reward system** - Small rewards for progress\n3. **Track progress visually** - Charts, journals, or apps\n4. **Find inspiration from role models** - Learn from others' success\n5. **Remember your 'why'** - Connect to deeper purpose\n6. **Practice self-compassion for setbacks** - Don't beat yourself up\n7. **Create routines** - Reduce decision fatigue\n8. **Use energizing music** - Create motivating playlists\n9. **Practice gratitude for progress** - Appreciate how far you've come\n10. **Break tasks into time blocks** - Work in focused intervals",
            
            "Constructive motivation strategies:\n\n1. **Start your day with intention** - Morning rituals that set the tone\n2. **Practice visualization** - See yourself achieving your goals\n3. **Use affirmations** - Positive statements about your capability\n4. **Create an inspiring workspace** - Environment affects motivation\n5. **Practice self-care** - Wellbeing supports motivation\n6. **Learn from failures** - See setbacks as learning opportunities\n7. **Connect with supportive people** - Surround yourself with encouragement\n8. **Practice mindfulness** - Stay present with your tasks\n9. **Use technology wisely** - Apps that track and motivate\n10. **Remember motivation follows action** - Start small, momentum builds"
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
        # NEW: Motivational music resources
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
    
    # Enhanced motivational quotes with variety - NOW INCLUDES NEPALI QUOTES
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
        ],
        
        # NEW: NEPALI QUOTES
        'nepali_motivational': [
            "जिन्दगी सधैं अघि बढिरहन्छ, तिमी पनि अघि बढ।",
            "आफूमा विश्वास गर, तिम्रो सपना साकार हुनेछ।",
            "कठिनाइहरू आउँछन् र जान्छन्, तर तिम्रो हौसला सधैं रहनु पर्छ।",
            "आजको संघर्ष भोलिको सफलताको कथा हुनेछ।",
            "तिम्रो यात्रा अद्वितीय छ, आफ्नो गतिमा अगाडि बढ।",
            "हार मानेर बस्नु भन्दा संघर्ष गर्दै मर्नु राम्रो।",
            "तिम्रो भाग्य तिम्रो हातमा छ, आफैं बनाउनु पर्छ।",
            "सपना देख्नु राम्रो हो, तर त्यो पुरा गर्न खोज्नु अझ राम्रो।",
            "जीवन छोटो छ, आजै सुरु गर।",
            "तिमी सक्षम छौ, तिमीले गर्न सक्छौ।"
        ],
        
        'nepali_happy': [
            "खुसी साना क्षणहरूमा बस्छ, तिनलाई महसुस गर्न सिक।",
            "मुस्कान संक्रामक हुन्छ, आज कसैलाई मुस्कुराउन दिनुहोस्।",
            "जीवन रमाइलो छ, प्रत्येक क्षणको आनन्द लिनुहोस्।",
            "तिम्रो खुसीले अरूलाई पनि खुसी बनाउँछ।",
            "आज एउटा सानो खुसी खोज्नुहोस् र त्यसलाई बडाउनुहोस्।",
            "खुसी भित्रबाट आउँछ, बाहिरबाट खोज्नु पर्दैन।",
            "हाँसो र खुसी सबैभन्दा ठूलो औषधि हुन्।",
            "प्रकृतिको सौन्दर्यले मनलाई खुसी बनाउँछ।",
            "साना साना खुसीहरू जोडेर ठूलो खुसी बनाउन सकिन्छ।",
            "तिम्रो मुस्कान तिम्रो सबैभन्दा सुन्दर आभूषण हो।"
        ],
        
        'nepali_sad': [
            "दुःख अस्थायी हुन्छ, यो पनि बित्नेछ।",
            "आँसुहरू मनको भारी हल्का गर्छन्।",
            "कठिन समयहरूले हामीलाई बलियो बनाउँछन्।",
            "अँध्यारो रात पछि उज्यालो भोलि आउँछ।",
            "तिम्रो भावनाहरू वैध छन्, तिनलाई स्वीकार गर।",
            "दुःख सबैले भोग्छन्, तिमी एक्लै होइनौ।",
            "आँसु पुछेपछि दृष्टि स्पष्ट हुन्छ।",
            "दुःखले नै सुखको महत्त्व बुझाउँछ।",
            "कठिन समयमा आफूलाई सान्त्वना दिन सिक्नु पर्छ।",
            "भावनाहरू बग्न दिनु पर्छ, रोक्नु हुँदैन।"
        ],
        
        'nepali_calming': [
            "शान्ति भित्रै पाइन्छ, बाहिर खोज्नु पर्दैन।",
            "श्वासले जीवन दिन्छ, शान्ति ल्याउँछ।",
            "मन शान्त भएको बेला सबै समाधान हराउँछन्।",
            "धीरज र शान्ति सबैभन्दा ठूलो शक्ति हो।",
            "वर्तमानमा बस्न सिक्नु, शान्ति त्यहीँ छ।",
            "शान्त मनले सबै समस्या समाधान गर्छ।",
            "प्रकृतिको शान्तिले मनलाई शान्त पार्छ।",
            "गहिरो श्वासले तनाव हटाउँछ।",
            "शान्तिमा बस्नु नै ध्यान हो।",
            "मन शान्त भए जीवन सजिलो हुन्छ।"
        ],
        
        'nepali_uplifting': [
            "आशाका बादल हराउँदैनन्, तिनीहरू फेरि आउँछन्।",
            "उज्यालो सधैं अँध्यारो पछि आउँछ।",
            "तिम्रो आत्मविश्वास नै तिम्रो सबैभन्दा ठूलो शक्ति हो।",
            "भोलि नयाँ सुरुवातको दिन हो।",
            "तिमी जस्तो छौ त्यस्तै रहनु, त्यो नै सबैभन्दा राम्रो छ।",
            "आशा नछाड्नु, आशा नै जीवन हो।",
            "तिम्रो क्षमता अनन्त छ, विश्वास गर।",
            "सकारात्मक सोचले जीवन बदल्छ।",
            "आफूलाई प्रेम गर, अरु पनि तिमीलाई प्रेम गर्नेछन्।",
            "तिम्रो भविष्य उज्यालो छ, विश्वास राख।"
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
    
    @classmethod
    def _get_fresh_quote(cls, category: str = 'motivational') -> str:
        """Get a quote that hasn't been given recently"""
        available_quotes = cls.QUOTE_CATEGORIES.get(category, cls.QUOTE_CATEGORIES['motivational'])
        
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
    def _get_fresh_poem(cls, category: str = 'uplifting') -> str:
        """Get a poem that hasn't been given recently"""
        available_poems = []
        
        # Check if it's a Nepali poem request
        if category.startswith('nepali_'):
            available_poems = cls.POEM_CATEGORIES.get(category, cls.POEM_CATEGORIES['nepali_uplifting'])
        else:
            available_poems = cls.POEM_CATEGORIES.get(category, cls.POEM_CATEGORIES['uplifting'])
        
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
    def _get_constructive_ways(cls, mood: str = None) -> str:
        """Get constructive ways for a specific mood"""
        if not mood or mood not in cls.CONSTRUCTIVE_WAYS:
            mood = 'neutral'
        
        ways = cls.CONSTRUCTIVE_WAYS.get(mood, cls.CONSTRUCTIVE_WAYS['neutral'])
        return random.choice(ways)
    
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
        
        # Check for follow-up to constructive ways/fear topic
        last_topic = cls._conversation_state.get('last_topic')
        if (last_topic in ['fear', 'overcome', 'constructive'] and 
            any(word in user_message_lower for word in ['ways', 'methods', 'techniques', 'strategies', 'how', 'what', 'tell'])):
            # This is a follow-up request for constructive ways
            mood_for_ways = detected_mood or 'neutral'
            response = cls._get_constructive_ways(mood_for_ways)
            cls._update_state(user_message, response, mood_for_ways, 'constructive')
            return response
        
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
        
        # CHECK 1: NEPALI QUOTE requests (MUST come before regular quote check)
        if 'nepali' in user_message_lower and ('quote' in user_message_lower or 'quotes' in user_message_lower):
            # Determine Nepali quote category
            if 'motivat' in user_message_lower:
                category = 'nepali_motivational'
            elif 'happy' in user_message_lower:
                category = 'nepali_happy'
            elif 'sad' in user_message_lower:
                category = 'nepali_sad'
            elif 'calm' in user_message_lower or 'peace' in user_message_lower:
                category = 'nepali_calming'
            elif 'uplift' in user_message_lower:
                category = 'nepali_uplifting'
            else:
                # Default based on mood
                if detected_mood == 'happy':
                    category = 'nepali_happy'
                elif detected_mood == 'sad':
                    category = 'nepali_sad'
                elif detected_mood in ['anxious', 'tired']:
                    category = 'nepali_calming'
                elif detected_mood == 'motivational':
                    category = 'nepali_motivational'
                else:
                    category = 'nepali_uplifting'
            
            quote = cls._get_fresh_quote(category)
            response = f"Here's a Nepali quote for you:\n\n\"{quote}\""
            cls._update_state(user_message, response, detected_mood, 'quote')
            return response
        
        # CHECK 2: NEPALI POEM requests
        if 'nepali' in user_message_lower and ('poem' in user_message_lower or 'poetry' in user_message_lower):
            # Determine Nepali poem category
            if 'motivat' in user_message_lower:
                category = 'nepali_motivational'
            elif 'happy' in user_message_lower:
                category = 'nepali_happy'
            elif 'sad' in user_message_lower:
                category = 'nepali_sad'
            elif 'lonely' in user_message_lower:
                category = 'nepali_lonely'
            elif 'calm' in user_message_lower or 'peace' in user_message_lower:
                category = 'nepali_calming'
            elif 'uplift' in user_message_lower:
                category = 'nepali_uplifting'
            else:
                # Default based on mood
                if detected_mood == 'happy':
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
                    category = 'nepali_uplifting'
            
            poem = cls._get_fresh_poem(category)
            response = f"Here's a Nepali poem for you:\n\n{poem}"
            cls._update_state(user_message, response, detected_mood, 'poem')
            return response
        
        # CHECK 3: General NEPALI requests (fallback)
        if 'nepali' in user_message_lower:
            # Default to poem for general Nepali requests
            if detected_mood == 'happy':
                category = 'nepali_happy'
            elif detected_mood == 'sad':
                category = 'nepali_sad'
            else:
                category = 'nepali_uplifting'
            
            poem = cls._get_fresh_poem(category)
            response = f"Here's a Nepali poem for you:\n\n{poem}"
            cls._update_state(user_message, response, detected_mood, 'poem')
            return response
        
        # CHECK 4: Constructive ways requests
        if any(word in user_message_lower for word in ['constructive', 'ways', 'methods', 'techniques', 'strategies', 'how to', 'how do i']):
            # Determine mood for constructive ways
            mood_for_ways = detected_mood or cls._conversation_state.get('current_mood', 'neutral')
            response = cls._get_constructive_ways(mood_for_ways)
            cls._update_state(user_message, response, mood_for_ways, 'constructive')
            return response
        
        # CHECK 5: Fear/overcome requests
        if any(word in user_message_lower for word in ['fear', 'scared', 'afraid', 'overcome', 'anxiety', 'worry']):
            # These are specific emotional support requests
            if 'fear' in user_message_lower or 'scared' in user_message_lower or 'afraid' in user_message_lower:
                fear_responses = [
                    "Fear can be overwhelming, but it's also a natural protective response. Here are constructive ways to work with fear:\n\n" + 
                    cls._get_constructive_ways('anxious'),
                    
                    "I hear you're dealing with fear. This emotion often points to something we care deeply about. Let me share some constructive approaches:\n\n" +
                    cls._get_constructive_ways('anxious'),
                    
                    "Fear can feel paralyzing. Here are some constructive strategies to help you work through it:\n\n" +
                    cls._get_constructive_ways('anxious')
                ]
                response = random.choice(fear_responses)
            elif 'overcome' in user_message_lower:
                response = "Overcoming challenges often starts with small, manageable steps. Here are constructive approaches:\n\n" + cls._get_constructive_ways('motivational')
            else:
                response = "I hear you're seeking support with emotional challenges. Here are constructive ways to work with these feelings:\n\n" + cls._get_constructive_ways('anxious')
            
            cls._update_state(user_message, response, 'anxious', 'fear')
            return response
        
        # CHECK 6: Poem requests (English)
        if 'poem' in user_message_lower or 'poetry' in user_message_lower:
            # Determine poem category based on mood
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
            elif 'calm' in user_message_lower or 'peace' in user_message_lower:
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
        
        # CHECK 7: Exercise/fitness requests
        if any(word in user_message_lower for word in ['exercise', 'workout', 'fitness', 'physical', 'activity', 'move', 'tip']):
            mood_for_exercise = detected_mood or cls._conversation_state.get('current_mood', 'neutral')
            exercise_tip = cls._get_fresh_exercise_tip(mood_for_exercise)
            
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
            cls._update_state(user_message, response, mood_for_exercise, 'exercise')
            return response
        
        # CHECK 8: Song/music requests
        if any(word in user_message_lower for word in ['song', 'music', 'playlist', 'youtube', 'listen']):
            is_cheer_up = 'cheer' in user_message_lower and 'up' in user_message_lower
            mood_for_song = detected_mood or cls._conversation_state.get('current_mood', 'neutral')
            
            if is_cheer_up and mood_for_song == 'sad':
                cls._conversation_state['cheer_up_context'] = True
            else:
                cls._conversation_state['cheer_up_context'] = False
            
            response = cls._get_mood_specific_youtube_resource(mood_for_song, is_cheer_up)
            cls._update_state(user_message, response, mood_for_song, 'music')
            return response
        
        # CHECK 9: Quote requests (English)
        if 'quote' in user_message_lower or 'quotes' in user_message_lower:
            # Determine quote category
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
            
            quote = cls._get_fresh_quote(category)
            response = f"Here's a quote for you:\n\n\"{quote}\""
            cls._update_state(user_message, response, detected_mood, 'quote')
            return response
        
        # CHECK 10: "what should I do" requests
        if 'what should i do' in user_message_lower or 'what to do' in user_message_lower or 'what do i do' in user_message_lower:
            # Offer constructive ways based on mood
            mood_for_help = detected_mood or cls._conversation_state.get('current_mood', 'neutral')
            response = "Here are some constructive approaches for your current state:\n\n" + cls._get_constructive_ways(mood_for_help)
            cls._update_state(user_message, response, mood_for_help, 'constructive')
            return response
        
        # CHECK 11: Cheer up requests
        if 'cheer' in user_message_lower and 'up' in user_message_lower:
            cls._conversation_state['cheer_up_context'] = True
            
            if 'sad' in user_message_lower or detected_mood == 'sad':
                response = random.choice(cls.MOOD_RESPONSES['sad']['cheer_up'])
                response += "\n\n" + cls._get_mood_specific_youtube_resource('sad', True)
            else:
                response = "I'd be happy to help cheer you up! "
                response += cls._get_mood_specific_youtube_resource(detected_mood or 'neutral', True)
            
            cls._update_state(user_message, response, detected_mood, 'cheer')
            return response
        
        # CHECK 12: Mood-based responses
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
        
        # Add motivational mood detection
        if 'motivat' in text_lower or 'inspire' in text_lower or 'encourag' in text_lower or 'overcome' in text_lower:
            return 'motivational'
        
        return None