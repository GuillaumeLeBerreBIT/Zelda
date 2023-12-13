from typing import Any
import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):    # Give the Entity class so do not need to rewrite 'move and 'collision
    
    def __init__(self, monster_name, pos,  groups, obstacle_sprites):
        # General setup
        super().__init__(groups)
        # To use in IF statements to get the enemy from all sprite objects
        self.sprite_type = 'enemy'  # React differently If player attacks enemy want to reduce health or kill enemy when healths go below zero
        
        # Graphics setup
        self.import_graphics(monster_name)  # Want to get all the graphics 
        self.status = 'idle'
        # Return one status from the monster and select only one image from the list returned using the frame_index from Entity class
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # Movement
        self.rect = self.image.get_rect(topleft = pos)
        # We are moving the hitbox and not rectangle so going to need the hitbox
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        
        # Stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resitance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_radius']
        
        # Player interaction
        self.can_attack  = True
        self.attack_time = None
        self.attack_cooldown_time =  400
                
    def import_graphics(self, name):
        # All kind of animation states
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
        
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)   # To acces the folder of the monster and the subfolder to get all the animations of the monster >> returns a surface list of the graphics
    
    def get_player_distance_direction(self,player):
        # Converting the center of our enemy into a vector
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        # Want to get the distance between two vectors
        # Each have their own seperate vector >> Goes from topleft window to respectively player and enemy >> When subtracting get the vector from player to enemy
        # Returns another vector that gives the realtion between the two vectors >>
        distance = (player_vec - enemy_vec).magnitude() # This returns the vector into a distance
        
        if distance > 0:
            # If multiply by speed would be way to large and move beyond player >> Reduce length from this vector to 1 >> Multiply then by the speed
            direction = (player_vec - enemy_vec).normalize()
        else: 
            # If enemy is righht on top of the player >> Do not move it at all
            direction = pygame.math.Vector2()
            
        return (distance, direction)
    
    def get_status(self, player):
        
        distance = self.get_player_distance_direction(player)[0]
        # Only want to start attacking when the mosnter is in the attack radius
        if distance <= self.attack_radius and self.can_attack == True:
            # Want to reset the animation once we switch to different animations
            if self.status != 'attack':
                self.frame_index = 0
                
            self.status = 'attack'
        # Want to start moving towards player of distance is smaller then notice radius
        elif distance <= self.notice_radius:
            self.status = 'move'
        # If outside any of the ranges just idle
        else: 
            self.status = 'idle'
    
    def actions(self, player):
        
        if self.status == 'attack':
            # Get the time from when the attack has happend
            self.attack_time = pygame.time.get_ticks()
            
        elif self.status == 'move':   
            # Want the enemy move to the player once the player is getting closer
            self.direction = self.get_player_distance_direction(player)[1]
        else: 
            self.direction = pygame.math.Vector2()  # This will ensure if the player moves outside the circle >> Then the monster will stop moving
                
    def animate(self):
        # The animation list
        animation = self.animations[self.status]
        # Loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.animations[self.status]):
            # Monster only stops being able to attack after the attack animation > Only attack once
            if self.status == 'attack':
                # Once have attacked once set the animation on False
                self.can_attack = False
            
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        # Loading the rectangle in the center of the hitbox
        self.rect = self.image.get_rect(center = self.hitbox.center)    # MOVING HITBOX NOT RECTANGLE
        
    def cooldown(self):
        # Only want to check the timer if this one is wrong
        if not self.can_attack:
            # Get current time
            current_time = pygame.time.get_ticks()
            
            if current_time - self.attack_time >= self.attack_cooldown_time:
                self.can_attack = True
    
    def get_damge(self, player, attack_type):
        
        if attack_type == 'weapon':
            self.health -= player.get_full_weapon_damage()
        else:
            pass
            # Magic damage
        
    def update(self):
        
        self.move(self.speed)
        self.cooldown()
        self.animate()
    
    def enemy_update(self, player):
        self.get_status(player = player)
        self.actions(player)