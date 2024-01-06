from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

# Can put sprite in different groups && Sprite can be in multiple groups at the same time
# Depending on what group it is in, should be able to interact with its environments

# Group for sprites that will be drawn >> Only group that draws sprites == Draw on screen
# Player, Map, Enemies, Obstacles, ... == VISIBLE SPRITES
    
# Everything that will be able to collide with the player == OBSTACLE SPRITES
# Level boundary == Sprites will interact with player via collisions BUT not drawn because not visible

# VERY IMPORTANT!!! Central part of the entire game == Going to be the container contains all essential game elements
# Player, Level, Enemies aka all sprites(player, enemies, obst, ...)
# Take all sprites the game >> Set them in different groups >> Manage all efficiently hundreds of sprites
# Use different groups to give different fuinctionality to different sprites             
class Level():
    
    def __init__(self):
        
        # Draw all of game on 'self.screen'
        self.display_surface = pygame.display.get_surface() # Will get the display surface from anywhere in our code
        self.game_paused = False 
        # Sprite groups
        self.visible_sprites = YSortCameraGroup() # Change this sprite class to a custom made group
        self.obstacle_sprites = pygame.sprite.Group()       
        
        # Attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group() # All enemies will be in this group
        self.attackable_sprites = pygame.sprite.Group() # Going to spawn the weapons
        # Want to check the collisions in these groups >> Check if hit anything
        
        # Sprite setup
        self.create_map()

        # User interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        
        # Particles
        self.animation_player = AnimationPlayer()   # To run the particle effect 
        self.magic_player = MagicPlayer(self.animation_player)
    
    def create_map(self):
        # To load in all the CSV files for the location of the objects to place
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        # To load in all the graphical images 
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'object': import_folder('graphics/Objects')
        }
        #print(graphics['object'])  # Here the image name loaded in order here >> have the same index as the layout number >> Can use index to extract correct image
        #print(layouts['object'])   # Because the number here represents the ID image used to place the object in tiled
        
        # Style >> Will be the boundarys & layout will be the csv map
        for style, layout in layouts.items():
            #print(layout)
            # Enumerate == row index -- >> Y POS
            for row_index, row in enumerate(layout):
                # Need to know index >> Going to be number to multiply with tile size to get y position    
                # Iterate over the strings of each list -- >> X POS
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # Convert WP into POS
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            # If you want to see blocked border add self.visible_sprites >> Ofc do noot want to see in final results
                            Tile(pos = (x, y), groups = [self.obstacle_sprites], sprite_type = 'invinsible')    
                        
                        if style == 'grass':
                            # Take a random image from the list containing all grass images
                            random_grass_image = choice(graphics['grass'])
                            # Now here parce the surface image with the tile function >> To put the picture on the map & Adding to the obstacle sprites makes it so can not walk past it 
                            Tile(pos = (x, y), groups = [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], sprite_type = 'grass', surface = random_grass_image)
                        
                        if style == 'object':
                            # This will return a list from what we want the index
                            surf = graphics['object'][int(col)]  # WANT TO USE COLUMN GET FOR INDEXING >> TO GET THE CORRECT IMAGE
                            # Now here parce the surface image with the tile function >> To put the picture on the map & Adding to the obstacle sprites makes it so can not walk past it 
                            Tile(pos = (x, y), groups = [self.visible_sprites, self.obstacle_sprites], sprite_type = 'object', surface = surf)
                            
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(pos = (x, y), 
                                                groups = [self.visible_sprites],           
                                                obstacle_sprites = self.obstacle_sprites,
                                                create_attack = self.create_attack,         # Not calling the function want to call it inside of the player
                                                destroy_attack = self.destroy_attack,       # Want to call the destroy attack here since place it in statementwhen attack is reset
                                                create_magic = self.create_magic)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit' 
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                
                                Enemy(monster_name = monster_name, 
                                        pos = (x,y), 
                                        groups = [self.visible_sprites, self.attackable_sprites],
                                        obstacle_sprites = self.obstacle_sprites,
                                        damage_player = self.damage_player,
                                        trigger_death_particles = self.trigger_death_particles,
                                        add_exp = self.add_exp)
            #    
            #    if col == 'x':
            #        Tile(pos = (x,y), groups = [self.visible_sprites, self.obstacle_sprites])   # Add to visible groups so can see them && 
            #            # To invisible sprites = If there is any collision from plyer and obstacle sprite if collision going to influence the player from collision
            #    
            #    if col == 'p':
            #        # Want to place the player on the position P based of positions indexes extrected from (x,y)
            #        # Want to make it OO so can target it
            #        self.player = Player(pos = (x,y), 
            #                             groups = [self.visible_sprites],           # Parsing the player inside this group
            #                             obstacle_sprites = self.obstacle_sprites)  # Then we give the player this group FOR THE COLLISIONS, Player is not inside this grou^p
        #self.player = Player(pos = (2000,1430), .....) >> MOVED INSIDE ENTITY BLOCK
        
    def create_attack(self):
        self.current_attack = Weapon(self.player, 
                                     groups = [self.visible_sprites, self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        
        if style == 'heal':
            # Calling the heal method 
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites]) # No collisions so do not need any of the attack sprites
            
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        
    
    def destroy_attack(self):
        if self.current_attack: # If the self.current_attack exist then want to kill it
            self.current_attack.kill()
        self.current_attack = None
    
    def player_attack_logic(self):
        
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites: # Iterate over the list containing all the sprites in this group
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)   # Use a SPRITE to check if it collides with any sprite inside a group >> In this case not want to destroy the sprite

                if collision_sprite: # If it exists
                    # This will give the sprites that have been colliding with the weapon
                    for target_sprite in collision_sprite:
                        # Need to figure out the sprite type to do something with it
                        if target_sprite.sprite_type == 'grass':
                            
                            pos = target_sprite.rect.center # Will place the particles right on the center where the grass will be
                            offset = pygame.math.Vector2(0,75)  # Lifting up the particle effect a tiny bit 
                    
                            # Spawn in multiple leafs >> Make it nicer 
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            
                            target_sprite.kill()
                        # For the enemies want to take the health and damage into account 
                        else: 
                            target_sprite.get_damge(self.player, attack_sprite.sprite_type)
    
    # Write a function that can damage the player
    def damage_player(self, amount, attack_type):
        
        if self.player.vulnerable: # Create a timer after the player is hit so it cant attack the player multiple times in one attack
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # Spawn particles
            # Get the slash, claw, thunder, leaf attack & Get the position of the player & 
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
            
    def trigger_death_particles(self, pos, particle_type): 
        
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])
        
    def add_exp(self, amount):
        
        self.player.exp += amount
        
    def toggle_menu(self):
        
        self.game_paused = not self.game_paused
        
    def run(self):
        # ALWAYS DRAWING PAUSED OR UNPAUSED
        # Sprites want to draw from the group
        # Object from the YSortCameraGroup
        self.visible_sprites.custom_draw(self.player) # Access player and get player position & Do not need any arguments due to display surface in class  #draw(self.display_surface) # Surface we want to draw on
        # Get the information of the player to pass into the UI
        self.ui.display(self.player)
               
        if self.game_paused:    # IF THE GAME IS PAUSED
            self.upgrade.display() 
        
        else:           # IF THE GAME IS NOT PAUSED 
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

        
# This sprite group is going to function as a CAMERA & The YSort == Sort the sprites by the Y coordinate and give them some overlap
class YSortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
       
       # General setup
       super().__init__()
       
       self.display_surface = pygame.display.get_surface()  # Get a reference to the currently set display surface >> Gets the display surface from anywhere in our code
       # Player to be exactly in the middle of the screen >> Get display surface 
       self.half_width = self.display_surface.get_size()[0] // 2    # The X pos & Floor divide by 2 so get an integer
       self.half_height = self.display_surface.get_size()[1] // 2   # The Y pos & Floor divide by 2 so get an integer
       # These lines calculate the half-width and half-height of the display surface. These values are later used to determine the offset of the sprites relative to the player.
       # Create a vector == ESSENTIALLY GOING TO BE OUR CAMERA
       self.offset = pygame.math.Vector2()  # Default 0,0>> going to add to the sprite rectangle >> If positions given entire game is given an offset == Drawing elements in a different spot
       # Used to store the offset of the player sprite, ensuring that other sprites are drawn relative to the player's position
       
       # Creating the floor
       self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
       self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
       
    def custom_draw(self, player):  # It is intended to be called each frame to render the sprites in the group, considering the player's position as a reference point.
        
        # These lines calculate the offset of the player from the center of the display surface. It determines how much the rendering should be shifted to keep the player centered on the screen.
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #                    POS CEN PLAYER ON WINDOW    HALF WIDHT WINDOW
        #print(self.offset.x, player.rect.centerx, self.half_width)
       
        # Get the coordinates off the map based on, player offset
        offset_floor = self.floor_rect.topleft - self.offset
        # Blit the surface and give the offset coordinates
        self.display_surface.blit(self.floor_surface, offset_floor)
        
        
        # All need for custom draw >> Now can get all of the sprites
        #for sprite in self.sprites():    # List of the Sprites this group contains
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # sorted(LIST_TO_SORT, key = Metric going to sort all of the sprites)
            # Everytime any kind of offset >> Going to add it to our rectangle 
            offset_pos = sprite.rect.topleft - self.offset  # SUBTRACT THE SPRITE - THE OFFSET PLAYER POS && sprite.rect.topleft this positions since all objects are oriented from (0,0) from display surface
            self.display_surface.blit(sprite.image, offset_pos)
            
        # For each sprite, it calculates the position where the sprite should be drawn based on the player's offset.
            
        # By default always drawing the sprite image in the position as the sprite rectangle
        # Can give the sprite rectangle a certain kind of offset
        # When calling blit will still keep our sprite.image & now for sprite.rect going to add a vector to give a certain kind of offset
        # This vector is going to be our camera >> Going to give control where the sprites are going to be drawn 
        # Get the offset from the player and connect this to the sprite vector 
        
    def enemy_update(self,player):
        # This will return a list for all the sprites that are either enemy or player
        # First need to check if the sprite has the attribute (var) sprite_type and then checks if it is an enem attr
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        
        for enemy in enemy_sprites:
            enemy.enemy_update(player)