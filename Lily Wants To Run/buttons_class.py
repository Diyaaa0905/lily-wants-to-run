import pygame
from music import *

#Screen Setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lily Wants To Run") #Title
clock = pygame.time.Clock() #FPS of game

class Button:
    def __init__(self, image, image_pressed, alpha, text, x, y):
        self.image_original = image.copy()
        self.image = image.copy()
        self.image_pressed = image_pressed.copy()
        self.alpha = alpha

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False
        self.was_pressed = False
        self.was_hovered = False

        self.original_width = image.get_width()
        self.original_height = image.get_height()

        self.font_size = 25.0 
        self.original_font_size = 25.0
        self.final_font_size = self.original_font_size * 0.8
        self.text = text
        
    #Animating button on screen
    def draw(self):
        screen.blit(self.image, self.rect)

        if self.clicked:
            text_color = "White"
        else:
            text_color = "Black"

        font = pygame.font.Font("assets/font/Minecraft.ttf", int(self.font_size))
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)
    
    #Checking if mouse is hovering over button
    def is_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    #Updating button transparency
    def update_alpha(self):
        target_alpha = 255 if self.is_hover() else 125

        if self.alpha < target_alpha:
            self.alpha = min(self.alpha + 10, target_alpha)
        elif self.alpha > target_alpha:
            self.alpha = max(self.alpha - 10, target_alpha)
        self.image.set_alpha(self.alpha)

    #Animating-in button
    def animate_in(self, final_width, final_height):
        if self.is_hover():
            width = self.image.get_width()
            height = self.image.get_height()
            center = self.rect.center

            if width > final_width:
                width = max(width - max(self.original_width*0.2//10, 1), final_width)
            if height > final_height:
                height = max(height - max(self.original_height*0.2//10, 1), final_height)

            current_scale = width / self.original_width
            final_font = self.original_font_size * current_scale
            if self.font_size > final_font:
                self.font_size = max(self.font_size - 0.8, final_font)

            if self.clicked:
                source_img = self.image_pressed
            else:
                source_img = self.image_original

            self.image = pygame.transform.smoothscale(source_img, (width, height))
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=center)

    #Animating-out button
    def animate_out(self, final_width, final_height):
        if not self.is_hover():
            width = self.image.get_width()
            height = self.image.get_height()
            center = self.rect.center

            if width < final_width:
                width = min(width + max(self.original_width*0.2//10, 1), final_width)
            if height < final_height:
                height = min(height + max(self.original_height*0.2//10, 1), final_height)

            current_scale = width / self.original_width
            final_font = self.original_font_size * current_scale
            if self.font_size < final_font:
                self.font_size = min(self.font_size + 0.8, final_font)

            if self.clicked:
                source_img = self.image_pressed
            else:
                source_img = self.image_original

            self.image = pygame.transform.smoothscale(source_img, (width, height))
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=center)

    #Total button animation
    def animate(self):
        if self.is_hover():
            self.animate_in(self.original_width*0.8, self.original_height*0.8)
            if not self.was_hovered:
                button_channel.play(button_hover_sound)
        else:
            self.animate_out(self.original_width, self.original_height)
        
        #Update hover state for next frame
        self.was_hovered = self.is_hover()

        self.image.set_alpha(self.alpha)
        self.draw()

    #Checking if button is clicked
    def is_clicked(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        #Check if mouse is over button & pressed
        if self.is_hover() and mouse_pressed:
            self.clicked = True
            self.was_pressed = True

        #Check if button was pressed & now mouse is released
        if self.was_pressed and not mouse_pressed:
            self.was_pressed = False
            self.clicked = False
            #Only trigger if mouse is still hovering over button when released
            if self.is_hover():
                button_channel.play(button_click_sound)
                return True
        
        #Reset clicked state if mouse is not pressed
        if not mouse_pressed:
            self.clicked = False
            
        return False
    
    #Resetting button state
    def reset(self):
        self.image = pygame.transform.scale(self.image_original, (self.original_width, self.original_height))
        self.font_size = self.original_font_size
