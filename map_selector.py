import pygame
import os

pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Map Selector")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Load map images
map_images = [
    pygame.image.load("assets/images/background/background.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/background1.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/background2.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/background3.jpeg").convert_alpha(),
    pygame.image.load("assets/images/background/background.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/background.jpg").convert_alpha(),
]

# Load selector background image
selector_bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Define font
font = pygame.font.Font(None, 50)

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Function to draw text with animation
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    alpha = 128 + 128 * (pygame.time.get_ticks() % 1000 > 500)
    img.set_alpha(alpha)
    screen.blit(img, (x - img.get_width() // 2, y))

# Function to draw rounded rectangle
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Map selector function
def map_selector():
    selected_map = 0
    run = True
    while run:
        screen.blit(selector_bg_image, (0, 0))

        for i, img in enumerate(map_images):
         x = (i % 3) * (SCREEN_WIDTH // 3) + 50
         y = (i // 3) * (SCREEN_HEIGHT // 2) + 100
         rect = pygame.Rect(x, y, SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 100)
         draw_rounded_rect(screen, WHITE, rect, 10)
         screen.blit(pygame.transform.scale(img, (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 100)), rect.topleft)
         if i == selected_map:
                   pygame.draw.rect(screen, RED, rect, 5, border_radius=10)


        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and selected_map % 3 > 0:
                    selected_map -= 1
                if event.key == pygame.K_RIGHT and selected_map % 3 < 2:
                    selected_map += 1
                if event.key == pygame.K_UP and selected_map >= 3:
                    selected_map -= 3
                if event.key == pygame.K_DOWN and selected_map < 3:
                    selected_map += 3
                if event.key == pygame.K_RETURN:
                    run = False

        # Update display
        draw_text("Select Map and Press Enter", font, RED, SCREEN_WIDTH // 2, 40)
        pygame.display.update()
        clock.tick(FPS)

    return selected_map

# Main program
def main():
    selected_map = map_selector()
    print(f"Selected Map: {selected_map}")
    # Here you can start your game with the selected map
    # For example: start_game(selected_map)

if __name__ == "__main__":
    main()
