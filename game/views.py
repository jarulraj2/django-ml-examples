from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import random

# Shared data
COLORS = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange']
EMOJIS = ['😀', '😂', '😍', '😎', '😢', '😡']
WORDS = ['python', 'coding', 'school', 'relax', 'brain', 'memory']
SHAPES = ['Circle', 'Square', 'Triangle']

def hub(request):
    return render(request, 'game/hub.html')

def render_game_partial(request, template_name):
    """
    Helper function to return partial HTML if AJAX request,
    else full render.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(template_name, request=request)
        return HttpResponse(html)
    else:
        return render(request, template_name)

# Game 1: Quick Color Match
def color_match(request):
    return render_game_partial(request, 'game/color_match.html')

@csrf_exempt
def get_color_challenge(request):
    word = random.choice(COLORS)
    font_color = random.choice([c for c in COLORS if c != word])
    return JsonResponse({'word': word, 'font_color': font_color, 'colors': COLORS})

# Game 2: Click Speed Test
def click_speed(request):
    return render_game_partial(request, 'game/click_speed.html')

# Game 3: Reaction Timer
def reaction_timer(request):
    return render_game_partial(request, 'game/reaction_timer.html')

# Game 4: Memory Flip Game
def memory_game(request):
    return render_game_partial(request, 'game/memory.html')

# Game 5: Simple Math Race
def math_race(request):
    return render_game_partial(request, 'game/math_race.html')

@csrf_exempt
def get_math_challenge(request):
    a, b = random.randint(1, 20), random.randint(1, 20)
    return JsonResponse({'question': f"{a} + {b}", 'answer': a + b})

# Game 6: Typing Speed Game
def typing_game(request):
    return render_game_partial(request, 'game/typing_game.html')

# Game 7: Emoji Match Game
def emoji_match(request):
    return render_game_partial(request, 'game/emoji_match.html')

@csrf_exempt
def get_emoji_challenge(request):
    emoji = random.choice(EMOJIS)
    return JsonResponse({'emoji': emoji, 'choices': EMOJIS})

# Game 8: Shape Tap Game
def shape_game(request):
    return render_game_partial(request, 'game/shape_game.html')

@csrf_exempt
def get_shape_challenge(request):
    shape = random.choice(SHAPES)
    return JsonResponse({'shape': shape, 'choices': SHAPES})

# Game 9: Word Scramble
def word_scramble(request):
    return render_game_partial(request, 'game/word_scramble.html')

@csrf_exempt
def get_scrambled_word(request):
    word = random.choice(WORDS)
    scrambled = ''.join(random.sample(word, len(word)))
    return JsonResponse({'word': scrambled, 'answer': word})

# Game 10: Breathe & Relax
def breathe(request):
    return render_game_partial(request, 'game/breathe.html')


####################################################
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import GameSession
import json

@csrf_exempt
def start_game_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        game_name = data.get('game_name', 'unknown')
        user = request.user if request.user.is_authenticated else None

        session = GameSession.objects.create(user=user, game_name=game_name)
        return JsonResponse({'session_id': session.id, 'started_at': session.started_at.isoformat()})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def stop_game_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        duration = data.get('duration_seconds', 0)
        clicks = data.get('clicks', 0)
        errors = data.get('errors', 0)
        score = data.get('score', 0)

        try:
            session = GameSession.objects.get(id=session_id)
            session.stopped_at = now()
            session.duration_seconds = duration
            session.clicks = clicks
            session.errors = errors
            session.score = score
            session.save()
            return JsonResponse({'status': 'success'})
        except GameSession.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

