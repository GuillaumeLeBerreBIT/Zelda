import pygame
from debug import *

class Weapon(pygame.sprite.Sprite):
    
    def __init__(self, player, groups):
        super().__init__(groups)
        
        self.sprite_type = 'weapon' # Now can use it to check collisions for specific weapons only
        # Want to get the direction either Up, Down, Left? Right and if Idle is present will be removed
        direction = player.status.split('_')[0]
        
        # Graphics
        # Get the full path to the folder using the weapon it gets from index and direction the player is facing 
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        # Placement
        if direction == 'right':
            # If player is walking towards the right want to, place it on the rightside of the player and the weapon with leftside on player & Add an offset to the image
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            # Set the weapon rightside on the left side of the player
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            # Set the weapon rightside on the left side of the player
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            # Set the weapon rightside on the left side of the player
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
        
        
        