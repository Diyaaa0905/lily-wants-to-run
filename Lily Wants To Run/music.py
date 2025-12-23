"""
Music and sound effects initialization
"""
import pygame

# Initializing music mixer
pygame.mixer.pre_init(frequency=44100, size=-16, channels=5, buffer=32)
pygame.init()
pygame.mixer.init()

# Initializing game music
intro_sound = pygame.mixer.Sound("assets/music/intro.ogg")
loop_sound = pygame.mixer.Sound("assets/music/intro-loop2.ogg")
gameplay_music = pygame.mixer.Sound("assets/music/gameplay.ogg")
gamewin_sound = pygame.mixer.Sound("assets/music/game-win.ogg")
gameover_sound = pygame.mixer.Sound("assets/music/game-over.ogg")
level_up_sound = pygame.mixer.Sound("assets/music/level-up.mp3")
score_count_sound = pygame.mixer.Sound("assets/music/score-count.mp3")

# Initializing game SFXs
jump_sound = pygame.mixer.Sound("assets/music/jump.ogg")
flower_sound = pygame.mixer.Sound("assets/music/flower-collect.ogg")
countdown_sound = pygame.mixer.Sound("assets/music/countdown.mp3")
button_hover_sound = pygame.mixer.Sound("assets/music/button-hover.mp3")
button_click_sound = pygame.mixer.Sound("assets/music/button-click.ogg")

# Initializing music channels
music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(0.5)

jump_channel = pygame.mixer.Channel(1)
jump_channel.set_volume(0.75)

flower_channel = pygame.mixer.Channel(2)
flower_channel.set_volume(1.0)

button_channel = pygame.mixer.Channel(3)
button_channel.set_volume(1.0)

countdown_channel = pygame.mixer.Channel(4)
countdown_channel.set_volume(1.0)