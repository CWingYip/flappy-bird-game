import pygame
import os

# Create the pipe sprite
def create_pipe_sprite():
    # Create a surface for the pipe
    pipe = pygame.Surface((52, 320), pygame.SRCALPHA)
    
    # Draw the pipe (a green pipe with a lip at the end)
    # Main pipe body
    pygame.draw.rect(pipe, (80, 180, 80), (0, 0, 52, 320))
    
    # Pipe lip (top)
    pygame.draw.rect(pipe, (60, 160, 60), (0, 0, 52, 20))
    pygame.draw.rect(pipe, (60, 160, 60), (-5, 20, 62, 10))
    
    # Pipe highlights (to give it some depth)
    pygame.draw.line(pipe, (100, 200, 100), (5, 30), (5, 320), 2)
    pygame.draw.line(pipe, (100, 200, 100), (15, 30), (15, 320), 2)
    pygame.draw.line(pipe, (60, 140, 60), (47, 30), (47, 320), 2)
    pygame.draw.line(pipe, (60, 140, 60), (37, 30), (37, 320), 2)
    
    # Save the pipe sprite
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    
    pygame.image.save(pipe, 'static/images/pipe.png')
    return 'static/images/pipe.png'

if __name__ == "__main__":
    pygame.init()
    create_pipe_sprite()
    pygame.quit()