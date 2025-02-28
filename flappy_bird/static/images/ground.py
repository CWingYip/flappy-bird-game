import pygame
import os

# Create the ground image
def create_ground():
    # Create a surface for the ground
    ground = pygame.Surface((336, 70))  # Wider than screen to allow scrolling
    
    # Fill the ground with a base color
    ground.fill((222, 216, 149))
    
    # Draw the top border of the ground
    pygame.draw.rect(ground, (172, 166, 99), (0, 0, 336, 5))
    
    # Draw some details on the ground
    for i in range(0, 336, 24):
        # Grass tufts
        if i % 48 == 0:
            pygame.draw.rect(ground, (172, 166, 99), (i, 10, 12, 2))
        
        # Dirt patches
        if i % 72 == 0:
            pygame.draw.ellipse(ground, (202, 196, 129), (i+5, 25, 30, 15))
        
        # Small stones
        if i % 36 == 0:
            pygame.draw.circle(ground, (192, 186, 119), (i+15, 45), 3)
    
    # Save the ground image
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    pygame.image.save(ground, 'static/images/ground.png')
    return 'static/images/ground.png'

if __name__ == "__main__":
    pygame.init()
    create_ground()
    pygame.quit()