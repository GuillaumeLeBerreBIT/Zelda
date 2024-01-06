import pygame
from settings import *

class Upgrade:
    
    def __init__(self,player):
        
        # Geneal setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)  # The length of the dictionary containing the player stats
        self.attribute_names = list(player.stats.keys())    # Get the attribute names of the player character
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # Item creation
        self.height = self.display_surface.get_size()[1] * 0.8  # Here only take the Y length and lose about 20 % of the screen 
        self.width = self.display_surface.get_size()[0] // 6 # Attribute nr + 1 >> Will have 5 elements and the 6 one will serve as padding in between the other 5
        self.create_items()     # Need to call the function once
        
        # Selection system
        self.selection_index = 0
        self.selection_time = None  # For moving it going to need a timer
        self.can_move = True
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.can_move:
            
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            
            elif keys[pygame.K_LEFT]and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            
            # Going to be the select button
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)
        
    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.selection_time >= 300:   # Set to 300 miliseconds
                self.can_move = True
                
    def create_items(self):
        # Want to store all items in a list
        self.item_list = []
        
        for index, item in enumerate(range(self.attribute_nr)):
            # Horizontal position
            full_width = self.display_surface.get_size()[0] 
            increment = full_width // self.attribute_nr     # Distance from the left to get the left side from each item >> Split the window in 5 different parts
            # (This is to place each item box on certain length based on the item) + (This way offsetting item litle bit from the left)
            left = (item * increment) + (increment - self.width) // 2
            
            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1  # Have the top which is 10 % of the top of the window
            # Create the object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)
                
    def display(self):
        
        self.input()
        self.selection_cooldown()
        
        for index, item in enumerate(self.item_list):
            
            # Get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index] # Those values dont change so get them at the top 
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)
        
# Each one will represent a box can use to upgrade
class Item: 
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index 
        self.font = font
    
    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        
        # Title
        title_surf = self.font.render(name, False, color)
        #Set the middle of the text on the middle of the surface
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20)) # Add 20 px offset in Y direction)
        # Cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0,-20))
        
        # Draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
        
    def display_bar(self, surface, value, max_value, selected):
        
        # Drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        
        # Bar setup
        full_height = bottom[1] - top[1]    # Bottom is the higher number so thats why substracting like that
        relative_number = (value / max_value) * full_height  # Set the bar at a third of the total height ~ 0.3 & multiply with the full height to turn into pixel mesurement
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)  # Bottom[1] is the fullest bottom and rel num is how much gap will be from the bottom
        
        # Draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)
    
    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        
        if player.exp >= player.upgrade_cost[upgrade_attribute] \
            and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4
        # If the stats exceed the maximum amount of stats then make sure the stats are set to maximum
        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute]  = player.max_stats[upgrade_attribute]
    
    def display(self, surface, selection_num, name, value, max_value, cost):    # This is the information want to draw
        if self.index == selection_num: 
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        
        self.display_names(surface, name, cost, self.index == selection_num)    #Parsing in here to get a true or false argument
        self.display_bar(surface, value, max_value, self.index == selection_num)