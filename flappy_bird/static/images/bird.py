import pygame
import os

# Create the bird sprite
def create_bird_sprite():
    # Create a surface for the bird
    bird = pygame.Surface((34, 24), pygame.SRCALPHA)
    
    # Draw the bird (a simple yellow bird with an eye and beak)
    # Body
    pygame.draw.ellipse(bird, (255, 255, 0), (0, 0, 34, 24))  # Yellow body
    
    # Eye
    pygame.draw.circle(bird, (255, 255, 255), (25, 10), 5)  # White eye
    pygame.draw.circle(bird, (0, 0, 0), (25, 10), 2)  # Black pupil
    
    # Beak
    pygame.draw.polygon(bird, (255, 165, 0), [(34, 12), (30, 8), (30, 16)])  # Orange beak
    
    # Wing
    pygame.draw.ellipse(bird, (220, 220, 0), (5, 14, 15, 8))  # Wing
    
    # Save the bird sprite
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    pygame.image.save(bird, 'static/images/bird.png')
    return 'static/images/bird.png'

if __name__ == "__main__":
    pygame.init()
    create_bird_sprite()
    pygame.quit()