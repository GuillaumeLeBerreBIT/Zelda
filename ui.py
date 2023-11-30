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
        
        # Convert weapon dictionary
        self.weapon_graphics = []
        # Iterate over the values in the dictionary which is esantially another dictionary
        for weapon in weapon_data.values(): 
            # Only want the key for path to the weapon index
            path = weapon['graphic']
            # Convert to pygame image
            weapon = pygame.image.load(path).convert_alpha()
            # Append to the graphic path to the list of weapons 
            self.weapon_graphics.append(weapon)

        # Convert weapon dictionary
        self.magic_graphics = []
        # Iterate over the values in the dictionary which is esantially another dictionary
        for magic in magic_data.values(): 
            # Only want the key for path to the weapon index
            path = magic['graphic']
            print(path)
            # Convert to pygame image
            magic = pygame.image.load(path).convert_alpha()
            # Append to the graphic path to the list of weapons 
            self.magic_graphics.append(magic)
    
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
    
        # Draw background behind the text make it more visible
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))  # Can use the inflate function to increase the pixels of the background box
        # Draw the surface based on the coordinates provided by positions through rect
        self.display_surface.blit(text_surf, text_rect)
        # Adding now a border to the background surface >> Change color and line
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
    
    def selection_box(self, left, top, has_switched):
        # Create a rectangel of the  rectenagle using >> POS LEFT, POS TOP, WIDTH, HEIGHT
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        # Create the background of the box which will be used to view the used weapon on
        pygame.draw.rect(self.display_surface, UI_BG_COLOR , bg_rect)
        if has_switched: 
            # Create a frame around the box
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE , bg_rect, 3)
        else:
            # Create a frame around the box
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR , bg_rect, 3) 
            
        # Give the background rectangle it
        return bg_rect
    
    def weapon_overlay(self, weapon_index, has_switched):
        # Draw the background to display the weapon on
        bg_rect = self.selection_box(10, 630, has_switched)     # Weapon
        # Select the image for the weapon based on the path of graphics
        weapon_surf = self.weapon_graphics[weapon_index]
        # Get the position of the background rectangle to place the weapon surface above >> Center Weapon on Center of BG
        weapon_rect  = weapon_surf.get_rect(center = bg_rect.center )
        # Want to place the surface of the rectangle inside the background box >> Need to return it in previous function
        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def magic_overlay(self, magic_index, has_switched):
        # Drawing the background to draw the magic on
        bg_rect_magic = self.selection_box(80, 635, has_switched)
        # Create a surface of the graphic image
        magic_surf = self.magic_graphics[magic_index]   # Already laoded the image previously >> Directly call from the list
        # Create a rectangle of the surface >> Which has the same center of the background drawn
        magic_rect = magic_surf.get_rect(center = bg_rect_magic.center)
        
        self.display_surface.blit(magic_surf, magic_rect)
        
    def display(self, player):
        
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        
        self.show_exp(player.exp)
        
        # By default is true but only want to box when it is not true since the logic is reversed in the function
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)     # Weapon
        self.magic_overlay(player.magic_index, not player.can_switch_magic)     # Magic