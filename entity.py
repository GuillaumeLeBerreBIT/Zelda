import pygame

class Entity(pygame.sprite.Sprite):
    
    def __init__(self,groups):
        super().__init__(groups)
        
        # To get the index of the image in the current status list of images
        self.frame_index = 0
        self.animation_speed = 0.15 # The speed to increase the index to get the correct image
        self.direction = pygame.math.Vector2()
     
    # Need an argument for SPEED!
    def move(self,speed):
        # Magnitude is the length of the vector
        if self.direction.magnitude() != 0:                 # Checking if the vector has a length >> SINCE CAN NT NORMALIZE VECTOR LENGTH OF 0
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