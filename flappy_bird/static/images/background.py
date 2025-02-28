import pygame
import os

# Create the background image
def create_background():
    # Create a surface for the background
    background = pygame.Surface((288, 512))
    
    # Fill the background with sky blue
    background.fill((135, 206, 235))
    
    # Draw some clouds
    pygame.draw.ellipse(background, (255, 255, 255), (30, 80, 60, 30))
    pygame.draw.ellipse(background, (255, 255, 255), (50, 70, 70, 40))
    pygame.draw.ellipse(background, (255, 255, 255), (90, 85, 50, 25))
    
    pygame.draw.ellipse(background, (255, 255, 255), (170, 140, 80, 40))
    pygame.draw.ellipse(background, (255, 255, 255), (200, 130, 60, 30))
    pygame.draw.ellipse(background, (255, 255, 255), (240, 145, 50, 25))
    
    pygame.draw.ellipse(background, (255, 255, 255), (50, 200, 70, 35))
    pygame.draw.ellipse(background, (255, 255, 255), (80, 190, 60, 30))
    
    # Draw some distant buildings
    pygame.draw.rect(background, (100, 100, 100), (20, 380, 30, 62))
    pygame.draw.rect(background, (80, 80, 80), (50, 360, 40, 82))
    pygame.draw.rect(background, (120, 120, 120), (90, 390, 35, 52))
    pygame.draw.rect(background, (90, 90, 90), (125, 370, 45, 72))
    pygame.draw.rect(background, (110, 110, 110), (170, 400, 25, 42))
    pygame.draw.rect(background, (70, 70, 70), (195, 350, 50, 92))
    pygame.draw.rect(background, (100, 100, 100), (245, 380, 30, 62))
    
    # Save the background image
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    pygame.image.save(background, 'static/images/background.png')
    return 'static/images/background.png'

if __name__ == "__main__":
    pygame.init()
    create_background()
    pygame.quit()