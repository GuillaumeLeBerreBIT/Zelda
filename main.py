# Loading in the neccesary modules
import pygame, sys
# Import everything from settings.py
from settings import *
# Import the Level to get access to all sprites
from level import Level

class Game:
    # The init method
    def __init__(self):
        ## BASIC SETUP
        # Initiating Pygame
        pygame.init()
        # Creating the display surface
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        # Set the caption name of screen window
        pygame.display.set_caption('Zelda')
        # Creating a clock >> FPS
        self.clock = pygame.time.Clock()
        # Creating instance from level class
        self.level = Level()
        
    
    # Run method
    def run(self):
        
        while True:
            # Event loop == check for all possile types of player input.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Checking if we are closing the game
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill('black')   # Filling screen with black color
            self.level.run()            # Run everything from Level class inside the loop >> calling run() function
            pygame.display.update()     # Updating the screen
            self.clock.tick(FPS)        # Controlling the Framerate
            
            
        
            
    
if __name__ == "__main__":  # This will check if it is our main file
    game = Game()           # Creating an instance of this game class
    game.run()              # Call the method run of this class
    
    
