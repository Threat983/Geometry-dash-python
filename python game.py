import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash Clone')

# Colors
WHITE = (0, 48, 143)                            
BLACK = (0, 0, 0)

# Load and scale the player sprite image
player_img = pygame.image.load('sprite.png')
player_size = 50
player_img = pygame.transform.scale(player_img, (player_size, player_size))

# Player attributes
player_x = 100
player_y = HEIGHT - player_size
player_velocity_y = 0
gravity = 1
jump_height = -15

# Load and scale the spike image to match the original obstacle size
spike_img = pygame.image.load('spike.png')
spike_width, spike_height = 50, 50
spike_img = pygame.transform.scale(spike_img, (spike_width, spike_height))

# Obstacle attributes
obstacle_velocity_x = -10

# Speed increment and score
speed_increment = 0.5
score = 0

# Clock
clock = pygame.time.Clock()

# Function to generate random spikes
def generate_spikes():
    spikes = []
    spike_type = random.choice(['single', 'double'])  # Choose randomly between single and double spikes
    if spike_type == 'single':
        spike_x = WIDTH
        spike_y = HEIGHT - spike_height
        spikes.append((spike_x, spike_y, 'single'))
    else:
        spike_x1 = WIDTH
        spike_x2 = WIDTH + spike_width  # Position the second spike next to the first one
        spike_y = HEIGHT - spike_height
        spikes.append((spike_x1, spike_y, 'double'))
        spikes.append((spike_x2, spike_y, 'double'))
    return spikes

# Generate the first set of spikes
spikes = generate_spikes()

# Main game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player_y == HEIGHT - player_size:
        player_velocity_y = jump_height

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Prevent the player from falling through the ground
    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_velocity_y = 0

    # Move spikes
    for i in range(len(spikes)):
        x, y, spike_type = spikes[i]
        spikes[i] = (x + obstacle_velocity_x, y, spike_type)

    # Regenerate spikes if they move off-screen
    if spikes[-1][0] < 0:
        spikes = generate_spikes()
        score += 1  # Increase score when the obstacle is passed

        # Increase the speed of the obstacles
        obstacle_velocity_x -= speed_increment

    # Collision detection
    for spike_x, spike_y, spike_type in spikes:
        if spike_type == 'single':
            if (player_x < spike_x + spike_width and
                player_x + player_size > spike_x and
                player_y + player_size > spike_y):
                running = False  # End the game if collision occurs
        else:
            # Handle collision for double spikes
            if ((player_x < spike_x + spike_width and
                 player_x + player_size > spike_x and
                 player_y + player_size > spike_y) or
                (player_x < spike_x + spike_width * 2 and
                 player_x + player_size > spike_x and
                 player_y + player_size > spike_y)):
                running = False  # End the game if collision occurs

    # Draw everything
    screen.fill(WHITE)
    screen.blit(player_img, (player_x, player_y))  # Draw the player sprite
    for spike_x, spike_y, spike_type in spikes:
        if spike_type == 'single':
            screen.blit(spike_img, (spike_x, spike_y))  # Draw single spike
        else:
            screen.blit(spike_img, (spike_x, spike_y))  # Draw the first part of double spike
            # Draw the second part of double spike
            screen.blit(spike_img, (spike_x + spike_width, spike_y))

    # Display the score
    font = pygame.font.SysFont(None, 35)
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, (10, 10))

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
