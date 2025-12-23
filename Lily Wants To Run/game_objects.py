"""
Game object creation and management
"""
import pygame
from config import WIDTH, HEIGHT

def create_flower(flower_frames, flower_mask, level_config, flower_index, game_paused):
    """Create a new flower object based on level configuration"""
    y = level_config.flower_positions[level_config.flower_sequence[flower_index]]
    rect = flower_frames[0].get_rect(bottomleft=(WIDTH, y))
    flower = {
        "surface": [flower_frames[0].copy(), flower_frames[1].copy()],
        "mask": [flower_mask[0].copy(), flower_mask[1].copy()],
        "speed": 5 if not game_paused else 0,
        "rect": rect,
        "alpha": 255,
        "fading": False
    }
    return flower

def create_enemy(enemy_assets, level_config, enemy_index, game_paused):
    """Create a new enemy object based on level configuration"""
    enemy_type = level_config.enemy_sequence[enemy_index]
    enemy_data = enemy_assets[enemy_type]
    
    enemy_y = level_config.enemy_spawn_y[enemy_index]
    enemy_rect = enemy_data['surface'].get_rect(bottomleft=(WIDTH, enemy_y))
    
    enemy = {
        "surface": enemy_data['surface'],
        "rect": enemy_rect,
        "mask": enemy_data['mask'],
        "speed": 5 if not game_paused else 0,
        "type": enemy_type
    }
    return enemy

def create_portal_rect(portal_frames):
    """Create portal rectangle"""
    return portal_frames[0].get_rect(center=(WIDTH, 300))

def reset_player_position(player_rect):
    """Reset player to initial position"""
    player_rect.x = 75
    player_rect.y = (HEIGHT-150+1)
    return player_rect

def reset_player_alpha(player_frames):
    """Reset alpha for all player frames"""
    for player in player_frames:
        player.set_alpha(255)

def create_background_surfaces(level_config):
    """Create background surfaces based on level configuration"""
    sky = pygame.Surface((WIDTH, (HEIGHT-150)))
    sky.fill(level_config.background_color)
    
    grass = pygame.Surface((WIDTH, 25))
    grass.fill(level_config.grass_color)
    
    ground = pygame.Surface((WIDTH, 125))
    ground.fill(level_config.ground_color)
    
    return sky, grass, ground