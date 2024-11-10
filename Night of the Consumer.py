import pygame, sys
from main_screen import MainScreen
from monster import Monster
from level import Level, spawn_fruits
from fruit import check_fruit_collision
from win_screen import display_win_screen

# from pygame.locals import *

pygame.init()

resolution: tuple = (800, 800)
display = pygame.display.set_mode(resolution)
pygame.display.set_caption("Night of the Consumer")

# Background and icons
background = pygame.image.load("background.PNG").convert_alpha()
monstermini = pygame.image.load('monster.PNG').convert_alpha()
pygame.display.set_icon(monstermini)

# Title screen images
start_img = pygame.image.load("start.png").convert_alpha()
exit_img = pygame.image.load("exit.png").convert_alpha()
directions = pygame.image.load("directions.png").convert_alpha()
restart_img = pygame.image.load("restart.png").convert_alpha()

# Buttons
start_button = pygame.transform.scale(start_img, (200, 200))
exit_button = pygame.transform.scale(exit_img, (200, 200))
directions = pygame.transform.scale(directions, (450, 200))
restart_button = pygame.transform.scale(restart_img, (450, 200))
start_rect = start_button.get_rect(center=(800 / 2 - 125, 800 / 2 - 100))
exit_rect = exit_button.get_rect(center=(800 / 2 + 125, 800 / 2 - 100))
directions_rect = directions.get_rect(center=(800 / 2, 800 / 2 + 100))
restart_rect = restart_button.get_rect(center=(800 / 2, 800 / 2 + 100))

# Sounds
bg_music = pygame.mixer.Sound("background.mp3")
eating = pygame.mixer.Sound("eating.mp3")
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

# Initialize Fonts
main_font = pygame.font.Font("Melted Monster.ttf", 64)
main_font_pos = (400, 100)
direction_font = pygame.font.Font("Melted Monster.ttf" , 32)
direction_font_pos = (400, 650)
direction_font2 = pygame.font.Font("Melted Monster.ttf" , 32)
direction_font_pos2 = (400, 750)

def restart_game():
    """Restarts the game by resetting game state and reloading necessary elements."""
    global monster, fruits, level

    # Re-initialize the game components
    monster = Monster(100, 600)  # Re-position the monster to its starting location
    level = Level(level_map)  # Re-load the level
    fruits = spawn_fruits(level)  # Spawn fruits again


# Level map using tiles to build the platformer
level_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 3, 0, 0, 2, 2, 2, 2, 3, 3, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 3, 3, 3],
    [0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 1, 0, 0, 0],
    [0, 3, 3, 3, 0, 0, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 3, 3, 3],
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 2, 2],
    [2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 1, 1],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]
]

# Main game loop setup
main_screen = MainScreen()
monster = Monster(100,600)
level = Level(level_map)
clock = pygame.time.Clock()
main_screen.title_screen( display, background, start_button, start_rect, exit_button, exit_rect, directions, directions_rect, main_font, main_font_pos, direction_font, direction_font_pos, direction_font_pos2)
fruits = spawn_fruits(level)

loop: bool = True
score: int = 0
game_over = False


while loop:

    # Draws buttons and background
    display.blit(background, (0, 0))
    level.draw(display)
    monster.update(display, level.tile_list)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and restart_rect.collidepoint(event.pos):
                restart_game()
                game_over = False  # Reset the game over flag

    # Update and draw the game only if it's not over
    if not game_over:
        monster.update(display, level.tile_list)
        level.draw(display)

        # Draw fruits and check for collisions
        for fruit in fruits:
            fruit.draw(display)
        check_fruit_collision(monster, fruits, eating)

        # Check if all fruits are eaten
        if not fruits:
            game_over = True  # Set game over to True when the player wins
    else:
        # Display the win screen and restart button
        display_win_screen(display, restart_button, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()