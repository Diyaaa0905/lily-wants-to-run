"""
Base level configuration class
All individual levels inherit from this class
"""
from config import HEIGHT

class LevelConfig:
    def __init__(self):
        # Level metadata
        self.level_number = 1
        
        # Flower positions (5 different heights)
        self.flower_positions = [
            (HEIGHT - 150 - 20),   # Position 0 - lowest
            (HEIGHT - 150 - 60),   # Position 1
            (HEIGHT - 150 - 100),  # Position 2
            (HEIGHT - 150 - 140),  # Position 3
            (HEIGHT - 150 - 180)   # Position 4 - highest
        ]
        
        # Flower configuration
        self.flower_sequence = []        # Which height each flower appears at (indices into flower_positions)
        self.flower_spawn_timer = []     # Frames to wait before spawning each flower
        
        # Enemy types available
        self.enemy_types = ['cacty']
        
        # Enemy configuration
        self.enemy_sequence = []         # Which enemy type spawns at each point
        self.enemy_spawn_timer = []      # Frames to wait before spawning each enemy
        self.enemy_spawn_y = []          # Y-position for each enemy spawn
        
        # Visual theme (RGB tuples)
        self.background_color = (144, 209, 196)  # Sky color
        self.ground_color = (158, 96, 35)        # Ground color
        self.grass_color = (101, 173, 68)        # Grass strip color
    
    def get_flower_count(self):
        """Returns total number of flowers in this level"""
        return len(self.flower_sequence)
    
    def get_enemy_count(self):
        """Returns total number of enemies in this level"""
        return len(self.enemy_sequence)
    
    def get_flower_y_position(self, index):
        """Get the Y position for a flower based on its sequence index"""
        if index < len(self.flower_sequence):
            position_index = self.flower_sequence[index]
            return self.flower_positions[position_index]
        return self.flower_positions[0]  # Default to lowest position
    
    def reset_spawn_timers(self):
        """Return a fresh copy of the spawn timers"""
        return {
            'flower': list(self.flower_spawn_timer),
            'enemy': list(self.enemy_spawn_timer)
        }