import os
import importlib
import time 
import pygame
from sys import exit

#FEATURES TO BE ADDED:
#board design
#pause screen, add: how to play, volume(drop-down: bg music, sfx), restart
#level complete: sparkles, sparkly flower beside 'flowers collected: ...' (if new record of flowers collected: blinking 'BEST!')
#start screen: how to play menu, volume(drop-down: bg music, sfx), made by, version
#move 'tutorial' to how-to-play
#game start: huge shiny "Lily Wants to Run" (big,left-enter->big,center-stay-> big, right-exit->small, right-enter-> small, center-stay), all other options pop up (total takes: 4sec)
#start game clicked: intro loop stops, 'portal enter whoosh sfx' + portal enter aniimation, game music start
    #music tranistion :((( <------- NOT NEEDED ANYMORE!! :D
#background design (YT: watch-later list!!)
#save-load file system

pygame.mixer.pre_init(frequency=44100, size=-16, channels=5, buffer=32)
pygame.init()
pygame.mixer.init() #For music

#Screen Setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lily Wants To Run") #Title
clock = pygame.time.Clock() #FPS of game

#Button Class
class Button:
    def __init__(self, image, image_pressed, alpha, text, x, y):
        self.image_original = image.copy()
        self.image = image.copy()
        self.image_pressed = image_pressed.copy()
        self.alpha = alpha

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False
        self.was_pressed = False
        self.was_hovered = False

        self.original_width = image.get_width()
        self.original_height = image.get_height()

        self.font_size = 25.0 
        self.original_font_size = 25.0
        self.final_font_size = self.original_font_size * 0.8
        self.text = text
        
    def draw(self):
        screen.blit(self.image, self.rect)

        if self.clicked:
            text_color = "White"
        else:
            text_color = "Black"

        font = pygame.font.Font("assets/font/Minecraft.ttf", int(self.font_size))
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)
    
    def is_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def update_alpha(self):
        target_alpha = 255 if self.is_hover() else 125

        if self.alpha < target_alpha:
            self.alpha = min(self.alpha + 10, target_alpha)
        elif self.alpha > target_alpha:
            self.alpha = max(self.alpha - 10, target_alpha)
        self.image.set_alpha(self.alpha)

    def animate_in(self, final_width, final_height):
        if self.is_hover():
            width = self.image.get_width()
            height = self.image.get_height()
            center = self.rect.center

            if width > final_width:
                width = max(width - self.original_width*0.2//10, final_width)
            if height > final_height:
                height = max(height - self.original_height*0.2//10, final_height)

            current_scale = width / self.original_width
            final_font = self.original_font_size * current_scale
            if self.font_size > final_font:
                self.font_size = max(self.font_size - 0.8, final_font)

            if self.clicked:
                source_img = self.image_pressed
            else:
                source_img = self.image_original

            self.image = pygame.transform.smoothscale(source_img, (width, height))
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=center)

    def animate_out(self, final_width, final_height):
        if not self.is_hover():
            width = self.image.get_width()
            height = self.image.get_height()
            center = self.rect.center

            if width < final_width:
                width = min(width + self.original_width*0.2//10, final_width)
            if height < final_height:
                height = min(height + self.original_height*0.2//10, final_height)

            current_scale = width / self.original_width
            final_font = self.original_font_size * current_scale
            if self.font_size < final_font:
                self.font_size = min(self.font_size + 0.8, final_font)

            if self.clicked:
                source_img = self.image_pressed
            else:
                source_img = self.image_original

            self.image = pygame.transform.smoothscale(source_img, (width, height))
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=center)

    def animate(self):
        if self.is_hover():
            self.animate_in(self.original_width*0.8, self.original_height*0.8)
            if not self.was_hovered:
                button_channel.play(button_hover_sound)
        else:
            self.animate_out(self.original_width, self.original_height)
        
        #Update hover state for next frame
        self.was_hovered = self.is_hover()

        self.image.set_alpha(self.alpha)
        self.draw()

    def is_clicked(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        #Check if mouse is over button & pressed
        if self.is_hover() and mouse_pressed:
            self.clicked = True
            self.was_pressed = True

        #Check if button was pressed & now mouse is released
        if self.was_pressed and not mouse_pressed:
            self.was_pressed = False
            self.clicked = False
            #Only trigger if mouse is still hovering over button when released
            if self.is_hover():
                button_channel.play(button_click_sound)
                return True
        
        #Reset clicked state if mouse is not pressed
        if not mouse_pressed:
            self.clicked = False
            
        return False
    
    def reset(self):
        self.image = pygame.transform.scale(self.image_original, (self.original_width, self.original_height))
        self.font_size = self.original_font_size

#Buttons
button_img = pygame.transform.scale(pygame.image.load("assets/buttons/button.png").convert_alpha(), (150,50))
button_click_img = pygame.transform.scale(pygame.image.load("assets/buttons/button_press.png").convert_alpha(), (150,50))
pause_button_img = pygame.transform.scale(pygame.image.load("assets/buttons/pause_button.png").convert_alpha(), (50,50))
pause_button_click_img = pygame.transform.scale(pygame.image.load("assets/buttons/pause_button_press.png").convert_alpha(), (50,50))

start_button = Button(button_img, button_click_img, 255, "START", WIDTH//2 - button_img.get_width()//2, 275)
exit_button = Button(button_img, button_click_img, 255, "EXIT", WIDTH//2 - button_img.get_width()//2, (HEIGHT-150))
back_button = Button(button_img, button_click_img, 255, "HOME", WIDTH//2 - 200+10, 100+20+40+40+30)
next_button = Button(button_img, button_click_img, 255, "NEXT", WIDTH//2 + 200-10-150, 100+20+40+40+30)
restart_button = Button(button_img, button_click_img, 255, "RESTART", WIDTH//2 - button_img.get_width()//2 - 100, 150+120)
esc_button = Button(button_img, button_click_img, 255, "HOME", WIDTH//2 - button_img.get_width()//2 + 100, 150+120)

pause_button = Button(pause_button_img, pause_button_click_img, 125, " ", WIDTH - pause_button_img.get_width() - 10, 10)
unpause_button = Button(button_img, button_click_img, 255, "UNPAUSE", WIDTH//2 - 160, HEIGHT//2)
home_from_pause_button = Button(button_img, button_click_img, 255, "HOME", WIDTH//2 + 10, HEIGHT//2)

#Font
font_large = pygame.font.Font("assets/font/Minecraft.ttf", 50)
font_medium = pygame.font.Font("assets/font/Minecraft.ttf", 25) 
font_small = pygame.font.Font("assets/font/Minecraft.ttf", 15) 

#Music & SFX
intro_sound = pygame.mixer.Sound("assets/music/intro.ogg")
loop_sound = pygame.mixer.Sound("assets/music/intro-loop2.ogg")
gameplay_music = pygame.mixer.Sound("assets/music/gameplay.ogg")
gamewin_sound = pygame.mixer.Sound("assets/music/game-win.ogg")
gameover_sound = pygame.mixer.Sound("assets/music/game-over.ogg")
level_up_sound = pygame.mixer.Sound("assets/music/level-up.mp3")
score_count_sound = pygame.mixer.Sound("assets/music/score-count.mp3")

jump_sound = pygame.mixer.Sound("assets/music/jump.ogg")
flower_sound = pygame.mixer.Sound("assets/music/flower-collect.ogg")
countdown_sound = pygame.mixer.Sound("assets/music/countdown.mp3")
button_hover_sound = pygame.mixer.Sound("assets/music/button-hover.mp3")
button_click_sound = pygame.mixer.Sound("assets/music/button-click.ogg")

music_channel = pygame.mixer.Channel(0); music_channel.set_volume(0.5)
jump_channel = pygame.mixer.Channel(1); jump_channel.set_volume(0.75)
flower_channel = pygame.mixer.Channel(2); flower_channel.set_volume(1.0)
button_channel = pygame.mixer.Channel(3); button_channel.set_volume(1.0)
countdown_channel = pygame.mixer.Channel(4); countdown_channel.set_volume(1.0)

#Music State
start_music_played = loop_music_playing = waiting_for_loop_to_end = False
gameplay_music_started = gamewin_music_played = countdown_sound_played = False
level_up_music_played = False
loop_cycle_end_time = 0
LOOP_LENGTH_MS = 4000 

#Background
sky = pygame.Surface((WIDTH, (HEIGHT-150))); sky.fill((144, 209, 196))
grass = pygame.Surface((WIDTH, 25)); grass.fill((101, 173, 68))
ground = pygame.Surface((WIDTH, 125)); ground.fill((158, 96, 35))

#Sparkle
sparkle_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/sparkle/spark{i}.png").convert_alpha(), (30, 30)) 
    for i in range(1, 6)
]

#Portal
portal_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/portal/portal{i}.png").convert_alpha(), (100, 100)) 
    for i in range(1, 5)
]
portal_rect = portal_frames[0].get_rect(center=(WIDTH, 300))
portal_speed = 5

#Flower
flower_positions = [(HEIGHT-150)-15, 275-15, 200-15, 125-15, 50-15] #y-positions
flower_sequence = [0, 0, 2, 3, 0, 3, 4, 3, 1, 2, 1, 4, 3, 2, 4, 2, 0, 0]
flower_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/flower/flower{i}.png").convert_alpha(), (30, 30)) 
    for i in range(1, 3)
]
flower_mask = [
    pygame.mask.from_surface(frame)
    for frame in flower_frames
]

flower_index = 0
current_flowers = []
flower_spawn_timer = [0.5*60, 1*60, 0.5*60, 1.5*60, 3*60, 2*60, 1*60, 2*60, 1.3*60, 2*60, 
        2.2*60, 1.5*60, 1*60, 1*60, 0.5*60, 2*60, 1*60, 0.5*60]  #Time before next flower spawns

#Generate Flower 
def create_flower():
    global flower_index, game_paused

    y = flower_positions[flower_sequence[flower_index]]
    rect = flower_frames[0].get_rect(bottomleft=(WIDTH, y))
    flower = {
        "surface": [flower_frames[0].copy(), flower_frames[1].copy()],
        "mask": [flower_mask[0].copy(), flower_mask[1].copy()],
        "speed": 5 if not game_paused else 0,
        "rect": rect,
        "alpha": 255,
        "fading": False
    }
    current_flowers.append(flower)
    flower_index += 1
    
#Enemy
cacty = pygame.transform.scale(pygame.image.load("assets/enemy/cacty.png").convert_alpha(), (75, 75))
cacty_rect = cacty.get_rect(bottomleft=(WIDTH, (HEIGHT-150)))
cacty_mask = pygame.mask.from_surface(cacty) 

enemies = [{
    "surface": cacty, 
    "rect": cacty_rect, 
    "mask": cacty_mask, 
    "speed": None
}]
current_enemies = []
enemy_spawn_timer = [3*60, 2*60, 2*60, 4*60, 2*60, 2*60, 1*60, 3*60, 4*60, 3*60]  #Time before next enemy spawns

#Generate Enemy
def create_enemy():
    global game_paused

    e = enemies[0]
    enemy = {
        "surface": e["surface"],
        "rect": e["rect"].copy(),  #Copy rect to avoid modifying original
        "mask": e["mask"],
        "speed": 5 if not game_paused else 0,
    }
    current_enemies.append(enemy)

#Player
player_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/girl-walk/girl-walk{i}.png").convert_alpha(), (75, 75)) 
    for i in range(1, 9)
]
player_rect = player_frames[0].get_rect(bottomright=(75, (HEIGHT-150+1)))
player_collide_frames = [
    pygame.transform.scale(pygame.image.load(f"assets/girl-collide/girl-collide{i}.png").convert_alpha(), (75, 75)) 
    for i in range(1, 4)
]

#Level Complete Screen
level_complete_screen = pygame.Surface((WIDTH, HEIGHT)); level_complete_screen.fill((0, 0, 0))
level_complete_screen.set_alpha(0)

level_complete_board = pygame.Surface((400, 200)); level_complete_board.fill((247, 219, 126))
level_complete_board_animated = False

#Bounce Animation
animation_duration = 1.5  #seconds
bounce_start_time = None 

def bounce_return_time(t):
    if t < 4/11.0:
        return (121 * t * t)/16.0
    elif t < 8/11.0:
        return (363/40.0 * t * t) - (99/10.0 * t) + 17/5.0
    elif t < 9/10.0:
        return (4356/361.0 * t * t) - (35442/1805.0 * t) + 16061/1805.0
    else:
        return (54/5.0 * t * t) - (513/25.0 * t) + 268/25.0
    
def animate_bounce(surface, x, end_y, start_y):
    global animation_duration, bounce_start_time

    if bounce_start_time is None:
        bounce_start_time = pygame.time.get_ticks() / 1000

    elapsed = (pygame.time.get_ticks() / 1000) - bounce_start_time
    t = min(elapsed / animation_duration, 1.0)
    eased_t = bounce_return_time(t)
    current_y = start_y + (end_y - start_y) * eased_t

    surface_rect = surface.get_rect(center=(x, current_y))
    screen.blit(surface, surface_rect)

def animate_bounce_outline(text, x, end_y, start_y, width):
    animate_bounce(text, x + width, end_y, start_y)
    animate_bounce(text, x - width, end_y, start_y)
    animate_bounce(text, x, end_y + width, start_y + width)
    animate_bounce(text, x, end_y - width, start_y - width)

def text_outline(text, center_x, center_y,  width):
    screen.blit(text, text.get_rect(center=(center_x + width, center_y)))
    screen.blit(text, text.get_rect(center=(center_x - width, center_y)))
    screen.blit(text, text.get_rect(center=(center_x, center_y + width)))
    screen.blit(text, text.get_rect(center=(center_x, center_y - width)))

score_counter = score_stage = stage_timer = 0  #stage_timer: for 0.5s wait between each text
score_sound_playing = False
def show_score(score, high, flowers_collected):
    global score_counter, score_stage, stage_timer, score_sound_playing

    current_time = pygame.time.get_ticks()

    #Score Counter Stage
    if score_stage == 0:
        score_counter += 0.01 * score
        
        if not score_sound_playing:
            countdown_channel.play(score_count_sound)
            score_sound_playing = True

        if int(score_counter) >= score:
            score_counter = 0
            score_stage = 1
            stage_timer = current_time
            countdown_channel.stop()
            score_sound_playing = False

    #Delay after Score
    elif score_stage == 1:
        if current_time - stage_timer >= 500:  #0.5 seconds
            score_stage = 2

    #High Score Stage
    elif score_stage == 2:
        score_counter += 0.01 * high

        if not score_sound_playing:
            countdown_channel.play(score_count_sound)
            score_sound_playing = True

        if int(score_counter) >= high:
            score_counter = 0
            score_stage = 3
            stage_timer = current_time
            countdown_channel.stop()
            score_sound_playing = False

    #Delay after High Score
    elif score_stage == 3:
        if current_time - stage_timer >= 500:
            score_stage = 4

    #Flowers Collected Stage
    elif score_stage == 4:
        score_counter += 0.05

        if not score_sound_playing:
            countdown_channel.play(score_count_sound)
            score_sound_playing = True

        if int(score_counter) >= flowers_collected:
            score_counter = flowers_collected  
            score_stage = 5
            if score_sound_playing:
                countdown_channel.stop()
                score_sound_playing = False

    #Finish SFX after all stages
    elif score_stage == 5:
        score_counter = flowers_collected
        if score_sound_playing:
                countdown_channel.stop()
                score_sound_playing = False

    #Render score text
    score_val = score if score_stage > 0 else int(score_counter)
    high_val = high if score_stage > 2 else (0 if score_stage < 2 else int(score_counter))
    flower_val = int(score_counter)

    score_text_outline = font_medium.render(f"SCORE: {score_val}", True, "White")
    score_text = font_medium.render(f"SCORE: {score_val}", True, "Black")

    highscore_text_outline = font_medium.render(f"HIGH SCORE: {high_val}", True, "White")
    highscore_text = font_medium.render(f"HIGH SCORE: {high_val}", True, "Black")

    flowers_collected_text_outline = font_medium.render(f"FLOWERS COLLECTED: {flower_val}/{len(flower_sequence)}", True, "White")
    flowers_collected_text = font_medium.render(f"FLOWERS COLLECTED: {flower_val}/{len(flower_sequence)}", True, "Black")

    #Outline text
    text_outline(score_text_outline, WIDTH//2 - 200 + 10 + score_text.get_width()//2, 120 + score_text.get_height()//2, 2)
    if score_stage >= 1:
        text_outline(highscore_text_outline, WIDTH//2 - 200 + 10 + highscore_text.get_width()//2, 160 + highscore_text.get_height()//2, 2)
    if score_stage >= 3:
        text_outline(flowers_collected_text_outline, WIDTH//2 - 200 + 10 + flowers_collected_text.get_width()//2, 200 + flowers_collected_text.get_height()//2, 2)

    #Draw
    screen.blit(score_text, (WIDTH//2 - 200 + 10, 120))
    if score_stage >= 1:
        screen.blit(highscore_text, (WIDTH//2 - 200 + 10, 160))
    if score_stage >= 3:
        screen.blit(flowers_collected_text, (WIDTH//2 - 200 + 10, 200))
   
    #Button
    back_button.animate()
    next_button.animate()

    if back_button.is_clicked():
        return 1
    elif next_button.is_clicked():
        return 2
    else:
        return 0
    
def handle_pause_screen():
    global game_paused, pause_start_time, game_home, game_active, countdown_timer, countdown_start, countdown_sound_played

    pause_overlay = pygame.Surface((WIDTH, HEIGHT))
    pause_overlay.set_alpha(120)
    pause_overlay.fill((0, 0, 0))
    screen.blit(pause_overlay, (0, 0))

    #Countdown in progress
    if countdown_start:
        if not countdown_sound_played:
            countdown_channel.play(countdown_sound)
            countdown_sound_played = True
        countdown_text_outline = font_large.render(f"{countdown_timer // 60 + 1}", True, "Black")
        countdown_text = font_large.render(f"{countdown_timer // 60 + 1}", True, "White")

        text_outline(countdown_text_outline, WIDTH//2, HEIGHT//2 - 20, 3)
        screen.blit(countdown_text, countdown_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))

        countdown_timer -= 1
        if countdown_timer <= 0:
            countdown_timer = 3*60 - 1 
            countdown_start = False
            countdown_sound_played = False
            music_channel.set_volume(0.5)
            game_paused = False
    
    else:
        #Text Colour-Blinking
        time_now = pygame.time.get_ticks()
        color = (255, 255, 255)
        if (time_now // 500) % 2 == 0:
            color = (255, 255, 255) 
        else:
            color = (247, 219, 126)

        title_outline = font_large.render("PAUSED", True, "Black")
        title = font_large.render("PAUSED", True, color)
        
        text_outline(title_outline, WIDTH//2, HEIGHT//2 - 100 + title.get_height()//2, 3)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))

        unpause_button.animate()
        home_from_pause_button.animate()

    #Unpause clicked
    if unpause_button.is_clicked():
        countdown_start = True
        countdown_timer = 3*60 - 1
        pause_button.reset()
        unpause_button.reset()

    #Home clicked
    if home_from_pause_button.is_clicked():
        reset()
        game_paused = False
        game_home = True
        game_active = False
        countdown_start = False  
        countdown_sound_played = False
        music_channel.set_volume(0.5)
        music_channel.stop()

#Reset all variables
def reset():
    global tip_state, score, loop, loop2, loop3, gravity, increment, flowers_collected, countdown_start, pause_start_time, countdown_timer
    global flower_loop, frame, sparkle_counter, portal_loop, move, end_scene, level_complete_alpha
    global enter_portal, floating_scores, level_complete, flower_index, current_flowers, current_enemies
    global enemy_spawn_timer, flower_spawn_timer, portal_rect, portal_speed
    global start_music_played, loop_music_playing, waiting_for_loop_to_end, countdown_sound_played, level_up_music_played
    global gameplay_music_started, gamewin_music_played, loop_cycle_end_time
    global bounce_start_time, score_counter, score_stage, stage_timer, score_sound_playing
    
    #Game state variables
    tip_state = 0
    score = 0
    loop = 0
    loop2 = 0
    loop3 = 0
    gravity = 0
    increment = 0
    flowers_collected = 0
    countdown_start = False
    pause_start_time = 0
    countdown_timer = 3*60 - 1 
    
    #Animation & visual variables
    flower_loop = 0
    frame = 0
    sparkle_counter = 0
    portal_loop = 0
    
    #Level completion variables
    bounce_start_time = None 
    score_counter = score_stage = stage_timer = 0 
    score_sound_playing = False
    move = 0
    end_scene = 0
    level_complete_alpha = 0
    enter_portal = 255
    level_complete = False
    
    #Collections & active objects
    floating_scores = []
    flower_index = 0
    current_flowers.clear()
    current_enemies.clear()
    
    #Reset spawn timers to original values
    enemy_spawn_timer = [3*60, 2*60, 2*60, 4*60, 2*60, 2*60, 1*60, 3*60, 4*60, 3*60]
    flower_spawn_timer = [0.5*60, 1*60, 0.5*60, 1.5*60, 3*60, 2*60, 1*60, 2*60, 1.3*60, 2*60, 
                         2.2*60, 1.5*60, 1*60, 1*60, 0.5*60, 2*60, 1*60, 0.5*60]
    
    #Reset portal position & speed
    portal_rect = portal_frames[0].get_rect(center=(WIDTH, 300))
    portal_speed = 5
    
    #Reset player position
    player_rect.x = 75
    player_rect.y = (HEIGHT-150+1)

    #Reset player alpha
    for player in player_frames:
        player.set_alpha(255)
    
    #Music state variables
    start_music_played = False
    loop_music_playing = False
    waiting_for_loop_to_end = False
    gameplay_music_started = False
    gamewin_music_played = False
    countdown_sound_played = False
    level_up_music_played = False
    loop_cycle_end_time = 0

#Game States
game_home = True
game_active = False
game_over = False
game_paused = False

#Initialization of all variables
tip_state = score = loop = loop2 = loop3 = gravity = increment = high = flowers_collected = 0
flower_loop = frame = sparkle_counter = portal_loop = move = end_scene = level_complete_alpha = 0
enter_portal = 255
countdown_start = pause_start_time = 0
countdown_timer = 3*60 - 1 
floating_scores = []
level_complete = False

#Game Loop
while True:
    current_time = pygame.time.get_ticks()

    #Main event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 

        #Handle events based on current game state
        if game_home and not game_active and not game_over:
            if event.type == pygame.USEREVENT and not loop_music_playing:
                music_channel.play(loop_sound, loops=-1)
                loop_music_playing = True

        elif game_active and not game_home and not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not move:
                increment = 1
                gravity = -20
                if tip_state == 0:
                    tip_state = 1
                if not countdown_start and not game_paused and not end_scene:
                    jump_channel.play(jump_sound)

    #Music Transition
    if waiting_for_loop_to_end and current_time >= loop_cycle_end_time:
        music_channel.stop()
        music_channel.play(gameplay_music, loops=-1)
        waiting_for_loop_to_end = False
        gameplay_music_started = True

    #Start Screen 
    if game_home and not game_active and not game_over:

        #Music Handler
        if not start_music_played:
            music_channel.play(intro_sound)
            loop_cycle_end_time = current_time + int(intro_sound.get_length()*1000)
            start_music_played = True
        elif not loop_music_playing and current_time >= loop_cycle_end_time:
            music_channel.play(loop_sound)
            loop_music_playing = True
            loop_cycle_end_time = current_time + LOOP_LENGTH_MS
        elif loop_music_playing and not waiting_for_loop_to_end and current_time >= loop_cycle_end_time:
            #Continue looping manually
            music_channel.play(loop_sound)
            loop_cycle_end_time = current_time + LOOP_LENGTH_MS

        #Reset buttons
        back_button.reset()
        next_button.reset()
        pause_button.reset()
        home_from_pause_button.reset()

        if start_button.is_clicked():
            reset()
            if score > high:
                high = score
            game_home = False
            game_active = True
            game_over = False

            #If loop is playing, wait for it to end
            if loop_music_playing:
                waiting_for_loop_to_end = True
            else:
                music_channel.stop()
                music_channel.play(gameplay_music, loops=-1)
                gameplay_music_started = True
            
        if exit_button.is_clicked():
            time.sleep(0.5)
            pygame.quit()
            exit()

        #Start Screen Draw
        screen.fill("Grey")

        title = font_large.render("LILY WANTS TO RUN", True, "Black")
        screen.blit(title, (WIDTH//2-title.get_width()//2, 75))

        start_button.animate()
        exit_button.animate()

    #Gameplay Screen
    elif not game_home and game_active and not game_over: 
        key = pygame.key.get_pressed() #Keyboard Input

        #Reset buttons
        start_button.reset()
        exit_button.reset()
        restart_button.reset()
        esc_button.reset()

        #Background
        screen.blit(sky, (0, 0))
        screen.blit(grass, (0, (HEIGHT-150)))
        screen.blit(ground, (0, 375))

        #Player Animation
        if not game_paused:
            loop2 += 1
            if loop2 == 144:
                loop2 = 0
            player = player_frames[(loop2//8) % 8]
            player_mask = pygame.mask.from_surface(player) #Only non-transparent cells

        #End-Level Cutscene
        if not enemy_spawn_timer and not current_enemies:
            end_scene = 1
        
        if end_scene:
            if not gamewin_music_played:
                music_channel.stop()
                music_channel.play(gamewin_sound)
                gamewin_music_played = True

            portal_loop += 1
            portal_rect.x -= portal_speed

            if portal_loop == 48:
                portal_loop = 0
            screen.blit(portal_frames[portal_loop//12], portal_rect)
            
            if not game_paused and portal_rect.x <= 650:
                portal_speed = 0
                if player_rect.x <= (700-37.5):
                    player_rect.x += 3
                    move = 1
                else:
                    player_rect.x += 0
                    enter_portal -= 3
                    player.set_alpha(max(enter_portal, 0))
            
            portal_sp_pos1 = portal_rect.x+20, portal_rect.y+10
            portal_sp_pos2 = portal_rect.x+80, portal_rect.y+80
            portal_sp_pos3 = portal_rect.x, portal_rect.y+60
            portal_sp_pos4 = portal_rect.x+70, portal_rect.y-15
            
            #Get current sparkle frame
            sparkle_counter += 1
            if sparkle_counter >= 44:
                sparkle_counter = 0
            temp_sp = sparkle_counter//9
            sp_frame = sparkle_frames[temp_sp]
            
            sp_transparent = sp_frame.copy()
            sp_transparent.set_alpha(150)
            screen.blit(sp_transparent, portal_sp_pos1)
            screen.blit(sp_transparent, portal_sp_pos2)
            screen.blit(sp_transparent, portal_sp_pos3)
            screen.blit(sp_transparent, portal_sp_pos4)

        #Level Complete
        if end_scene and enter_portal <= 0:
            level_complete = True
    
        if level_complete:
            if bounce_start_time is None:
                bounce_start_time = pygame.time.get_ticks() / 1000  

            if not level_up_music_played:
                music_channel.play(level_up_sound)
                level_up_music_played = True
            level_complete_alpha += 4
    
            level_complete_screen_copy = level_complete_screen.copy()

            level_complete_screen_copy.set_alpha(min(level_complete_alpha, 100))

            screen.blit(level_complete_screen_copy, (0, 0))
            animate_bounce(level_complete_board, WIDTH//2, 200, -200)

            time_now = pygame.time.get_ticks()
            color = (247, 219, 126)
            if (time_now // 500) % 2 == 0:
                color = (247, 219, 126) 
            else:
                color = (242, 166, 94)
            level_complete_sign_outline = font_large.render("LEVEL COMPLETE!", True, "Black")
            level_complete_sign = font_large.render("LEVEL COMPLETE!", True, color)
            animate_bounce_outline(level_complete_sign_outline, WIDTH//2, 50, -200, 3)
            animate_bounce(level_complete_sign, WIDTH // 2, 50, -200)

            elapsed = pygame.time.get_ticks() / 1000 - bounce_start_time
            if elapsed >= animation_duration:
                if score > high:
                    high = score

                state = show_score(score, high, flowers_collected)

                if state == 1:  #Back button
                    reset()
                    game_home = True; game_active = False; game_over = False
                    music_channel.stop()
                elif state == 2:  #Next button
                    reset()
                    game_home = False; game_active = True; game_over = False
                    music_channel.stop()
                    music_channel.play(gameplay_music, loops=-1)
                    gameplay_music_started = True

        #Player Jump
        if not game_paused:
            gravity += increment
            player_rect.y += gravity
            if player_rect.bottom >= (HEIGHT-150+1):
                player_rect.bottom = (HEIGHT-150+1)
                increment = gravity = 0
            if player_rect.top <= 0:
                player_rect.top = gravity = 0
        screen.blit(player, player_rect)

        #Flower Score
        for fs in floating_scores[:]:
            fs_surf = font_medium.render(fs["text"], True, (0, 0, 0))
            fs_surf.set_alpha(fs["alpha"])
            screen.blit(fs_surf, (fs["x"], fs["y"]))

            #Update position & alpha
            fs["y"] -= 1
            fs["alpha"] -= 5
            fs["lifetime"] -= 1

            if fs["alpha"] <= 0 or fs["lifetime"] <= 0:
                floating_scores.remove(fs)

        #Sparkle
        if not end_scene:  #Only update sparkle counter if not in end scene
            sparkle_counter += 1
            if sparkle_counter >= 44:
                sparkle_counter = 0
            temp_sp = sparkle_counter//9
            sp_frame = sparkle_frames[temp_sp]

        #Flower Animation
        flower_loop += 1
        if flower_loop == 60:
            frame = 0
        if flower_loop == 120:
            frame = 1
            flower_loop = 0

        #Flower Spawn
        if not game_paused:
            if len(flower_spawn_timer) != 0:
                flower_spawn_timer[0] -= 1
                if flower_spawn_timer[0] <= 0:
                    create_flower()
                    flower_spawn_timer.pop(0)

            for f in current_flowers[:]:
                f["rect"].x -= f["speed"]
                if f["rect"].right <= -10:
                    current_flowers.remove(f)
            
        for f in current_flowers[:]:
            screen.blit(f["surface"][frame], f["rect"])
            if not end_scene:  
                screen.blit(sp_frame, f["rect"])

        #Enemy Spawn
        if not game_paused:
            if len(enemy_spawn_timer) != 0:
                enemy_spawn_timer[0] -= 1
                if enemy_spawn_timer[0] <= 0:
                    create_enemy()
                    enemy_spawn_timer.pop(0)

            for e in current_enemies[:]:
                e["rect"].x -= e["speed"]
                if e["rect"].right <= -10:
                    current_enemies.remove(e)
                    
        for e in current_enemies[:]:
            screen.blit(e["surface"], e["rect"])

        #Pause
        if not game_paused and not end_scene: 
            pause_button.update_alpha()
            pause_button.animate()
        if pause_button.is_clicked():
            game_paused = True
        if game_paused:
            music_channel.set_volume(0.1)
            handle_pause_screen()
        
        #Collision of player with flower
        if not game_paused:
            for f in current_flowers[:]:
                if player_mask.overlap(f["mask"][frame], (f["rect"].x - player_rect.x, f["rect"].y - player_rect.y)): #returns 0 or 1
                    current_flowers.remove(f)
                    flower_channel.play(flower_sound)
                    score += 10
                    flowers_collected += 1

                    floating_scores.append({
                        "text": "+10",
                        "x": player_rect.right + 5,
                        "y": player_rect.top,
                        "alpha": 255,
                        "lifetime": 60  #1 second at 60fps
                    })

        #Collision of player with enemy
        if not game_paused:
            for e in current_enemies[:]:
                if player_mask.overlap(e["mask"], (e["rect"].x - player_rect.x, e["rect"].y - player_rect.y)): #returns 0 or 1
                    if player == player_frames[0] or player == player_frames[4]:
                        player = player_collide_frames[0]
                    elif player == player_frames[2] or player == player_frames[6]:
                        player = player_collide_frames[2]
                    else:
                        player = player_collide_frames[1]
                    screen.blit(player, player_rect)

                    music_channel.stop()
                    music_channel.play(gameover_sound)

                    game_active = False
                    game_over = True
                    break

        #Tutorial
        if tip_state == 0:
            tip = font_small.render("(press SPACE to jump)", True, "Black")
            screen.blit(tip, tip.get_rect(center=(WIDTH//2, 55)))
        
        #Score 
        if not level_complete and not game_paused:    
            loop += 1
            if loop == 60 and not end_scene:
                loop = 0
                score += 1

            game_score_outline = font_large.render("SCORE: {}".format(score), True, "White")
            game_score = font_large.render("SCORE: {}".format(score), True, "Black")

            text_outline(game_score_outline, WIDTH//2, 100, 3)
            screen.blit(game_score, game_score.get_rect(center=(WIDTH//2, 100)))

            high_score_outline = font_medium.render("HIGH SCORE: {}".format(high), True, "White")
            high_score = font_medium.render("HIGH SCORE: {}".format(high), True, "Black")

            text_outline(high_score_outline, WIDTH//2, 150, 2)
            screen.blit(high_score, high_score.get_rect(center=(WIDTH//2, 150)))

    #Game Over Screen
    elif not game_home and not game_active and game_over:
        
        #Reset buttons
        back_button.reset()
        next_button.reset()

        if restart_button.is_clicked():
            if score > high: 
                high = score
            reset()
            game_over = False
            game_active = True
            game_home = False
            music_channel.stop()
            music_channel.play(gameplay_music, loops=-1)
            gameplay_music_started = True
                
        if esc_button.is_clicked():
            if score > high:
                high = score
            reset()
            game_over = False
            game_home = True
            game_active = False
            music_channel.stop()

        #Background
        screen.blit(sky, (0, 0))
        screen.blit(grass, (0, (HEIGHT-150)))
        screen.blit(ground, (0, 375))

        screen.blit(e["surface"], e["rect"])
        screen.blit(f["surface"][frame], f["rect"])
        screen.blit(sp_frame, f["rect"])
        screen.blit(player, player_rect)
        
        game_over_text = font_large.render("GAME OVER", True, "Black")
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 75))

        #Display final score
        final_score = font_medium.render(f"FINAL SCORE: {score}", True, "Black")
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 125))

        restart_button.animate()
        esc_button.animate()

    pygame.display.update()
    clock.tick(60) #FPS=60 MAX in this project

#File save-load feature (IN PROGRESS)
"""#Find files (level1.py, level2.py, etc)
level_files= []
for f in os.listdir("levels"):
    if f.startswith("level") and f.endswith(".py"):
        level_files.append(f)
level_files.sort()

#Importing levels
levels= []
for f in level_files:
    mod= importlib.import_module(f"levels.{f[:-3]}") #Importing level1.py, level2.py, etc
    level= getattr(mod, "Level") #Getting classes Level1, Level2, etc
    levels.append(level())"""