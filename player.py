import pygame
from settings import *
from support import *

# This will be a sprite variable
class Player(pygame.sprite.Sprite):
    
    # Self, Pos: so know where to place, Groups: sprite group should be part of, Obstacle_sprites: To know where the obstacles are (Collisions)
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        # To initiate Tile class ^^
        super().__init__(groups)
        # Always need for a Sprite!!
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()    # Will import player 
        self.rect = self.image.get_rect(topleft = pos)  # Position we get here will give to tile when create it
        self.hitbox = self.rect.inflate(0,-26)
        
        # Graphics setup
        self.import_player_assets()
        self.status = 'down'
        # To get the index of the image in the current status list of images
        self.frame_index = 0
        self.animation_speed = 0.15 # The speed to increase the index to get the correct image
        
        # Movement 
        self.direction = pygame.math.Vector2()  # The vector that is going to have x and y by default (0,0) >> Move player
        #self.speed = 5 
        # Used as timer for attacking
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        self.obstacle_sprites = obstacle_sprites

        # Weapon 
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0       
        # Want to create a list from the keys of weapon_data  for sword, lance, ... which are selected based on the weapon index
        self.weapon = list(weapon_data.keys())[self.weapon_index]   # e.g. sword
        self.can_switch_weapon = True   # Possible to switch the weapons
        self.weapon_switch_time = None   # Equivelant of the attack time
        self.switch_duration_cooldown = 200
        
        # Magic
        self.create_magic = create_magic
        self.magic_index = 0 
        #It will return the list for either fire or heal
        self.magic = list(magic_data.keys())[self.magic_index] 
        self.can_switch_magic = True    # Makes 
        self.magic_switch_time = None
        
        # Stats 
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}    # Base stats >> Use for creating the UI
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']
              
    def import_player_assets(self):
        # Path to folder containing all different animations
        character_path = 'graphics/player/'
        self.animations = {'up': [],'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': [],}
        
        # Get all the type of animations from the dictionary
        for animation in self.animations.keys():
            # Create a path to the folder containing all the images
            full_path = character_path + '/' + animation
            # Call the correct key from the dictionary to load in the images
            self.animations[animation] = import_folder(full_path)   
        
    def input(self):
        # Want to do nothing when attacking >> this will make sure image stays same untill attack done
        if not self.attacking:
            # If the key stays pressed down it will register that it is being pressed.
            # >> This makes it so when continously pressed down multiple keys can move diagonallyt constantly 
            keys_pressed = pygame.key.get_pressed()
            # If the Arrow up key pressed then move Player up  
            if keys_pressed[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'  # Change the status to the location where the player is walking
                
            # If the arrow key down is pressed >> Move down        
            elif keys_pressed[pygame.K_DOWN]:
                self.direction.y = +1
                self.status = 'down'
            # If neither pressed then player doesnt move in any of those directions
            else:
                self.direction.y = 0 
                    
            if keys_pressed[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'  
            elif keys_pressed[pygame.K_RIGHT]:
                self.direction.x = +1
                self.status = 'right'
            else: 
                self.direction.x = 0
            
            # Attack input
            if keys_pressed[pygame.K_SPACE]: # and not self.attacking: # Check if False so it does not spam attack 
                self.attacking = True 
                self.attack_time = pygame.time.get_ticks()  # This only called once
                self.create_attack()    # Here can call the attack function
                
            # Magic input
            if keys_pressed[pygame.K_LCTRL]: # and not self.attacking:
                style = list(magic_data.keys())[self.magic_index]   # Turn into a lsit so can index on it 
                strength = list(magic_data.values())[self.magic_index]["strength"]  # This returns a list of the dictionaries under the key values, can index it and specify the value to get
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)     # Here want to call the magic funtion
                
            if keys_pressed[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False  # Once the weapon switched set it ot false
                self.weapon_switch_time = pygame.time.get_ticks() # Want the time of when the attack is pressed 
                # Keep increasing the weapon index of the weapon but once hit the max set it back to index zero
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else: 
                    self.weapon_index = 0
                    
                self.weapon = list(weapon_data.keys())[self.weapon_index]   # Want to update the weapon list once the index is changed
                
                
            if keys_pressed[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False 
                self.magic_switch_time = pygame.time.get_ticks() # This is the starting time from upon calling an attack/magic
                # Keep increasing the weapon index of the weapon but once hit the max set it back to index zero
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else: 
                    self.magic_index = 0
                    
                self.magic = list(magic_data.keys())[self.magic_index]   # Want to update the weapon list once the index is changed
        
    # Need the player direction + input >> Player status == Now from [1,0] player moving to the right and Attacking False that it is not attacking          
    def get_status(self):
        # Idle status 
        if self.direction.x == 0 and self.direction.y == 0: # When not moving then idling
            if not 'idle' in self.status and not 'attack' in self.status:   # If the status does not contains the idle part add it (only once instead of continously)
                self.status = self.status + '_idle'
            # If after the attack we are not moving then we adjust it to idle  
            #if not 'idle' in self.status and 'attack' in self.status and self.attacking == False:
            #    self.status = self.status.replace('_attack', '_idle')
        
        if self.attacking:  # DO not want to move the player and attack at the same time
            self.direction.x = 0
            self.direction.y = 0
            # Add the attack commont on the status 
            if not 'attack' in self.status:   # If the status does not contains the idle part add it (only once instead of continously)
                if 'idle' in self.status:
                    # Overwrite idle
                    self.status = self.status.replace('_idle', '_attack')
                    
                else: 
                    self.status = self.status + '_attack'
        else: # When attacking is false
            if 'attack' in self.status: # Attack is in the string Need to remove it >>
                self.status = self.status.replace('_attack', '') 
            
    # Need an argument for SPEED!
    def move(self,speed):
        # Magnitude is the length of the vector
        if self.direction.magnitude() != 0:                 # Checking if the vector has a length
            self.direction = self.direction.normalize()     # Setting the length of vector to 1 (so does not matter which direction it moves)

        # Split up the method into the x and y movement >> CHANGE THE RECT TO HITBOX HERE
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')        # Checking any horizontal collisions
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')  # Checking any vertical collisions
        self.rect.center = self.hitbox.center   # Set the center of the hitbox as center of the rectangle
        
        #self.rect.center += self.direction * speed
        # Need to normalize how the player moves because diagonally moves faster!
    
    def collision(self,direction):  # Give the directions as arguments
        
        if direction == 'horizontal':   # Check the direction for collision
            # Check for all the sprites for collisions
            for sprite in self.obstacle_sprites:
                # This will tell whether there will be a collisions between obstacle and the player
                # CHECK THE HITBOX INSTEAD OF THE RECTANGLE
                if sprite.hitbox.colliderect(self.hitbox):
                    # We can predict there will always be a collision on e.g. right side if player is moving to right
                    if self.direction.x > 0:    # Moving right
                        self.hitbox.right = sprite.hitbox.left  # If player moving to right and colliding but overlapping >> Want to move right side of player to left side of the obstacle weve been colliding with so it looks player always on that side and is not overlapping

                    if self.direction.x < 0: # Moving left
                        self.hitbox.left = sprite.hitbox.right  # Place the left side of the player against the right side of the obstacle
                    
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                
                if sprite.hitbox.colliderect(self.hitbox):
                    
                    if self.direction.y < 0: # Moving up
                        self.hitbox.top = sprite.hitbox.bottom  # Will place the top of the player under the bottom of the sprite
                    if self.direction.y > 0: # Moving down
                        self.hitbox.bottom = sprite.hitbox.top # Will place the bottom of the player at the top of the obstacle sprite
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()  # This will be run multiple times
        # Check for attack
        if self.attacking:
            # If the time of attack has passed more then 400 ticks then set to False so can attack again
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()   # Want to destroy the sprite once the attack animation is done
                
        if not self.can_switch_weapon:  #If u can not switch the weapon 
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown: # Check current time - the time of weapon swithc and of bigger then can switch again
                self.can_switch_weapon = True
        
        if not self.can_switch_magic:  #If u can not switch the weapon 
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown: # Check current time - the time of weapon swithc and of bigger then can switch again
                self.can_switch_magic = True
   
    def animate(self):
        # Use the status the get the correct key of images to represent
        animation = self.animations[self.status]
        
        # Loop over the frame index
        self.frame_index += self.animation_speed
        # If the index is higher then the list of images >> Reset the index to 0
        if self.frame_index >= len(animation):
            self.frame_index  = 0  
        # Load in the new images each time again >> Do not need to laod in image since already done by the function
        self.image = animation[int(self.frame_index)]
        # Different images of the player have different dimensions >> Need teo update the rectangle to have the correct pixels
        self.rect = self.image.get_rect(center = self.hitbox.center)
            
    def update(self):
        # Update the input keys each time
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed) # Defined above
        
        
# Possible that 2 sprites collide either on the bottom of a sprite or on the left (side) of a sprite
# If the sprite collides on the right it might teleport it below the other sprite >> Might break game
# FIX -- > Apply each direction individually 
# Apply horizontal movements >> check collisions (x) >> If collision going to move the player to the point of that collision
# Then work on Vertical movements and collisions then there is no problem