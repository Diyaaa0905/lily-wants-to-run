"""
Animation utilities
"""
import pygame

def bounce_return_time(t):
    """Easing function for bounce animation"""
    if t < 4/11.0:
        return (121 * t * t)/16.0
    elif t < 8/11.0:
        return (363/40.0 * t * t) - (99/10.0 * t) + 17/5.0
    elif t < 9/10.0:
        return (4356/361.0 * t * t) - (35442/1805.0 * t) + 16061/1805.0
    else:
        return (54/5.0 * t * t) - (513/25.0 * t) + 268/25.0

def animate_bounce(screen, surface, x, end_y, start_y, bounce_start_time, animation_duration):
    """Animate a surface with bounce effect"""
    if bounce_start_time is None:
        bounce_start_time = pygame.time.get_ticks() / 1000

    elapsed = (pygame.time.get_ticks() / 1000) - bounce_start_time
    t = min(elapsed / animation_duration, 1.0)
    eased_t = bounce_return_time(t)
    current_y = start_y + (end_y - start_y) * eased_t

    surface_rect = surface.get_rect(center=(x, current_y))
    screen.blit(surface, surface_rect)
    
    return bounce_start_time

def animate_bounce_outline(screen, text, x, end_y, start_y, width, bounce_start_time, animation_duration):
    """Animate text outline with bounce effect"""
    bounce_start_time = animate_bounce(screen, text, x + width, end_y, start_y, bounce_start_time, animation_duration)
    bounce_start_time = animate_bounce(screen, text, x - width, end_y, start_y, bounce_start_time, animation_duration)
    bounce_start_time = animate_bounce(screen, text, x, end_y + width, start_y + width, bounce_start_time, animation_duration)
    bounce_start_time = animate_bounce(screen, text, x, end_y - width, start_y - width, bounce_start_time, animation_duration)
    return bounce_start_time

def text_outline(screen, text, center_x, center_y, width):
    """Draw text with outline effect"""
    screen.blit(text, text.get_rect(center=(center_x + width, center_y)))
    screen.blit(text, text.get_rect(center=(center_x - width, center_y)))
    screen.blit(text, text.get_rect(center=(center_x, center_y + width)))
    screen.blit(text, text.get_rect(center=(center_x, center_y - width)))