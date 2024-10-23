import pygame, sys

# from pygame.locals import *

pygame.init()

resolution: tuple = (800, 800)
display = pygame.display.set_mode(resolution)
pygame.display.set_caption("Night of the Consumer")

# Creates a background for the level
background = pygame.image.load("background.PNG").convert_alpha()


# Temporary grid
def draw_grid():
    for line in range(0, 16):
        pygame.draw.line(display, (255, 255, 255), (0, line * 50), (800, line * 50))
        pygame.draw.line(display, (255, 255, 255), (line * 50, 0), (line * 50, line * 800))


# Player / Monster
class Monster:
    def __init__(self, x, y):
        """Initializes a new monster with initial position data
        :param x: Initial X position
        :param y: Initial Y position
        """

        # Defines a monster with the sprite png and scales it
        Monster.png = pygame.image.load('monster.PNG')
        self.image = pygame.transform.scale(Monster.png, (80, 80))

        # Defines the position of the monster
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Defines initial direction data
        self.direction: int = 1
        self.last_direction: int = 1

        # Defines initial y velocity and jump value
        self.vel_y = 0
        self.jumped = False

    def update(self):
        """Updates the player position based on user input
        """

        # Change in x and y position
        dx = 0
        dy = 0

        # Gets user input from the keyboard
        key = pygame.key.get_pressed()

        # Moves the character based on user input
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.direction = 0  # Updates the direction of the sprite
            dx -= 5
        if key[pygame.K_RIGHT] and self.rect.right < 800:
            self.direction = 1  # Updates the direction of the sprite
            dx += 5

        # Flips the sprite if the player changes the direction they're facing
        if not self.direction == self.last_direction:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
            self.last_direction = self.direction  # Updates the last direction

        # Adds to the y velocity value for gravity
        self.vel_y += 1

        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 800:
            self.rect.bottom = 800
            dy = 0

        # Draw player onto screen
        display.blit(self.image, self.rect)

    def get_coordinates(self) -> tuple:
        """Gets the current player position

        :return: Tuple representation of the position as (x, y)
        """
        return self.rect.x, self.rect.y


class Level:
    def __init__(self, data):
        """Adds tiles for the platforms of the game based on the level map

        :param data:
        """
        self.tile_list = []

        # Defines the images for the dirt and grass pngs
        dirt = pygame.image.load("dirt.PNG").convert_alpha()
        grass = pygame.image.load("ground.PNG").convert_alpha()

        row_count = 0 # Initializes row counter
        for row in data:
            # Assigns a blank tile for the level builder
            col_count = 0 # Initializes column counter
            for tile in row:
                if tile == 1:
                    # Assigns tile 1 in the level builder as the dirt png and rescales it
                    dirt = pygame.transform.scale(dirt, (50, 50))
                    dirt_rect = dirt.get_rect()
                    dirt_rect.x = col_count * 50  # X coordinate
                    dirt_rect.y = row_count * 50  # Y coordinate
                    tile = (dirt, dirt_rect)
                    self.tile_list.append(tile) # Saves the tile to tile list
                if tile == 2:
                    # Assigns tile 2 in the level builder as the grass png and rescales it
                    grass = pygame.transform.scale(grass, (50, 50))
                    grass_rect = grass.get_rect()
                    grass_rect.x = col_count * 50  # X coordinate
                    grass_rect.y = row_count * 50  # Y coordinate
                    tile = (grass, grass_rect)
                    self.tile_list.append(tile) # Saves the tile to tile list
                col_count += 1 # Increments the column value
            row_count += 1 # Increments the row value

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])


level_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]
]

level: Level = Level(level_map)
monster: Monster = Monster(100, 800 - 130)
clock = pygame.time.Clock()

loop: bool = True
score: int = 0

while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    display.blit(background, (0, 0))

    level.draw()
    monster.update()

    # Temporary grid
    draw_grid()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()