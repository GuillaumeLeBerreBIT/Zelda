from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    
    with open(path, 'r') as level_map:
        # Using the csv reader to read the csv file
        layout = reader(level_map, delimiter = ',')
        
        # Print each row out from list of layout
        for row in layout:  # -1 == / & 395 == Restraint blocks where the player can not walk on 
            
            terrain_map.append(list(row)) # Append each row to a seperate lsit && make sure it is a list

        return terrain_map  # Get a lsit that contains a whole bunch of lsit that give the layout of the map 

def import_folder(path):
    # Want to return a full surface list 
    surface_list = []
    
    # Since do not care about the first parts returned from the list/tuple >> Only images are interesting
    for _, __, img_files in walk(path):
        # Iterate over all the images
        for image in img_files:
            
            # Concat the full path
            full_path = path + '/' + image      
            # Creating the image surface 
            image_surf = pygame.image.load(full_path).convert_alpha()
            # Append all the grass blocks in a list for all surfaces
            surface_list.append(image_surf)
    
    return surface_list # Need to return the list otherwise will not be able to get the objects

#print(import_folder('graphics/grass')) # ('graphics/grass', [], ['grass_1.png', 'grass_2.png', 'grass_3.png']) > Folder path + List of folders + LIST OF IMAGES OF FILES INSIDE FOLDER