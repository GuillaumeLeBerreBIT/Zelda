import pygame
from settings import *

class UI:
    
    def __init__(self):
        # General setup
        self.display_surface = pygame.display.get_surface()  # Get a reference to the currently set display surface >> Gets the display surface from anywhere in our code
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # Bar setup
        
    def display(self, player):
        pass