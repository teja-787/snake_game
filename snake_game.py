import pygame
import random

# Initialize pygame
pygame.init()

# Define window size
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = 10

# Direction
direction = "RIGHT"
change_to = direction

# Food
food_pos = [random.randrange(1, (WIDTH//10)) * 10,
            random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

# Score
score = 0

# Initialize music
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")  # Ensure the file is in the same directory
pygame.mixer.music.play(-1)  # Play music in a loop

# Function to display score
def show_score(color, font, size):
    font = pygame.font.SysFont(font, size)
    score_surface = font.render(f"Score: {score}", True, color)
    win.blit(score_surface, [10, 10])

# Function for Game Over screen
def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    go_surface = font.render('Game Over!', True, RED)
    win.blit(go_surface, [WIDTH//3, HEIGHT//3])
    pygame.display.flip()
    pygame.time.delay(2000)  # Wait for 2 seconds before quitting
    pygame.quit()
    exit()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controls for movement
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Move snake
    if direction == "UP":
        snake_pos[1] -= 10
    if direction == "DOWN":
        snake_pos[1] += 10
    if direction == "LEFT":
        snake_pos[0] -= 10
    if direction == "RIGHT":
        snake_pos[0] += 10

    # Snake body growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10,
                    random.randrange(1, (HEIGHT//10)) * 10]
    food_spawn = True

    # Collision with walls
    if snake_pos[0] < 0 or snake_pos[0] > WIDTH-10 or snake_pos[1] < 0 or snake_pos[1] > HEIGHT-10:
        game_over()

    # Collision with self
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Draw elements
    win.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    
    pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Show score
    show_score(WHITE, 'times new roman', 20)

    # Update display
    pygame.display.update()

    # Increase speed as score increases
    speed = 10 + (score // 2)
    clock.tick(speed)

pygame.quit()
