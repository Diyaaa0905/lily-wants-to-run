import pygame
from buttons_class import Button

#Screen sizes
WIDTH, HEIGHT = 800, 500

#Button Images
button_img = [pygame.transform.scale(pygame.image.load("assets/buttons/button.png").convert_alpha(), (150,50)),
              pygame.transform.scale(pygame.image.load("assets/buttons/button-press.png").convert_alpha(), (150,50))]
small_button_img = [pygame.transform.scale(pygame.image.load("assets/buttons/small-button.png").convert_alpha(), (50,50)),
              pygame.transform.scale(pygame.image.load("assets/buttons/small-button-press.png").convert_alpha(), (50,50))]
smaller_button_img = [pygame.transform.scale(pygame.image.load("assets/buttons/small-button.png").convert_alpha(), (30,30)),
              pygame.transform.scale(pygame.image.load("assets/buttons/small-button-press.png").convert_alpha(), (30,30))]
volume_button_img = [pygame.transform.scale(pygame.image.load("assets/buttons/volume-button.png").convert_alpha(), (50,50)), 
                     pygame.transform.scale(pygame.image.load("assets/buttons/volume-button-press.png").convert_alpha(), (50,50))]
pause_button_img = [pygame.transform.scale(pygame.image.load("assets/buttons/pause-button.png").convert_alpha(), (50,50)), 
                    pygame.transform.scale(pygame.image.load("assets/buttons/pause-button-press.png").convert_alpha(), (50,50))]
bg_icon_img = pygame.transform.scale(pygame.image.load("assets/board/bg-icon.png").convert_alpha(), (40,40))
sfx_icon_img = pygame.transform.scale(pygame.image.load("assets/board/sfx-icon.png").convert_alpha(), (40,40))

#Buttons [HOME]
start_button = Button(button_img[0], button_img[1], 255, "START", WIDTH//2 - button_img[0].get_width()//2, 250)
exit_button = Button(button_img[0], button_img[1], 255, "EXIT", WIDTH//2 - button_img[0].get_width()//2, (HEIGHT-175))
how_start_button = Button(small_button_img[0], small_button_img[1], 255, "?", WIDTH//2 - 75, 400)
volume_start_button = Button(volume_button_img[0], volume_button_img[1], 255, " ", WIDTH//2 + 25, 400)

x0_button = Button(small_button_img[0], small_button_img[1], 255, "X", WIDTH//2+200-50-17, 100+17)
left_arrow_button = [Button(smaller_button_img[0], smaller_button_img[1], 255, "<", 293, 172),
                     Button(smaller_button_img[0], smaller_button_img[1], 255, "<", 293, 234),]
right_arrow_button = [Button(smaller_button_img[0], smaller_button_img[1], 255, ">", 528, 172),
                      Button(smaller_button_img[0], smaller_button_img[1], 255, ">", 528, 234)]
                     
#Buttons [LEVEL COMPLETE]
back_button = Button(button_img[0], button_img[1], 255, "HOME", WIDTH//2 - 200+10, 100+20+40+40+30)
next_button = Button(button_img[0], button_img[1], 255, "NEXT", WIDTH//2 + 200-10-150, 100+20+40+40+30)

#Buttons [GAME OVER]
restart_button = Button(button_img[0], button_img[1], 255, "RESTART", WIDTH//2 - button_img[0].get_width()//2 - 100, 150+120)
esc_button = Button(button_img[0], button_img[1], 255, "HOME", WIDTH//2 - button_img[0].get_width()//2 + 100, 150+120)

#Buttons [PAUSE SCREEN]
pause_button = Button(pause_button_img[0], pause_button_img[1], 125, " ", WIDTH - pause_button_img[0].get_width() - 10, 10)
unpause_button = Button(button_img[0], button_img[1], 255, "UNPAUSE", WIDTH//2 - 160, HEIGHT//2)
home_from_pause_button = Button(button_img[0], button_img[1], 255, "HOME", WIDTH//2 + 10, HEIGHT//2)
