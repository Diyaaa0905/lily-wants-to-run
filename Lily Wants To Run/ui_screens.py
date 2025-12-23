"""
UI screen rendering functions
"""
import pygame
from config import WIDTH, HEIGHT
from animations import text_outline
from music import countdown_channel, score_count_sound, countdown_sound, music_channel

def show_score(screen, font_medium, score, high, flowers_collected, flower_sequence_len, 
               score_counter, score_stage, stage_timer, score_sound_playing):
    """Display and animate score counting"""
    current_time = pygame.time.get_ticks()

    # Score Counter Stage
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

    # Delay after Score
    elif score_stage == 1:
        if current_time - stage_timer >= 500:
            score_stage = 2

    # High Score Stage
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

    # Delay after High Score
    elif score_stage == 3:
        if current_time - stage_timer >= 500:
            score_stage = 4

    # Flowers Collected Stage
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

    # Finish SFX after all stages
    elif score_stage == 5:
        score_counter = flowers_collected
        if score_sound_playing:
            countdown_channel.stop()
            score_sound_playing = False

    # Render score text
    score_val = score if score_stage > 0 else int(score_counter)
    high_val = high if score_stage > 2 else (0 if score_stage < 2 else int(score_counter))
    flower_val = int(score_counter)

    score_text_outline = font_medium.render(f"SCORE: {score_val}", True, "White")
    score_text = font_medium.render(f"SCORE: {score_val}", True, "Black")

    highscore_text_outline = font_medium.render(f"HIGH SCORE: {high_val}", True, "White")
    highscore_text = font_medium.render(f"HIGH SCORE: {high_val}", True, "Black")

    flowers_collected_text_outline = font_medium.render(f"FLOWERS COLLECTED: {flower_val}/{flower_sequence_len}", True, "White")
    flowers_collected_text = font_medium.render(f"FLOWERS COLLECTED: {flower_val}/{flower_sequence_len}", True, "Black")

    # Outline text
    text_outline(screen, score_text_outline, WIDTH//2 - 200 + 10 + score_text.get_width()//2, 
                120 + score_text.get_height()//2, 2)
    if score_stage >= 1:
        text_outline(screen, highscore_text_outline, WIDTH//2 - 200 + 10 + highscore_text.get_width()//2, 
                    160 + highscore_text.get_height()//2, 2)
    if score_stage >= 3:
        text_outline(screen, flowers_collected_text_outline, WIDTH//2 - 200 + 10 + flowers_collected_text.get_width()//2, 
                    200 + flowers_collected_text.get_height()//2, 2)

    # Draw
    screen.blit(score_text, (WIDTH//2 - 200 + 10, 120))
    if score_stage >= 1:
        screen.blit(highscore_text, (WIDTH//2 - 200 + 10, 160))
    if score_stage >= 3:
        screen.blit(flowers_collected_text, (WIDTH//2 - 200 + 10, 200))
    
    return score_counter, score_stage, stage_timer, score_sound_playing

def handle_pause_screen(screen, font_large, countdown_timer, countdown_start, countdown_sound_played,
                       unpause_button, home_from_pause_button):
    """Handle pause screen rendering and countdown"""
    pause_overlay = pygame.Surface((WIDTH, HEIGHT))
    pause_overlay.set_alpha(120)
    pause_overlay.fill((0, 0, 0))
    screen.blit(pause_overlay, (0, 0))

    # Countdown in progress
    if countdown_start:
        if not countdown_sound_played:
            countdown_channel.play(countdown_sound)
            countdown_sound_played = True
        countdown_text_outline = font_large.render(f"{countdown_timer // 60 + 1}", True, "Black")
        countdown_text = font_large.render(f"{countdown_timer // 60 + 1}", True, "White")

        text_outline(screen, countdown_text_outline, WIDTH//2, HEIGHT//2 - 20, 3)
        screen.blit(countdown_text, countdown_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))

        countdown_timer -= 1
        if countdown_timer <= 0:
            countdown_timer = 3*60 - 1
            countdown_start = False
            countdown_sound_played = False
            music_channel.set_volume(0.5)
            game_paused = False
            return countdown_timer, countdown_start, countdown_sound_played, game_paused
    
    else:
        # Text Colour-Blinking
        time_now = pygame.time.get_ticks()
        color = (255, 255, 255)
        if (time_now // 500) % 2 == 0:
            color = (255, 255, 255)
        else:
            color = (247, 219, 126)

        title_outline = font_large.render("PAUSED", True, "Black")
        title = font_large.render("PAUSED", True, color)
        
        text_outline(screen, title_outline, WIDTH//2, HEIGHT//2 - 100 + title.get_height()//2, 3)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))

        unpause_button.animate(screen)
        home_from_pause_button.animate(screen)

    return countdown_timer, countdown_start, countdown_sound_played, None