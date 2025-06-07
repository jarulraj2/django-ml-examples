from django.urls import path
from . import views

app_name = 'game'  # Important for namespacing in templates

urlpatterns = [
    path('', views.hub, name='hub'),

    # Game 1: Quick Color Match
    path('color-match/', views.color_match, name='color_match'),
    path('get_color_challenge/', views.get_color_challenge, name='get_color_challenge'),

    # Game 2: Click Speed Test
    path('click-speed/', views.click_speed, name='click_speed'),

    # Game 3: Reaction Timer
    path('reaction-timer/', views.reaction_timer, name='reaction_timer'),

    # Game 4: Memory Flip Game
    path('memory/', views.memory_game, name='memory_game'),

    # Game 5: Simple Math Race
    path('math-race/', views.math_race, name='math_race'),
    path('get_math_challenge/', views.get_math_challenge, name='get_math_challenge'),

    # Game 6: Typing Speed Game
    path('typing/', views.typing_game, name='typing_game'),

    # Game 7: Emoji Match Game
    path('emoji-match/', views.emoji_match, name='emoji_match'),
    path('get_emoji_challenge/', views.get_emoji_challenge, name='get_emoji_challenge'),

    # Game 8: Shape Tap Game
    path('shape-tap/', views.shape_game, name='shape_game'),
    path('get_shape_challenge/', views.get_shape_challenge, name='get_shape_challenge'),

    # Game 9: Word Scramble
    path('word-scramble/', views.word_scramble, name='word_scramble'),
    path('get_scrambled_word/', views.get_scrambled_word, name='get_scrambled_word'),

    # Game 10: Breathe & Relax
    path('breathe/', views.breathe, name='breathe'),
    

    path('start-session/', views.start_game_session, name='start_game_session'),
    path('stop-session/', views.stop_game_session, name='stop_game_session'),
]
