"""
Game state management
"""
from config import COUNTDOWN_TIMER_FRAMES

class GameState:
    def __init__(self):
        # Game mode flags
        self.game_home = True
        self.game_active = False
        self.game_over = False
        self.game_paused = False
        
        # Level management
        self.current_level_number = 1
        self.current_level = None
        
        # Game variables
        self.timer = 0
        self.start_state = 0
        self.tip_state = 0
        self.score = 0
        self.high = 0
        self.loop = 0
        self.loop2 = 0
        self.loop3 = 0
        self.gravity = 0
        self.increment = 0
        self.flowers_collected = 0
        
        # Animation variables
        self.flower_loop = 0
        self.frame = 0
        self.sparkle_counter = 0
        self.portal_loop = 0
        
        # Level completion variables
        self.move = 0
        self.end_scene = 0
        self.level_complete_alpha = 0
        self.enter_portal = 255
        self.level_complete = False
        self.bounce_start_time = None
        self.score_counter = 0
        self.score_stage = 0
        self.stage_timer = 0
        self.score_sound_playing = False
        
        # Pause variables
        self.countdown_start = False
        self.pause_start_time = 0
        self.countdown_timer = COUNTDOWN_TIMER_FRAMES
        self.countdown_sound_played = False
        
        # Collections
        self.floating_scores = []
        self.flower_index = 0
        self.current_flowers = []
        self.current_enemies = []
        
        # Spawn timers (will be set from level config)
        self.enemy_spawn_timer = []
        self.flower_spawn_timer = []
        
        # Portal
        self.portal_speed = 5
        
        # Music state
        self.start_music_played = False
        self.loop_music_playing = False
        self.waiting_for_loop_to_end = False
        self.gameplay_music_started = False
        self.gamewin_music_played = False
        self.level_up_music_played = False
        self.loop_cycle_end_time = 0
    
    def load_level(self, level_config):
        """Set up the game state for a specific level"""
        self.current_level = level_config
        
        # Get fresh timers
        timers = self.current_level.reset_spawn_timers()
        self.flower_spawn_timer = timers['flower']
        self.enemy_spawn_timer = timers['enemy']
        
        # Reset tracking variables
        self.flower_index = 0
        self.current_flowers = []
        self.current_enemies = []
        
        # Set level complete flags
        self.level_complete = False
        self.level_complete_alpha = 0
        
    def reset_game(self, keep_level=False):
        """Reset all game variables to initial state"""
        self.timer = 0
        self.start_state = 0
        self.tip_state = 0
        self.score = 0
        self.loop = 0
        self.loop2 = 0
        self.loop3 = 0
        self.gravity = 0
        self.increment = 0
        self.flowers_collected = 0
        self.countdown_start = False
        self.pause_start_time = 0
        self.countdown_timer = COUNTDOWN_TIMER_FRAMES
        
        self.flower_loop = 0
        self.frame = 0
        self.sparkle_counter = 0
        self.portal_loop = 0
        
        self.bounce_start_time = None
        self.score_counter = 0
        self.score_stage = 0
        self.stage_timer = 0
        self.score_sound_playing = False
        self.move = 0
        self.end_scene = 0
        self.level_complete_alpha = 0
        self.enter_portal = 255
        self.level_complete = False
        
        self.floating_scores.clear()
        self.flower_index = 0
        self.current_flowers.clear()
        self.current_enemies.clear()
        
        # Reset level timers if level is loaded
        if self.current_level and keep_level:
            timers = self.current_level.reset_spawn_timers()
            self.enemy_spawn_timer = timers['enemy']
            self.flower_spawn_timer = timers['flower']
        else:
            self.enemy_spawn_timer = []
            self.flower_spawn_timer = []
        
        self.portal_speed = 5
        
        self.start_music_played = False
        self.loop_music_playing = False
        self.waiting_for_loop_to_end = False
        self.gameplay_music_started = False
        self.gamewin_music_played = False
        self.countdown_sound_played = False
        self.level_up_music_played = False
        self.loop_cycle_end_time = 0
    
    def next_level(self):
        """Move to next level"""
        self.current_level_number += 1
    
    def reset_to_level_1(self):
        """Reset to level 1"""
        self.current_level_number = 1