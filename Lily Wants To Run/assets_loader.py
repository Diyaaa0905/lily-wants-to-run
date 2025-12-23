"""
Asset loading utilities for images and surfaces
"""
import pygame
from config import WIDTH, HEIGHT

def load_button_images():
    """Load all button images"""
    button_img = [
        pygame.transform.scale(pygame.image.load("assets/buttons/button.png").convert_alpha(), (150, 50)),
        pygame.transform.scale(pygame.image.load("assets/buttons/button-press.png").convert_alpha(), (150, 50))
    ]
    
    small_button_img = [
        pygame.transform.scale(pygame.image.load("assets/buttons/small-button.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("assets/buttons/small-button-press.png").convert_alpha(), (50, 50))
    ]
    
    smaller_button_img = [
        pygame.transform.scale(pygame.image.load("assets/buttons/small-button.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("assets/buttons/small-button-press.png").convert_alpha(), (30, 30))
    ]
    
    volume_button_img = [
        pygame.transform.scale(pygame.image.load("assets/buttons/volume-button.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("assets/buttons/volume-button-press.png").convert_alpha(), (50, 50))
    ]
    
    pause_button_img = [
        pygame.transform.scale(pygame.image.load("assets/buttons/pause-button.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("assets/buttons/pause-button-press.png").convert_alpha(), (50, 50))
    ]
    
    bg_icon_img = pygame.transform.scale(pygame.image.load("assets/board/bg-icon.png").convert_alpha(), (40, 40))
    sfx_icon_img = pygame.transform.scale(pygame.image.load("assets/board/sfx-icon.png").convert_alpha(), (40, 40))
    
    return {
        'button': button_img,
        'small_button': small_button_img,
        'smaller_button': smaller_button_img,
        'volume_button': volume_button_img,
        'pause_button': pause_button_img,
        'bg_icon': bg_icon_img,
        'sfx_icon': sfx_icon_img
    }

def load_background_surfaces():
    """Create background surfaces"""
    sky = pygame.Surface((WIDTH, (HEIGHT-150)))
    sky.fill((144, 209, 196))
    
    grass = pygame.Surface((WIDTH, 25))
    grass.fill((101, 173, 68))
    
    ground = pygame.Surface((WIDTH, 125))
    ground.fill((158, 96, 35))
    
    bar = pygame.Surface((211, 14))
    bar.fill((255, 255, 255))
    
    level_complete_screen = pygame.Surface((WIDTH, HEIGHT))
    level_complete_screen.fill((0, 0, 0))
    level_complete_screen.set_alpha(0)
    
    return {
        'sky': sky,
        'grass': grass,
        'ground': ground,
        'bar': bar,
        'level_complete_screen': level_complete_screen
    }

def load_sparkle_frames():
    """Load sparkle animation frames"""
    return [
        pygame.transform.scale(pygame.image.load(f"assets/sparkle/spark{i}.png").convert_alpha(), (30, 30))
        for i in range(1, 6)
    ]

def load_portal_frames():
    """Load portal animation frames"""
    return [
        pygame.transform.scale(pygame.image.load(f"assets/portal/portal{i}.png").convert_alpha(), (100, 100))
        for i in range(1, 5)
    ]

def load_flower_frames():
    """Load flower animation frames and masks"""
    frames = [
        pygame.transform.scale(pygame.image.load(f"assets/flower/flower{i}.png").convert_alpha(), (30, 30))
        for i in range(1, 3)
    ]
    masks = [pygame.mask.from_surface(frame) for frame in frames]
    return frames, masks

def load_player_frames():
    """Load player animation frames"""
    walk_frames = [
        pygame.transform.scale(pygame.image.load(f"assets/girl-walk/girl-walk{i}.png").convert_alpha(), (75, 75))
        for i in range(1, 9)
    ]
    
    collide_frames = [
        pygame.transform.scale(pygame.image.load(f"assets/girl-collide/girl-collide{i}.png").convert_alpha(), (75, 75))
        for i in range(1, 4)
    ]
    
    return walk_frames, collide_frames

def load_enemy_assets():
    """Load all enemy sprites and create masks"""
    enemies = {}
    
    # Load cactus enemy
    cacty = pygame.transform.scale(pygame.image.load("assets/enemy/cacty.png").convert_alpha(), (75, 75))
    cacty_mask = pygame.mask.from_surface(cacty)
    enemies['cacty'] = {
        'surface': cacty,
        'mask': cacty_mask
    }
    
    # Add more enemy types here in the future
    # Example:
    # bird = pygame.transform.scale(pygame.image.load("assets/enemy/bird.png").convert_alpha(), (75, 75))
    # bird_mask = pygame.mask.from_surface(bird)
    # enemies['bird'] = {'surface': bird, 'mask': bird_mask}
    
    return enemies

def load_board():
    """Load the board image"""
    return pygame.transform.scale(pygame.image.load("assets/board/board.png").convert_alpha(), (400, 200))