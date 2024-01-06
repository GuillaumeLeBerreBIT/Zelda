import pygame
from random import choice
from support import import_folder

class AnimationPlayer:
    
    def __init__(self):
        
        self.frames = {
            # magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            
            # attacks 
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/sparkle'),
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'thunder': import_folder('graphics/particles/thunder'),
 
            # monster deaths
            'squid': import_folder('graphics/particles/smoke_orange'),
            'raccoon': import_folder('graphics/particles/raccoon'),
            'spirit': import_folder('graphics/particles/nova'),
            'bamboo': import_folder('graphics/particles/bamboo'),
            
            # Leafs >> Going to import the images twice so get more variability >> Once in proper direction and once in reflected direction
            'leaf': (
                import_folder('graphics/particles/leaf1'),
                import_folder('graphics/particles/leaf2'),
                import_folder('graphics/particles/leaf3'),
                import_folder('graphics/particles/leaf4'),
                import_folder('graphics/particles/leaf5'),
                import_folder('graphics/particles/leaf6'),
                self.reflect_images(import_folder('graphics/particles/leaf1')),
                self.reflect_images(import_folder('graphics/particles/leaf2')),
                self.reflect_images(import_folder('graphics/particles/leaf3')),
                self.reflect_images(import_folder('graphics/particles/leaf4')),
                self.reflect_images(import_folder('graphics/particles/leaf5')),
                self.reflect_images(import_folder('graphics/particles/leaf6'))
                )
            }
    
    def reflect_images(self, frames):
        
        new_frames = []
        
        for frame in frames:
            # Her will flip only on the x-axis and not on the y-axis
            flipped_frame = pygame.transform.flip(frame, True, False)
            # Add all flipped frames to list
            new_frames.append(flipped_frame)
            
            return new_frames
        
    def create_grass_particles(self, pos, groups):
        # Pick random animation from leaf tuple, that has a bunch of lists inside 
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)
        
    def create_particles(self, animation_type, pos, groups):
        # Pick from the frames of the attack type, which can parse in here since the list has all kind of attack types
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)
        

class ParticleEffect(pygame.sprite.Sprite):
    
    def __init__(self, pos, animation_frames, groups):
        
        super().__init__(groups)
        
        # BASICS
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center = pos) 
        
    ## RUN ANIMATION ONCE AND THEN DESTROYED
    def animate(self):
        # Increasing the frame index
        self.frame_index += self.animation_speed
        # Once the animation index is byond then frame then kill the sprite 
        if self.frame_index >= len(self.frames):
            self.kill()
        # If still inside the list >> Picking one image from the list 
        else:
            self.image = self.frames[int(self.frame_index)]
            
    def update(self):
        
        self.animate()