import pygame
from settings import *

class UI:
    
    def __init__(self):
        # General setup
        self.display_surface = pygame.display.get_surface()  # Get a reference to the currently set display surface >> Gets the display surface from anywhere in our code
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # Bar setup             
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)    # Need to the left position, top position, width and height of the bar
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
    
    def show_bar(self, current, max_amount, bg_rect, color):
        # Draw the background bar
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)    # Use the surface to draw on, background color, Rectangle want to draw
        
        # Converting stat to pixel
        ratio = current / max_amount    # Want to have the current health of the player / max amount the player can have
        current_width = bg_rect.width * ratio # Get the max width in pixels & multiply it by the ratio >> The width the Bar for health, energy should be 
        # Adjust the background of the rectangle to match the current health/energy
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        # Draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        # Want to draw a border around the background rectangle to make it more easthetic
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect, 3)
        
    def show_exp(self, exp):
        # Want to create the experience text >> 
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        # We want to get the dimeonsions of the display surface >> Get the X and Y positions respectively from the tuple & Add some padding 
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        # Use the coordinates to place the text onto the screen
        text_rect = text_surf.get_rect(bottomright = (x, y))
    
    ### 3:31:51
    
    
        # Draw background behind the text make it more visible
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))  # Can use the inflate function to increase the pixels of the background box
        # Draw the surface based on the coordinates provided by positions through rect
        self.display_surface.blit(text_surf, text_rect)
        # Adding now a border to the background surface >> Change color and line
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
    
    def display(self, player):
        
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        
        self.show_exp(player.exp)