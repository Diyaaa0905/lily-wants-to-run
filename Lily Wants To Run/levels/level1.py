from levels.level_config import LevelConfig
from config import HEIGHT

class Level1(LevelConfig):
    def __init__(self):
        super().__init__()
        
        # Level metadata
        self.level_number = 1
        
        # Flower configuration (18 flowers)
        self.flower_sequence = [0, 0, 2, 3, 0, 3, 4, 3, 1, 2, 1, 4, 3, 2, 4, 2, 0, 0]
        
        # Flower spawn timers (in frames at 60 FPS)
        self.flower_spawn_timer = [
            0.5*60, 1*60, 0.5*60, 1.5*60, 3*60, 2*60, 1*60, 2*60, 1.3*60, 2*60,
            2.2*60, 1.5*60, 1*60, 1*60, 0.5*60, 2*60, 1*60, 0.5*60
        ]
        
        # Enemy configuration (10 enemies - all cacty)
        self.enemy_sequence = ['cacty', 'cacty', 'cacty', 'cacty', 'cacty', 
                               'cacty', 'cacty', 'cacty', 'cacty', 'cacty']
        
        # Enemy spawn timers (in frames at 60 FPS)
        self.enemy_spawn_timer = [3*60, 2*60, 2*60, 4*60, 2*60, 2*60, 1*60, 3*60, 4*60, 3*60]
        
        # Enemy spawn Y positions (all at ground level)
        self.enemy_spawn_y = [
            (HEIGHT-150), (HEIGHT-150), (HEIGHT-150), (HEIGHT-150), (HEIGHT-150),
            (HEIGHT-150), (HEIGHT-150), (HEIGHT-150), (HEIGHT-150), (HEIGHT-150)
        ]
        
        # Visual theme - Original colors
        self.background_color = (144, 209, 196)  # Teal sky
        self.ground_color = (158, 96, 35)        # Brown ground
        self.grass_color = (101, 173, 68)        # Green grass