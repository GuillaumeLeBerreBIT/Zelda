import pygame
from settings import *

# This will be a sprite variable
class Tile(pygame.sprite.Sprite):
    
    # Self, Pos: so know where to place, Groups: sprite group should be part of
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        # To initiate Tile class ^^^
        super().__init__(groups)
        # Always need for a Sprite!!
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object': # Objects of 128 pixels
            # Larger tiles since are 128 px will place the topleft on the pos BUT ACTUALLY WANT TO HAVE THE BOTTOM 64 PX OF TILESIZE PLACED ON THE POSITION e.g. If 192 want to extract 128
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE)) # >> Image placed on correct Index/ Tile placed correct
        else: 
            self.rect = self.image.get_rect(topleft = pos)  # Position we get here will give to tile when create it >> Full size of entire image
        # Want to make the hitbox a bit smaller than the original image
        self.hitbox = self.rect.inflate(0, y_offset)   # It takes a rectangle and changes the size >> POS(x,y) >> Where e.g. -10 will remove 5 px top and 5 px bottom