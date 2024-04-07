import pygame
import sys
import math
import random
from button import Button

# Initialize Pygame
pygame.init()

# Set up screen dimensions
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Growth")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (234, 169, 98)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_health = 5
player_max_health = 5

# Enemy settings
enemy_width, enemy_height = 30, 30
enemy_speed = 2
enemy_health = 1
enemies = []

# Bullet settings
bullet_width, bullet_height = 10, 10
bullet_speed = 10
bullets = []

# Experience and Level settings
experience = 0
level = 1
exp_required = 10  # Experience required to level up

clock = pygame.time.Clock()

def draw_player(x, y, health, max_health):
    # Function to draw the player character
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

    health_tag_x = x + player_width // 2
    health_tag_y = y - 30
    font = pygame.font.Font(None, 36)
    health_tag = font.render(f"Health: {health}/{max_health}", True, WHITE)
    screen.blit(health_tag, (health_tag_x - health_tag.get_width() // 2, health_tag_y))

def draw_player_spawn_area(player_x, player_y):
    # Function to draw a green area around the player spawn position
    area_size = 3  # Size of the area around the player spawn
    area_color = (0, 255, 0)  # Green color

    # Calculate the position of the top-left corner of the area
    area_top_left_x = player_x - area_size * player_width // 2
    area_top_left_y = player_y - area_size * player_height // 2

    # Calculate the size of the area
    area_width = area_size * player_width
    area_height = area_size * player_height

    # Draw the green area
    pygame.draw.rect(screen, area_color, (area_top_left_x, area_top_left_y, area_width, area_height))

def draw_experience(experience, exp_required, level):
    # Function to draw the experience bar and level number
    bar_width = 300
    bar_height = 20
    bar_x = (WIDTH - bar_width) // 2
    bar_y = 20

    # Draw experience bar background
    pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width, bar_height))

    # Calculate the width of the filled part of the bar
    filled_width = bar_width * (experience / exp_required)

    # Draw filled part of the bar
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, filled_width, bar_height))

    # Draw text displaying current level
    font = pygame.font.Font(None, 24)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (bar_x + bar_width + 10, bar_y))

    # Draw text displaying current experience/required experience inside the bar
    exp_text = font.render(f"{experience}/{exp_required}", True, WHITE)
    exp_text_rect = exp_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
    screen.blit(exp_text, exp_text_rect)

def draw_enemy(x, y):
    # Function to draw an enemy
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height))


def draw_bullets(bullets):
    # Function to draw bullets on the screen
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

def move_bullets(bullets):
    # Function to move bullets
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed

def move_enemies(enemies):
    # Function to move enemies towards the player
    for enemy in enemies:
        dx = player_x - enemy[0]
        dy = player_y - enemy[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance
            enemy[0] += dx * enemy_speed
            enemy[1] += dy * enemy_speed
def spawn_enemy():
    # Function to spawn enemies from random sides of the screen
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH - enemy_width)
        y = -enemy_height
    elif side == "bottom":
        x = random.randint(0, WIDTH - enemy_width)
        y = HEIGHT
    elif side == "left":
        x = -enemy_width
        y = random.randint(0, HEIGHT - enemy_height)
    else:
        x = WIDTH
        y = random.randint(0, HEIGHT - enemy_height)
    enemies.append([x, y,enemy_health])

def menu(): #Main Menu
    pygame.display.set_caption("Menu")
    while True:
        screen.fill((204,102,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 100)
        MENU_TEXT = font.render("MAIN MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("GameAsset/Play Rect.png"), pos=(WIDTH/2, 300), 
                            text_input="PLAY", font=pygame.font.Font(None, 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("GameAsset/Quit Rect.png"), pos=(WIDTH/2, 500), 
                            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_over():
    pygame.display.set_caption("Menu")
    while True:
        screen.fill((0,0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 100)
        MENU_TEXT = font.render("GameOver", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 100))

        MAIN_MENU = Button(image=pygame.image.load("GameAsset/Play Rect.png"), pos=(WIDTH/2, 300), 
                            text_input="Main Menu", font=pygame.font.Font(None, 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("GameAsset/Quit Rect.png"), pos=(WIDTH/2, 500), 
                            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [MAIN_MENU, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_MENU.checkForInput(MENU_MOUSE_POS):
                    menu()
                    player_health = 5
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play():
    global player_x, player_y, bullets, player_health, enemies, experience, level, exp_required

    shooting = False  # Flag to track if shooting is active

    player_health = player_max_health
    experience = 0
    level = 1
    exp_required = 10

    

    while True:
        screen.fill(YELLOW)  # Fill the screen with black color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    shooting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    shooting = False

        if shooting:
            # Bullet direction based on player and mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx, dy = mouse_x - player_x, mouse_y - player_y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                dx /= distance
                dy /= distance
                # Create a bullet
                bullet = [player_x + player_width // 2 - bullet_width // 2, player_y + player_height // 2 - bullet_height // 2, dx, dy]
                bullets.append(bullet)

        keys = pygame.key.get_pressed()
        # Check key presses to move the player
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed

        # Ensure player stays centered on the screen
        screen_center_x = WIDTH // 2
        screen_center_y = HEIGHT // 2
        screen_x = screen_center_x - player_x - player_width // 2
        screen_y = screen_center_y - player_y - player_height // 2

        # Move enemies towards the player

        for enemy in enemies:
            enemy[0] += screen_x
            enemy[1] += screen_y

        # Move bullets
        for bullet in bullets:
            bullet[0] += screen_x
            bullet[1] += screen_y

        # Update player position
        player_x += screen_x
        player_y += screen_y

        # Spawn enemies randomly
        if random.randint(1, 100) == 1:
            spawn_enemy()

        # Move enemies towards the player
        move_enemies(enemies)

        # Move bullets
        move_bullets(bullets)

        #Bullets enemy collision
        for bullet in bullets:
            for enemy in enemies:
                if (bullet[0] < enemy[0] + enemy_width and bullet[0] + bullet_width > enemy[0] and bullet[1] < enemy[1] + enemy_height and bullet[1] + bullet_height > enemy[1]):
                    bullets.remove(bullet)
                    enemy[2] -= 1  # Decrease enemy health
                    if enemy[2] <= 0:
                        enemies.remove(enemy)
                        experience += 1  # Gain experience for killing an enemy
                        if experience >= exp_required:  # Level up when experience reaches required threshold
                            level += 1
                            experience = 0
                            exp_required += 10
                    break
        
        #Enemy player collision
        for enemy in enemies:
            if (player_x < enemy[0] + enemy_width and player_x + player_width > enemy[0] and player_y < enemy[1] + enemy_height and player_y + player_height > enemy[1]):
                player_health -= 1
                enemies.remove(enemy)

        # Draw player and bullets
        draw_player(player_x, player_y,player_health,5)
        draw_bullets(bullets)
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])

        draw_experience(experience, exp_required,level)

        if player_health <= 0:
            game_over()

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Cap the frame rate to 60 frames per secondda

def main():
    menu()

if __name__ == "__main__":
    main()

