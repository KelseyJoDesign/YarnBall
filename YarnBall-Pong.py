import os
import platform
import pygame, asyncio
import sys
import json

# Initialize Pygame
pygame.init()

# Determine the operating system
current_os = platform.system()
base_path = r'C:\KelsCodes\YarnBall' if current_os == "Windows" else r'/Users/kelseygilles/Desktop/KelsCodes/YarnBall'

# Resources paths
silkscreen_font_path = os.path.join(base_path, 'Silkscreen/Silkscreen-Regular.ttf')
paddle_a_image_path = os.path.join(base_path, 'PNGs/YarnBall-Assets-BearPaw.png')
paddle_b_image_path = os.path.join(base_path, 'PNGs/YarnBall-Assets-ZoeyPaw.png')
ball_image_path = os.path.join(base_path, 'PNGs/YarnBall-Assets-Ball.png')
go_button_image_path = os.path.join(base_path, 'PNGs/YarnBall-Assets-GoButton.png')
bear_image_path = os.path.join(base_path, 'PNGs/YarnBall-Assets-Bear.png')
zoey_image_path = os.path.join(base_path, 'PNGs/YarnBall-Assets-Zoey.png')

# Game settings
WIDTH, HEIGHT = 800, 600
NAVY, WHITE = (30, 30, 106), (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yarn Ball")
silkscreen_font = pygame.font.Font(silkscreen_font_path, 36)

# Load and scale background
bg_image_path = os.path.join(base_path, 'PNGs/YarnBallAssets-Background.png')
bg_image = pygame.image.load(bg_image_path)
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Load images
paddle_a_image = pygame.transform.scale(pygame.image.load(paddle_a_image_path), (160, 135))
paddle_b_image = pygame.transform.scale(pygame.image.load(paddle_b_image_path), (160, 135))
ball_image = pygame.transform.scale(pygame.image.load(ball_image_path), (50, 50))
go_button_image = pygame.transform.scale(pygame.image.load(go_button_image_path), (160, 135))
bear_image = pygame.transform.scale(pygame.image.load(bear_image_path), (200, 165))
zoey_image = pygame.transform.scale(pygame.image.load(zoey_image_path), (200, 165))

# global go button define
go_button_image = pygame.transform.scale(pygame.image.load(go_button_image_path), (160, 135))
# Define go_button_rect globally here
go_button_rect = go_button_image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 150))

# Game variables
high_score = 0  # Add this at the top where you declare other global variables
paddle_speed = 10
initial_ball_speed_x = 2
initial_ball_speed_y = -2
ball_speed_x, ball_speed_y = 2, -2  # Start with slower speed
bounce_count_a, bounce_count_b, high_score = 0, 0, 0

# Check for previous high score
if os.path.exists(f"{os.getcwd()}/high_score.json"):
    high_score = json.load(open(f"{os.getcwd()}/high_score.json", "r"))
    high_score = high_score["high_score"]
    print(f"Found previous high score of {high_score}")
else:
    with open(f"{os.getcwd()}/high_score.json", "w") as f:
        high_score = {"high_score": high_score}
        json.dump(high_score, f)

# initial game state
game_state = "START"

# Paddle and ball Rects for positioning and collision
paddle_a_rect = pygame.Rect(0, HEIGHT // 2 - 135 // 2, 160, 135)
paddle_b_rect = pygame.Rect(WIDTH - 160, HEIGHT // 2 - 135 // 2, 160, 135)
ball_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50)

######################################################################################################################
# DEFINE START SCREEN
######################################################################################################################

def start_screen():
    global game_state

    # go button positioning
    go_button_rect = go_button_image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 150))

    # "YARN BALL" text and position
    larger_font = pygame.font.Font(silkscreen_font_path, (72))
    yarn_ball_text = larger_font.render("YARN BALL", True, WHITE)
    yarn_ball_text_pos = (WIDTH / 2 - yarn_ball_text.get_width() / 2, HEIGHT / 2 - 200)

    # Instructions text and position
    instructions_font = pygame.font.Font(silkscreen_font_path, 24)
    instructions_text = instructions_font.render("W + S : UP + DOWN", True, WHITE)
    instructions_text_pos = (WIDTH / 2 - instructions_text.get_width() / 2, HEIGHT - 400)  # Position it at the bottom

    # draw everything
    screen.blit(bg_image, (0, 0))
    screen.blit(bear_image, (20, HEIGHT / 2 - bear_image.get_height() / 2 + 50))
    screen.blit(zoey_image, (WIDTH - zoey_image.get_width() - 20, HEIGHT / 2 - zoey_image.get_height() / 2 + 50))
    screen.blit(go_button_image, go_button_rect.topleft)
    screen.blit(yarn_ball_text, yarn_ball_text_pos)  # Display "YARN BALL" text
    screen.blit(instructions_text, instructions_text_pos)  # Display instructions text
    
    pygame.display.flip()

    # Check for click on the go button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if go_button_rect.collidepoint(event.pos):
                game_state = "COUNTDOWN"
                return  # Exit the function immediately after changing the state

######################################################################################################################
# DEFINE COUNTDOWN
######################################################################################################################

def countdown():
    global game_state
    countdown_font = pygame.font.Font(silkscreen_font_path, 72)  # Larger font size for the countdown
    for number in range(3, 0, -1):
        screen.blit(bg_image, (0, 0))
        countdown_text = countdown_font.render(str(number), True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second before showing the next number
        game_state = "PLAYING"

######################################################################################################################
# DEFINE GAME LOOP
######################################################################################################################

def game_loop():
    global bounce_count_a, bounce_count_b, ball_rect, ball_speed_x, ball_speed_y, game_state
    
    while game_state == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_a_rect.top > 0:
            paddle_a_rect.y -= paddle_speed
        if keys[pygame.K_s] and paddle_a_rect.bottom < HEIGHT:
            paddle_a_rect.y += paddle_speed
        if keys[pygame.K_UP] and paddle_b_rect.top > 0:
            paddle_b_rect.y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle_b_rect.bottom < HEIGHT:
            paddle_b_rect.y += paddle_speed

        # Ball movement
        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y

        # Ball collision with paddles
        if ball_rect.colliderect(paddle_a_rect):
            ball_speed_x *= -1.03  # Increase speed by 3% and change direction
            bounce_count_a += 1
            ball_rect.x = paddle_a_rect.right  # Ensure ball is just outside the paddle

        if ball_rect.colliderect(paddle_b_rect):
            ball_speed_x *= -1.03  # Increase speed by 3% and change direction
            bounce_count_b += 1
            ball_rect.x = paddle_b_rect.left - ball_rect.width  # Ensure ball is just outside the paddle

        # Ball collision with top and bottom walls
        if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Score update & draw everything
        screen.blit(bg_image, (0, 0))
        screen.blit(paddle_a_image, paddle_a_rect.topleft)
        screen.blit(paddle_b_image, paddle_b_rect.topleft)
        screen.blit(ball_image, ball_rect.topleft)
        score_text = silkscreen_font.render(f"YOUR SCORE: {bounce_count_a + bounce_count_b}", True, WHITE)
        screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 20))

        # Check for game over
        if ball_rect.left < 0 or ball_rect.right > WIDTH:  # If ball goes past the left or right edge
            game_state = "GAME_OVER"

        # Listen for space bar press in the main loop
        if game_state == "GAME_OVER" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_state = "COUNTDOWN"
            # Reset scores and positions as needed here, similar to the mouse button logic

        pygame.display.flip()
        pygame.time.delay(10)

######################################################################################################################
# DEFINE GAME OVER
######################################################################################################################
def game_over():
    global game_state, bounce_count_a, bounce_count_b, high_score, zoey_image, bear_image, ball_speed_x, ball_speed_y

    # Game over text
    game_over_font = pygame.font.Font(silkscreen_font_path, 72)
    game_over_text = game_over_font.render("GAME OVER", True, WHITE)

    # score function and text display
    final_score = bounce_count_a + bounce_count_b
    if final_score > high_score:
        high_score = final_score
        with open(f"{os.getcwd()}/high_score.json", "w") as f:
            json.dump({"high_score": high_score}, f)
    score_message = f"YOUR SCORE: {final_score}"
    score_text = silkscreen_font.render(score_message, True, WHITE)
    high_score_text = silkscreen_font.render(f"HIGH SCORE: {high_score}", True, WHITE)

    # go button
    go_button_rect = go_button_image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))

    # Draw everything
    screen.blit(bg_image, (0, 0))
    screen.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - 200))
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - 115))
    screen.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, HEIGHT / 2))
    screen.blit(bear_image, (20, HEIGHT / 2 - bear_image.get_height() / 2 + 50))
    screen.blit(zoey_image, (WIDTH - zoey_image.get_width() - 20, HEIGHT / 2 - zoey_image.get_height() / 2 + 50))
    screen.blit(go_button_image, go_button_rect.topleft)
    
    pygame.display.flip()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and go_button_rect.collidepoint(event.pos):
            reset_game()  # Call a function to reset game variables and state

def reset_game():
    global bounce_count_a, bounce_count_b, game_state, ball_rect, ball_speed_x, ball_speed_y
    bounce_count_a = 0
    bounce_count_b = 0
    ball_rect.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = initial_ball_speed_x
    ball_speed_y = initial_ball_speed_y
    game_state = "COUNTDOWN"

######################################################################################################################
# MAIN GAME LOOP
######################################################################################################################

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "START":
        start_screen()
    elif game_state == "COUNTDOWN":
        countdown()
        game_state = "PLAYING"  # After countdown, automatically transition to PLAYING
    elif game_state == "PLAYING":
        game_loop()
    elif game_state == "GAME_OVER":
        game_over()

    pygame.display.flip()