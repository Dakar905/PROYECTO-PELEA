import pygame
from pygame import mixer
from fighter import Fighter
from map_selector import map_selector  # Import the map selector

mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)





pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)  # Transparent color

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
show_restart_button = False

# Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
small_font = pygame.font.Font("assets/fonts/turok.ttf", 50)  # Font for victory text

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg(bg_image):
    screen.blit(bg_image, (0, 0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 700 * ratio, 30))

# Select map
selected_map_index = map_selector()
map_images = [
    "assets/images/background/background.jpg",
    "assets/images/background/background1.jpg",
    "assets/images/background/background2.jpg",
    "assets/images/background/background3.jpeg",
    "assets/images/background/background.jpg",
    "assets/images/background/background.jpg"
]
bg_image = pygame.image.load(map_images[selected_map_index]).convert_alpha()

# Create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Game loop
run = True
while run:

    clock.tick(FPS)

    # Draw background
    draw_bg(bg_image)

    # Show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("EL ESPADACHIN MIGUEL: " + str(score[0]), score_font, RED, 20, 80)  # Adjusted Y position
    draw_text("EL MAGO ARTURO: " + str(score[1]), score_font, RED, 580, 80)  # Adjusted Y position

    # Update countdown
    if intro_count <= 0:
        # Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # Display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # Update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Update fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for player defeat
    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            winner = 2  # Wizard won
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            winner = 1  # Warrior won
    else:
        if winner == 1:
            winner_text = "EL ESPADACHIN MIGUEL"
        else:
            winner_text = "EL MAGO ARTURO"

        draw_text(f"{winner_text} ¡GANO!", small_font, RED, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20)  # Centered text

        # Draw transparent restart button
        restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, TRANSPARENT, restart_rect)
        pygame.draw.rect(screen, RED, restart_rect, 2)

        draw_text("Restart", small_font, RED, restart_rect.centerx - 60, restart_rect.centery - 15)

        # Check if restart button is clicked or Enter is pressed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(mouse_x, mouse_y):
                if round_over:
                    round_over = False
                    intro_count = 3
                    score = [0, 0]
                    selected_map_index = map_selector()
                    bg_image = pygame.image.load(map_images[selected_map_index]).convert_alpha()
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if round_over:
                    round_over = False
                    intro_count = 3
                    score = [0, 0]
                    selected_map_index = map_selector()
                    bg_image = pygame.image.load(map_images[selected_map_index]).convert_alpha()
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

# Exit pygame
pygame.quit()
