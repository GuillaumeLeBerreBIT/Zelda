import pygame
# Want to init pygame because want to create a Font
pygame.init()
font = pygame.font.Font(None,30)

# Will not influence the game BUT Debugging tool
# It will give information about what is going on inside the game on the left side of the corner
# Requires 3 arguments: Info want to parse, The y POS, The X POS -- > Want to show multiple debugs can change the Y pos with 2nd argument
# Example debug('mouse!', pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[0]) -- > This will follow mouse pixelperfect

def debug(info, y = 10, x = 10):
    # This will get the display surface
    display_surface = pygame.display.get_surface()
    # To create some text 
    debug_surface = font.render(str(info), True, 'White')
    # Create a rectangle -- > Place topleft position on x,y coordinates
    debug_rect = debug_surface.get_rect(topleft = (x,y))
    # Draw a black canvas on the recangle
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    # Draw the surface on the display surface
    display_surface.blit(debug_surface, debug_rect)