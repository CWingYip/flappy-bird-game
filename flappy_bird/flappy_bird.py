import pygame
import random
import base64
import io
import os
from flask import Flask, render_template, request, jsonify

# Initialize pygame
pygame.init()

# Game constants
WIDTH = 288
HEIGHT = 512
GRAVITY = 0.25
BIRD_JUMP = -5
PIPE_GAP = 100
PIPE_FREQUENCY = 1500  # milliseconds
PIPE_SPEED = 2
FLOOR_HEIGHT = 70
GROUND_SCROLL = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
bird_y = HEIGHT // 2
bird_velocity = 0
score = 0
game_over = False
last_pipe = pygame.time.get_ticks() - PIPE_FREQUENCY
pipes = []
game_started = False

# Set up a display (required for image loading)
pygame.display.set_mode((1, 1), pygame.NOFRAME)

# Create game surface
screen = pygame.Surface((WIDTH, HEIGHT))

# Load images
# Check if images exist, if not create them
if not os.path.exists('static/images/bird.png'):
    from static.images.bird import create_bird_sprite
    create_bird_sprite()

if not os.path.exists('static/images/pipe.png'):
    from static.images.pipe import create_pipe_sprite
    create_pipe_sprite()

if not os.path.exists('static/images/background.png'):
    from static.images.background import create_background
    create_background()

if not os.path.exists('static/images/ground.png'):
    from static.images.ground import create_ground
    create_ground()

# Load the images
bird_img = pygame.image.load('static/images/bird.png').convert_alpha()
pipe_img = pygame.image.load('static/images/pipe.png').convert_alpha()
bg_img = pygame.image.load('static/images/background.png').convert()
ground_img = pygame.image.load('static/images/ground.png').convert()

# Bird properties
bird_width = bird_img.get_width()
bird_height = bird_img.get_height()
bird_rect = pygame.Rect(50, bird_y, bird_width, bird_height)

# Create Flask app
app = Flask(__name__)

def reset_game():
    global bird_y, bird_velocity, score, game_over, last_pipe, pipes, game_started, GROUND_SCROLL
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    game_over = False
    last_pipe = pygame.time.get_ticks() - PIPE_FREQUENCY
    pipes = []
    game_started = False
    bird_rect.y = bird_y
    GROUND_SCROLL = 0

def draw_bird():
    global bird_rect
    bird_rect = pygame.Rect(50, bird_y, bird_width, bird_height)
    screen.blit(bird_img, (50, bird_y))

def draw_pipes():
    for pipe in pipes:
        # Draw top pipe (flipped)
        pipe_top = pygame.transform.flip(pipe_img, False, True)
        pipe_top = pygame.transform.scale(pipe_top, (pipe[0].width, pipe[0].height))
        screen.blit(pipe_top, pipe[0])
        
        # Draw bottom pipe
        pipe_bottom = pygame.transform.scale(pipe_img, (pipe[1].width, pipe[1].height))
        screen.blit(pipe_bottom, pipe[1])

def draw_floor():
    global GROUND_SCROLL
    # Draw scrolling ground
    screen.blit(ground_img, (GROUND_SCROLL, HEIGHT - FLOOR_HEIGHT))
    screen.blit(ground_img, (GROUND_SCROLL + ground_img.get_width(), HEIGHT - FLOOR_HEIGHT))
    
    if game_started and not game_over:
        GROUND_SCROLL -= PIPE_SPEED
        if abs(GROUND_SCROLL) > ground_img.get_width():
            GROUND_SCROLL = 0

def draw_score():
    font = pygame.font.SysFont('Arial', 30)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

def check_collision():
    # Check if bird hits the floor
    if bird_rect.bottom >= HEIGHT - FLOOR_HEIGHT:
        return True
    
    # Check if bird hits the ceiling
    if bird_rect.top <= 0:
        return True
    
    # Check if bird hits pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            return True
    
    return False

def update_pipes():
    global score
    # Move pipes to the left
    for pipe in pipes:
        pipe[0].x -= PIPE_SPEED
        pipe[1].x -= PIPE_SPEED
    
    # Remove pipes that are off screen
    pipes_copy = pipes.copy()
    for pipe in pipes_copy:
        if pipe[0].right < 0:
            pipes.remove(pipe)
            score += 1

def create_pipe():
    pipe_height = random.randint(100, 300)
    pipe_top = pygame.Rect(WIDTH, 0, 52, pipe_height)
    pipe_bottom = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, 52, HEIGHT - pipe_height - PIPE_GAP - FLOOR_HEIGHT)
    return [pipe_top, pipe_bottom]

def update_game_state(action=None):
    global bird_y, bird_velocity, game_over, last_pipe, game_started
    
    if action == "jump" and not game_over:
        bird_velocity = BIRD_JUMP
        game_started = True
    
    if action == "restart" and game_over:
        reset_game()
    
    if game_started and not game_over:
        # Apply gravity
        bird_velocity += GRAVITY
        bird_y += bird_velocity
        
        # Update bird rectangle position
        bird_rect.y = bird_y
        
        # Check for collisions
        game_over = check_collision()
        
        # Create new pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipes.append(create_pipe())
            last_pipe = current_time
        
        # Update pipes
        update_pipes()
    
    # Draw everything
    screen.blit(bg_img, (0, 0))  # Draw background
    draw_pipes()
    draw_floor()
    draw_bird()
    draw_score()
    
    if game_over:
        font = pygame.font.SysFont('Arial', 40)
        game_over_text = font.render('Game Over', True, BLACK)
        restart_text = font.render('Click to Restart', True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
    
    elif not game_started:
        font = pygame.font.SysFont('Arial', 30)
        start_text = font.render('Click to Start', True, BLACK)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 15))
    
    # Convert the pygame surface to a base64 encoded image
    image_data = pygame.image.tostring(screen, 'RGB')
    image = pygame.image.fromstring(image_data, (WIDTH, HEIGHT), 'RGB')
    
    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    pygame.image.save(image, buffer, 'PNG')
    buffer.seek(0)
    
    # Encode the image as base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return {
        'image': img_base64,
        'score': score,
        'game_over': game_over,
        'game_started': game_started
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state', methods=['GET', 'POST'])
def game_state():
    action = None
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
    
    state = update_game_state(action)
    return jsonify(state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52328, debug=True)