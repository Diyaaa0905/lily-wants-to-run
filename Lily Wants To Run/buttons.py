"""
Button instances for the game
"""
from buttons_class import Button
from config import WIDTH, HEIGHT

def create_all_buttons(button_images):
    """Create and return all button instances"""
    button_img = button_images['button']
    small_button_img = button_images['small_button']
    smaller_button_img = button_images['smaller_button']
    volume_button_img = button_images['volume_button']
    pause_button_img = button_images['pause_button']
    
    buttons = {}
    
    # HOME buttons
    buttons['start'] = Button(button_img[0], button_img[1], 255, "START", 
                              WIDTH//2 - button_img[0].get_width()//2, 250)
    buttons['exit'] = Button(button_img[0], button_img[1], 255, "EXIT", 
                             WIDTH//2 - button_img[0].get_width()//2, HEIGHT-175)
    buttons['how_start'] = Button(small_button_img[0], small_button_img[1], 255, "?", 
                                  WIDTH//2 - 75, 400)
    buttons['volume_start'] = Button(volume_button_img[0], volume_button_img[1], 255, " ", 
                                     WIDTH//2 + 25, 400)
    buttons['x0'] = Button(small_button_img[0], small_button_img[1], 255, "X", 
                           WIDTH//2+200-50-17, 100+17)
    
    # Arrow buttons
    buttons['left_arrow'] = [
        Button(smaller_button_img[0], smaller_button_img[1], 255, "<", 293, 172),
        Button(smaller_button_img[0], smaller_button_img[1], 255, "<", 293, 234)
    ]
    buttons['right_arrow'] = [
        Button(smaller_button_img[0], smaller_button_img[1], 255, ">", 528, 172),
        Button(smaller_button_img[0], smaller_button_img[1], 255, ">", 528, 234)
    ]
    
    # LEVEL COMPLETE buttons
    buttons['back'] = Button(button_img[0], button_img[1], 255, "HOME", 
                            WIDTH//2 - 200+10, 100+20+40+40+30)
    buttons['next'] = Button(button_img[0], button_img[1], 255, "NEXT", 
                            WIDTH//2 + 200-10-150, 100+20+40+40+30)
    
    # GAME OVER buttons
    buttons['restart'] = Button(button_img[0], button_img[1], 255, "RESTART", 
                               WIDTH//2 - button_img[0].get_width()//2 - 100, 150+120)
    buttons['esc'] = Button(button_img[0], button_img[1], 255, "HOME", 
                           WIDTH//2 - button_img[0].get_width()//2 + 100, 150+120)
    
    # PAUSE SCREEN buttons
    buttons['pause'] = Button(pause_button_img[0], pause_button_img[1], 125, " ", 
                             WIDTH - pause_button_img[0].get_width() - 10, 10)
    buttons['unpause'] = Button(button_img[0], button_img[1], 255, "UNPAUSE", 
                               WIDTH//2 - 160, HEIGHT//2)
    buttons['home_from_pause'] = Button(button_img[0], button_img[1], 255, "HOME", 
                                       WIDTH//2 + 10, HEIGHT//2)
    
    return buttons