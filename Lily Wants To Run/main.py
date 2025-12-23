import time
import pygame
from sys import exit

# Import configuration and modules
from config import WIDTH, HEIGHT, FPS, ANIMATION_DURATION, LOOP_LENGTH_MS
from music import *
from game_state import GameState
from assets_loader import *
from buttons import create_all_buttons
from animations import animate_bounce, animate_bounce_outline, text_outline
from game_objects import (create_flower, create_enemy, create_portal_rect, 
                          reset_player_position, reset_player_alpha, create_background_surfaces)
from ui_screens import show_score, handle_pause_screen
from levels import get_level, get_total_levels

# Initialize Pygame
pygame.mixer.pre_init(frequency=44100, size=-16, channels=5, buffer=32)
pygame.init()
pygame.mixer.init()

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lily Wants To Run")
clock = pygame.time.Clock()

# Load fonts
font_large = pygame.font.Font("assets/font/Minecraft.ttf", 50)
font_medium = pygame.font.Font("assets/font/Minecraft.ttf", 25)
font_small = pygame.font.Font("assets/font/Minecraft.ttf", 15)

# Load assets
button_images = load_button_images()
static_backgrounds = load_background_surfaces()
sparkle_frames = load_sparkle_frames()
portal_frames = load_portal_frames()
flower_frames, flower_mask = load_flower_frames()
player_frames, player_collide_frames = load_player_frames()
enemy_assets = load_enemy_assets()
board = load_board()

# Create buttons
buttons = create_all_buttons(button_images)

# Create game objects
player_rect = player_frames[0].get_rect(bottomright=(75, (HEIGHT-150+1)))
portal_rect = create_portal_rect(portal_frames)

# Initialize game state
game_state = GameState()

# Dynamic backgrounds (will be updated per level)
sky, grass, ground = None, None, None

# Game Loop
while True:
    current_time = pygame.time.get_ticks()

    # Main event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state.game_home and not game_state.game_active and not game_state.game_over:
            if event.type == pygame.USEREVENT and not game_state.loop_music_playing:
                music_channel.play(loop_sound, loops=-1)
                game_state.loop_music_playing = True

        elif game_state.game_active and not game_state.game_home and not game_state.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_state.move:
                game_state.increment = 1
                game_state.gravity = -20
                if game_state.tip_state == 0:
                    game_state.tip_state = 1
                if not game_state.countdown_start and not game_state.game_paused and not game_state.end_scene:
                    jump_channel.play(jump_sound)

    # Music Transition
    if game_state.waiting_for_loop_to_end and current_time >= game_state.loop_cycle_end_time:
        music_channel.stop()
        music_channel.play(gameplay_music, loops=-1)
        game_state.waiting_for_loop_to_end = False
        game_state.gameplay_music_started = True

    # START SCREEN
    if game_state.game_home and not game_state.game_active and not game_state.game_over:
        # Music Handler
        if not game_state.start_music_played:
            music_channel.play(intro_sound)
            game_state.loop_cycle_end_time = current_time + int(intro_sound.get_length()*1000)
            game_state.start_music_played = True
        elif not game_state.loop_music_playing and current_time >= game_state.loop_cycle_end_time:
            music_channel.play(loop_sound)
            game_state.loop_music_playing = True
            game_state.loop_cycle_end_time = current_time + LOOP_LENGTH_MS
        elif game_state.loop_music_playing and not game_state.waiting_for_loop_to_end and current_time >= game_state.loop_cycle_end_time:
            music_channel.play(loop_sound)
            game_state.loop_cycle_end_time = current_time + LOOP_LENGTH_MS

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))

        buttons['back'].reset()
        buttons['next'].reset()
        buttons['pause'].reset()
        buttons['home_from_pause'].reset()

        if buttons['start'].is_clicked() and game_state.start_state == 0:
            # Load level 1
            level_config = get_level(1)
            if level_config:
                game_state.reset_game()
                game_state.load_level(level_config)
                sky, grass, ground = create_background_surfaces(level_config)
                
                if game_state.score > game_state.high:
                    game_state.high = game_state.score
                
                portal_rect = create_portal_rect(portal_frames)
                reset_player_position(player_rect)
                reset_player_alpha(player_frames)
                
                game_state.game_home = False
                game_state.game_active = True
                game_state.game_over = False

                if game_state.loop_music_playing:
                    game_state.waiting_for_loop_to_end = True
                else:
                    music_channel.stop()
                    music_channel.play(gameplay_music, loops=-1)
                    game_state.gameplay_music_started = True

        if buttons['exit'].is_clicked():
            time.sleep(0.5)
            pygame.quit()
            exit()

        if buttons['how_start'].is_clicked():
            game_state.start_state = 1

        if buttons['volume_start'].is_clicked():
            game_state.start_state = 2

        screen.fill("Grey")

        title = font_large.render("LILY WANTS TO RUN", True, "Black")
        screen.blit(title, (WIDTH//2-title.get_width()//2, 75))

        version = font_small.render("v 1.0", True, "Black")
        screen.blit(version, (10, HEIGHT-version.get_height()-10))

        made_by = font_small.render("DIYA JAISWAL ^_^", True, "Black")
        screen.blit(made_by, (WIDTH-made_by.get_width()-10, HEIGHT-made_by.get_height()-10))

        if game_state.start_state == 0:
            buttons['start'].animate(screen)
            buttons['exit'].animate(screen)
            buttons['how_start'].animate(screen)
            buttons['volume_start'].animate(screen)
            buttons['x0'].reset()

        how_to_play = [font_medium.render("Press SPACE to jump.", True, "Black"),
                      font_medium.render("Collect all flowers.", True, "Black"),
                      font_medium.render("Help Lily run!", True, "Black")]
        
        if game_state.start_state == 1:
            buttons['how_start'].reset()
            game_state.timer += 1
            screen.blit(overlay, (0, 0))
            game_state.bounce_start_time = animate_bounce(screen, board, WIDTH//2, 200, -200, 
                                                          game_state.bounce_start_time, ANIMATION_DURATION)
            if game_state.timer >= 60:
                game_state.bounce_start_time = None
                h0 = how_to_play[0].get_height()
                h1 = how_to_play[1].get_height()
                h2 = how_to_play[2].get_height()
                
                screen.blit(board, (WIDTH//2-board.get_width()//2, 200-board.get_height()//2))
                screen.blit(how_to_play[0], (WIDTH//2-how_to_play[0].get_width()//2, 200-h1//2-h0+15))
                screen.blit(how_to_play[1], (WIDTH//2-how_to_play[1].get_width()//2, 200-h1//2+15))
                screen.blit(how_to_play[2], (WIDTH//2-how_to_play[2].get_width()//2, 200-h1//2+h2+15))
                buttons['x0'].animate(screen)
            if buttons['x0'].is_clicked():
                game_state.timer = 0
                game_state.start_state = 0

        if game_state.start_state == 2:
            buttons['volume_start'].reset()
            game_state.timer += 1
            screen.blit(overlay, (0, 0))
            game_state.bounce_start_time = animate_bounce(screen, board, WIDTH//2, 200, -200, 
                                                          game_state.bounce_start_time, ANIMATION_DURATION)
            if game_state.timer >= 60:
                game_state.bounce_start_time = None
                
                screen.blit(board, (WIDTH//2-board.get_width()//2, 200-board.get_height()//2))
                screen.blit(button_images['bg_icon'], (241, 167))
                screen.blit(button_images['sfx_icon'], (241, 229))
                screen.blit(static_backgrounds['bar'], (320, 180))
                screen.blit(static_backgrounds['bar'], (320, 242))
                buttons['x0'].animate(screen)
                buttons['left_arrow'][0].animate(screen)
                buttons['left_arrow'][1].animate(screen)
                buttons['right_arrow'][0].animate(screen)
                buttons['right_arrow'][1].animate(screen)
            if buttons['x0'].is_clicked():
                game_state.timer = 0
                game_state.start_state = 0

    # GAMEPLAY SCREEN
    elif not game_state.game_home and game_state.game_active and not game_state.game_over:
        buttons['start'].reset()
        buttons['exit'].reset()
        buttons['how_start'].reset()
        buttons['volume_start'].reset()
        buttons['restart'].reset()
        buttons['esc'].reset()

        # Background
        screen.blit(sky, (0, 0))
        screen.blit(grass, (0, HEIGHT-150))
        screen.blit(ground, (0, 375))

        # Player Animation
        if not game_state.game_paused:
            game_state.loop2 += 1
            if game_state.loop2 == 144:
                game_state.loop2 = 0
            player = player_frames[(game_state.loop2//8) % 8]
            player_mask = pygame.mask.from_surface(player)

        # End-Level Cutscene
        if not game_state.enemy_spawn_timer and not game_state.current_enemies:
            game_state.end_scene = 1

        if game_state.end_scene:
            if not game_state.gamewin_music_played:
                music_channel.stop()
                music_channel.play(gamewin_sound)
                game_state.gamewin_music_played = True

            game_state.portal_loop += 1
            portal_rect.x -= game_state.portal_speed

            if game_state.portal_loop == 48:
                game_state.portal_loop = 0
            screen.blit(portal_frames[game_state.portal_loop//12], portal_rect)

            if not game_state.game_paused and portal_rect.x <= 650:
                game_state.portal_speed = 0
                if player_rect.x <= (700-37.5):
                    player_rect.x += 3
                    game_state.move = 1
                else:
                    player_rect.x += 0
                    game_state.enter_portal -= 3
                    player.set_alpha(max(game_state.enter_portal, 0))

            portal_sp_pos1 = portal_rect.x+20, portal_rect.y+10
            portal_sp_pos2 = portal_rect.x+80, portal_rect.y+80
            portal_sp_pos3 = portal_rect.x, portal_rect.y+60
            portal_sp_pos4 = portal_rect.x+70, portal_rect.y-15

            game_state.sparkle_counter += 1
            if game_state.sparkle_counter >= 44:
                game_state.sparkle_counter = 0
            temp_sp = game_state.sparkle_counter//9
            sp_frame = sparkle_frames[temp_sp]

            sp_transparent = sp_frame.copy()
            sp_transparent.set_alpha(150)
            screen.blit(sp_transparent, portal_sp_pos1)
            screen.blit(sp_transparent, portal_sp_pos2)
            screen.blit(sp_transparent, portal_sp_pos3)
            screen.blit(sp_transparent, portal_sp_pos4)

        # Level Complete
        if game_state.end_scene and game_state.enter_portal <= 0:
            game_state.level_complete = True

        if game_state.level_complete:
            if game_state.bounce_start_time is None:
                game_state.bounce_start_time = pygame.time.get_ticks() / 1000

            if not game_state.level_up_music_played:
                music_channel.play(level_up_sound)
                game_state.level_up_music_played = True
            game_state.level_complete_alpha += 4

            level_complete_screen_copy = static_backgrounds['level_complete_screen'].copy()
            level_complete_screen_copy.set_alpha(min(game_state.level_complete_alpha, 100))

            screen.blit(level_complete_screen_copy, (0, 0))
            game_state.bounce_start_time = animate_bounce(screen, board, WIDTH//2, 200, -200, 
                                                          game_state.bounce_start_time, ANIMATION_DURATION)

            time_now = pygame.time.get_ticks()
            color = (247, 219, 126) if (time_now // 500) % 2 == 0 else (242, 166, 94)
            level_complete_sign_outline = font_large.render("LEVEL COMPLETE!", True, "Black")
            level_complete_sign = font_large.render("LEVEL COMPLETE!", True, color)
            animate_bounce_outline(screen, level_complete_sign_outline, WIDTH//2, 50, -200, 3, 
                                 game_state.bounce_start_time, ANIMATION_DURATION)
            animate_bounce(screen, level_complete_sign, WIDTH//2, 50, -200, 
                          game_state.bounce_start_time, ANIMATION_DURATION)

            elapsed = pygame.time.get_ticks() / 1000 - game_state.bounce_start_time
            if elapsed >= ANIMATION_DURATION:
                if game_state.score > game_state.high:
                    game_state.high = game_state.score

                (game_state.score_counter, game_state.score_stage, 
                 game_state.stage_timer, game_state.score_sound_playing) = show_score(
                    screen, font_medium, game_state.score, game_state.high, 
                    game_state.flowers_collected, game_state.current_level.get_flower_count(),
                    game_state.score_counter, game_state.score_stage, 
                    game_state.stage_timer, game_state.score_sound_playing
                )

                buttons['back'].animate(screen)
                
                # Only show next button if there are more levels
                if game_state.current_level_number < get_total_levels():
                    buttons['next'].animate(screen)

                if buttons['back'].is_clicked():
                    game_state.reset_game()
                    game_state.reset_to_level_1()
                    portal_rect = create_portal_rect(portal_frames)
                    reset_player_position(player_rect)
                    reset_player_alpha(player_frames)
                    game_state.game_home = True
                    game_state.game_active = False
                    game_state.game_over = False
                    music_channel.stop()
                elif buttons['next'].is_clicked() and game_state.current_level_number < get_total_levels():
                    # Load next level
                    game_state.next_level()
                    level_config = get_level(game_state.current_level_number)
                    if level_config:
                        game_state.reset_game(keep_level=False)
                        game_state.load_level(level_config)
                        sky, grass, ground = create_background_surfaces(level_config)
                        
                        portal_rect = create_portal_rect(portal_frames)
                        reset_player_position(player_rect)
                        reset_player_alpha(player_frames)
                        game_state.game_home = False
                        game_state.game_active = True
                        game_state.game_over = False
                        music_channel.stop()
                        music_channel.play(gameplay_music, loops=-1)
                        game_state.gameplay_music_started = True

        # Player Jump
        if not game_state.game_paused:
            game_state.gravity += game_state.increment
            player_rect.y += game_state.gravity
            if player_rect.bottom >= (HEIGHT-150+1):
                player_rect.bottom = (HEIGHT-150+1)
                game_state.increment = game_state.gravity = 0
            if player_rect.top <= 0:
                player_rect.top = game_state.gravity = 0
        screen.blit(player, player_rect)

        # Flower Score
        for fs in game_state.floating_scores[:]:
            fs_surf = font_medium.render(fs["text"], True, (0, 0, 0))
            fs_surf.set_alpha(fs["alpha"])
            screen.blit(fs_surf, (fs["x"], fs["y"]))

            fs["y"] -= 1
            fs["alpha"] -= 5
            fs["lifetime"] -= 1

            if fs["alpha"] <= 0 or fs["lifetime"] <= 0:
                game_state.floating_scores.remove(fs)

        # Sparkle
        if not game_state.end_scene:
            game_state.sparkle_counter += 1
            if game_state.sparkle_counter >= 44:
                game_state.sparkle_counter = 0
            temp_sp = game_state.sparkle_counter//9
            sp_frame = sparkle_frames[temp_sp]

        # Flower Animation
        game_state.flower_loop += 1
        if game_state.flower_loop == 60:
            game_state.frame = 0
        if game_state.flower_loop == 120:
            game_state.frame = 1
            game_state.flower_loop = 0

        # Flower Spawn
        if not game_state.game_paused:
            if len(game_state.flower_spawn_timer) != 0:
                game_state.flower_spawn_timer[0] -= 1
                if game_state.flower_spawn_timer[0] <= 0:
                    new_flower = create_flower(flower_frames, flower_mask, game_state.current_level,
                                              game_state.flower_index, game_state.game_paused)
                    game_state.current_flowers.append(new_flower)
                    game_state.flower_index += 1
                    game_state.flower_spawn_timer.pop(0)

            for f in game_state.current_flowers[:]:
                f["rect"].x -= f["speed"]
                if f["rect"].right <= -10:
                    game_state.current_flowers.remove(f)

        for f in game_state.current_flowers[:]:
            screen.blit(f["surface"][game_state.frame], f["rect"])
            if not game_state.end_scene:
                screen.blit(sp_frame, f["rect"])

        # Enemy Spawn
        enemy_index = game_state.current_level.get_enemy_count() - len(game_state.enemy_spawn_timer)
        if not game_state.game_paused:
            if len(game_state.enemy_spawn_timer) != 0:
                game_state.enemy_spawn_timer[0] -= 1
                if game_state.enemy_spawn_timer[0] <= 0:
                    current_enemy_index = game_state.current_level.get_enemy_count() - len(game_state.enemy_spawn_timer)
                    new_enemy = create_enemy(enemy_assets, game_state.current_level,
                                            current_enemy_index, game_state.game_paused)
                    game_state.current_enemies.append(new_enemy)
                    game_state.enemy_spawn_timer.pop(0)

            for e in game_state.current_enemies[:]:
                e["rect"].x -= e["speed"]
                if e["rect"].right <= -10:
                    game_state.current_enemies.remove(e)

        for e in game_state.current_enemies[:]:
            screen.blit(e["surface"], e["rect"])

        # Pause
        if not game_state.game_paused and not game_state.end_scene:
            buttons['pause'].update_alpha()
            buttons['pause'].animate(screen)
        if buttons['pause'].is_clicked():
            game_state.game_paused = True
        if game_state.game_paused:
            music_channel.set_volume(0.1)
            result = handle_pause_screen(screen, font_large, game_state.countdown_timer, 
                                        game_state.countdown_start, game_state.countdown_sound_played,
                                        buttons['unpause'], buttons['home_from_pause'])
            game_state.countdown_timer, game_state.countdown_start, game_state.countdown_sound_played, pause_result = result
            if pause_result is not None:
                game_state.game_paused = pause_result

            if buttons['unpause'].is_clicked():
                game_state.countdown_start = True
                game_state.countdown_timer = 3*60 - 1
                buttons['pause'].reset()
                buttons['unpause'].reset()

            if buttons['home_from_pause'].is_clicked():
                game_state.reset_game()
                game_state.reset_to_level_1()
                portal_rect = create_portal_rect(portal_frames)
                reset_player_position(player_rect)
                reset_player_alpha(player_frames)
                game_state.game_paused = False
                game_state.game_home = True
                game_state.game_active = False
                game_state.countdown_start = False
                game_state.countdown_sound_played = False
                music_channel.set_volume(0.5)
                music_channel.stop()

        # Collision of player with flower
        if not game_state.game_paused:
            for f in game_state.current_flowers[:]:
                if player_mask.overlap(f["mask"][game_state.frame], 
                                      (f["rect"].x - player_rect.x, f["rect"].y - player_rect.y)):
                    game_state.current_flowers.remove(f)
                    flower_channel.play(flower_sound)
                    game_state.score += 10
                    game_state.flowers_collected += 1

                    game_state.floating_scores.append({
                        "text": "+10",
                        "x": player_rect.right + 5,
                        "y": player_rect.top,
                        "alpha": 255,
                        "lifetime": 60
                    })

        # Collision of player with enemy
        if not game_state.game_paused:
            for e in game_state.current_enemies[:]:
                if player_mask.overlap(e["mask"], (e["rect"].x - player_rect.x, e["rect"].y - player_rect.y)):
                    if player == player_frames[0] or player == player_frames[4]:
                        player = player_collide_frames[0]
                    elif player == player_frames[2] or player == player_frames[6]:
                        player = player_collide_frames[2]
                    else:
                        player = player_collide_frames[1]
                    screen.blit(player, player_rect)

                    music_channel.stop()
                    music_channel.play(gameover_sound)

                    game_state.game_active = False
                    game_state.game_over = True
                    break

        # Tutorial
        if game_state.tip_state == 0:
            tip = font_small.render("(press SPACE to jump)", True, "Black")
            screen.blit(tip, tip.get_rect(center=(WIDTH//2, 55)))

        # Score and Level Display
        if not game_state.level_complete and not game_state.game_paused:
            game_state.loop += 1
            if game_state.loop == 60 and not game_state.end_scene:
                game_state.loop = 0
                game_state.score += 1

            # Level indicator
            level_indicator = font_small.render(f"LEVEL {game_state.current_level_number}", True, "White")
            level_indicator_bg = font_small.render(f"LEVEL {game_state.current_level_number}", True, "Black")
            text_outline(screen, level_indicator_bg, 60, 30, 2)
            screen.blit(level_indicator, level_indicator.get_rect(center=(60, 30)))

            game_score_outline = font_large.render("SCORE: {}".format(game_state.score), True, "White")
            game_score = font_large.render("SCORE: {}".format(game_state.score), True, "Black")

            text_outline(screen, game_score_outline, WIDTH//2, 100, 3)
            screen.blit(game_score, game_score.get_rect(center=(WIDTH//2, 100)))

            high_score_outline = font_medium.render("HIGH SCORE: {}".format(game_state.high), True, "White")
            high_score = font_medium.render("HIGH SCORE: {}".format(game_state.high), True, "Black")

            text_outline(screen, high_score_outline, WIDTH//2, 150, 2)
            screen.blit(high_score, high_score.get_rect(center=(WIDTH//2, 150)))

    # GAME OVER SCREEN
    elif not game_state.game_home and not game_state.game_active and game_state.game_over:
        buttons['back'].reset()
        buttons['next'].reset()

        if buttons['restart'].is_clicked():
            if game_state.score > game_state.high:
                game_state.high = game_state.score
            
            # Restart current level
            level_config = get_level(game_state.current_level_number)
            if level_config:
                game_state.reset_game(keep_level=False)
                game_state.load_level(level_config)
                sky, grass, ground = create_background_surfaces(level_config)
                
                portal_rect = create_portal_rect(portal_frames)
                reset_player_position(player_rect)
                reset_player_alpha(player_frames)
                game_state.game_over = False
                game_state.game_active = True
                game_state.game_home = False
                music_channel.stop()
                music_channel.play(gameplay_music, loops=-1)
                game_state.gameplay_music_started = True

        if buttons['esc'].is_clicked():
            if game_state.score > game_state.high:
                game_state.high = game_state.score
            game_state.reset_game()
            game_state.reset_to_level_1()
            portal_rect = create_portal_rect(portal_frames)
            reset_player_position(player_rect)
            reset_player_alpha(player_frames)
            game_state.game_over = False
            game_state.game_home = True
            game_state.game_active = False
            music_channel.stop()

        # Background
        screen.blit(sky, (0, 0))
        screen.blit(grass, (0, HEIGHT-150))
        screen.blit(ground, (0, 375))

        if game_state.current_enemies:
            e = game_state.current_enemies[0]
            screen.blit(e["surface"], e["rect"])
        if game_state.current_flowers:
            f = game_state.current_flowers[0]
            screen.blit(f["surface"][game_state.frame], f["rect"])
            screen.blit(sp_frame, f["rect"])
        screen.blit(player, player_rect)

        game_over_text = font_large.render("GAME OVER", True, "Black")
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 75))

        final_score = font_medium.render(f"FINAL SCORE: {game_state.score}", True, "Black")
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 125))

        buttons['restart'].animate(screen)
        buttons['esc'].animate(screen)

    pygame.display.update()
    clock.tick(FPS)