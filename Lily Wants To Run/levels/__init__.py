"""
Level system initialization
"""
from levels.level1 import Level1
#from levels.level2 import Level2
#from levels.level3 import Level3

# Add all levels to this list in order
LEVELS = [Level1]

def get_level(level_number):
    """Get level configuration by number (1-indexed)"""
    if 1 <= level_number <= len(LEVELS):
        return LEVELS[level_number - 1]()
    return None

def get_total_levels():
    """Get total number of levels"""
    return len(LEVELS)