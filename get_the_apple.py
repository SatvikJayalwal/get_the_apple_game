import pygame
import random

# Initialize pygame
pygame.init()

# Get the screen dimensions for full screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("GET THE APPLE")

# Load images
background_image = pygame.image.load("C:\\python_codes\\get_the_apple_game\\get_the_apple_bg.webp")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

basket_image = pygame.image.load("C:\\python_codes\\get_the_apple_game\\basket.webp")
basket_size = 80
basket_image = pygame.transform.scale(basket_image, (basket_size, basket_size))

leaf_image = pygame.image.load("C:\\python_codes\\get_the_apple_game\\leaf.png")
leaf_size = 80
leaf_image = pygame.transform.scale(leaf_image, (leaf_size, leaf_size))

apple_image = pygame.image.load("C:\\python_codes\\get_the_apple_game\\apple.png")
apple_size = 80
apple_image = pygame.transform.scale(apple_image, (apple_size, apple_size))

# Load sounds
collision_sound = pygame.mixer.Sound("C:\\python_codes\\get_the_apple_game\\gameend.mp3")
powerup_sound = pygame.mixer.Sound("C:\\python_codes\\get_the_apple_game\\powerup.mp3")

# Load and play background music
pygame.mixer.music.load("C:\\python_codes\\get_the_apple_game\\gamebgm.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Game variables
basket1 = [WIDTH // 2 - 100, HEIGHT - 2 * basket_size]
basket2 = [WIDTH // 2 + 100, HEIGHT - 2 * basket_size]
leaf_list = []
apple_list = []
score = 0
level = 1

# Movement flags
moving_left = False
moving_right = False
moving_left_p2 = False
moving_right_p2 = False

# Pause flag
paused = False

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("monospace", 35, bold=True)

def get_speed(score):
    return 10 + (score // 10) * 2

def drop_enemies(leaf_list):
    delay = random.random()
    if len(leaf_list) < 10 + level * 5 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - leaf_size)
        y_pos = 0
        if not any(detect_collision([x_pos, y_pos], enemy) for enemy in leaf_list):
            leaf_list.append([x_pos, y_pos])

def drop_powerups(apple_list):
    delay = random.random()
    if len(apple_list) < 1 and delay < 0.01:
        x_pos = random.randint(0, WIDTH - apple_size)
        y_pos = 0
        apple_list.append([x_pos, y_pos])

def detect_collision(pos1, pos2):
    p1_x, p1_y = pos1
    p2_x, p2_y = pos2

    if (p1_x >= p2_x and p1_x < (p2_x + leaf_size)) or (p2_x >= p1_x and p2_x < (p1_x + leaf_size)):
        if (p1_y >= p2_y and p1_y < (p2_y + leaf_size)) or (p2_y >= p1_y and p2_y < (p1_y + leaf_size)):
            return True
    return False

def draw_leaf(leaf_list):
    for leaf_pos in leaf_list:
        screen.blit(leaf_image, (leaf_pos[0], leaf_pos[1]))

def draw_apple(apple_list):
    for leaf_pos in apple_list:
        screen.blit(apple_image, (leaf_pos[0], leaf_pos[1]))

def update_leaf_position(leaf_list, score):
    speed = get_speed(score)
    for idx, leaf_pos in enumerate(leaf_list):
        if leaf_pos[1] >= 0 and leaf_pos[1] < HEIGHT:
            leaf_pos[1] += speed
        else:
            leaf_list.pop(idx)
            score += 1
    return score

def update_apple_position(apple_list):
    speed = get_speed(score) // 2
    for idx, leaf_pos in enumerate(apple_list):
        if leaf_pos[1] >= 0 and leaf_pos[1] < HEIGHT:
            leaf_pos[1] += speed
        else:
            apple_list.pop(idx)

def leaf_collision_check(leaf_list, basket_pos):
    for leaf_pos in leaf_list:
        if detect_collision(leaf_pos, basket_pos):
            return True
    return False

def apple_collision_check(apple_list, basket_pos):
    for leaf_pos in apple_list:
        if detect_collision(leaf_pos, basket_pos):
            apple_list.remove(leaf_pos)
            return True
    return False

def game_over_screen():
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50)) 
    
    text = font.render("Do you want to play again? (Y/N)", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.update() 
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting_for_input = False
                    return True
                elif event.key == pygame.K_n:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def render_text_with_shadow(text, font, color, shadow_color, position):
    shadow_offset = 2
    shadow = font.render(text, True, shadow_color)
    text = font.render(text, True, color)
    shadow_rect = shadow.get_rect(center=(position[0] + shadow_offset, position[1] + shadow_offset))
    text_rect = text.get_rect(center=position)
    screen.blit(shadow, shadow_rect)
    screen.blit(text, text_rect)

def welcome_screen():
    background_image = pygame.image.load("C:\\python_codes\\get_the_apple_game\\get_the_apple_bg.webp")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    options = ["Single Player", "Multiplayer", "Exit"]
    selected_option = 0

    while True:
        screen.blit(background_image, (0, 0))  # Draw the background image

        render_text_with_shadow("GET THE APPLE", font, (255, 255, 255), (0, 0, 0), (WIDTH // 2, HEIGHT // 2 - 100))
        
        for i, option in enumerate(options):
            color = (255, 255, 255)  # Default color
            if i == selected_option:
                color = (255, 0, 0)  # Highlight color

            render_text_with_shadow(option, font, color, (0, 0, 0), (WIDTH // 2, HEIGHT // 2 + i * 50))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Exit":
                        pygame.quit()
                        exit()
                    else:
                        return options[selected_option].lower()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, option in enumerate(options):
                    option_rect = font.render(option, True, (255, 255, 255)).get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                    if option_rect.collidepoint(mouse_pos):
                        if option == "Exit":
                            pygame.quit()
                            exit()
                        else:
                            return option.lower()

def display_scoreboard(score, level):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

def pause_screen():
    global paused  # Declare paused as global here
    screen.fill((0, 0, 0))
    text = font.render("PAUSED", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    
    text = font.render("Press SPACE to resume", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Main game loop
game_mode = welcome_screen()

while True:
    # Initialize game variables
    basket1 = [WIDTH // 2 - 100, HEIGHT - 2 * basket_size]
    basket2 = [WIDTH // 2 + 100, HEIGHT - 2 * basket_size]
    leaf_list = []
    apple_list = []
    score = 0
    level = 1
    game_over = False
    paused = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                elif event.key == pygame.K_RIGHT:
                    moving_right = True
                elif event.key == pygame.K_a:
                    moving_left_p2 = True
                elif event.key == pygame.K_d:
                    moving_right_p2 = True
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pause_screen()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                elif event.key == pygame.K_RIGHT:
                    moving_right = False
                elif event.key == pygame.K_a:
                    moving_left_p2 = False
                elif event.key == pygame.K_d:
                    moving_right_p2 = False

        if not paused:
            # Move the players
            if moving_left:
                basket1[0] -= basket_size // 2
            if moving_right:
                basket1[0] += basket_size // 2
            if moving_left_p2:
                basket2[0] -= basket_size // 2
            if moving_right_p2:
                basket2[0] += basket_size // 2

            # Ensure the players stay within screen boundaries
            basket1[0] = max(0, min(WIDTH - basket_size, basket1[0]))
            basket2[0] = max(0, min(WIDTH - basket_size, basket2[0]))

            # Draw background
            screen.blit(background_image, (0, 0))

            drop_enemies(leaf_list)
            drop_powerups(apple_list)
            score = update_leaf_position(leaf_list, score)
            update_apple_position(apple_list)

            if leaf_collision_check(leaf_list, basket1) or (game_mode == 'multiplayer' and leaf_collision_check(leaf_list, basket2)):
                collision_sound.play()
                moving_left = False
                moving_right = False
                moving_left_p2 = False
                moving_right_p2 = False
                game_over = True 
                if game_over_screen():
                    game_mode = welcome_screen()

            if apple_collision_check(apple_list, basket1) or (game_mode == 'multiplayer' and apple_collision_check(apple_list, basket2)):
                powerup_sound.play()
                # Reduce speed of enemies
                speed = get_speed(score)
                speed -= 2

            draw_leaf(leaf_list)
            draw_apple(apple_list)
            screen.blit(basket_image, (basket1[0], basket1[1]))
            if game_mode == 'multiplayer':
                screen.blit(basket_image, (basket2[0], basket2[1]))

            display_scoreboard(score, level)
        
        pygame.display.update()
        clock.tick(30)
