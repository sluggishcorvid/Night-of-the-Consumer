import pygame, sys, random

# from pygame.locals import *

"""
TODO: :}
    Fruit spawning
    Fruit sound effects
    Fruit Collisions
    Score logging
    background music
    separate methods into new files
    youtube video
"""

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

# Buttons
start_button = pygame.transform.scale(start_img, (200, 200))
exit_button = pygame.transform.scale(exit_img, (200, 200))
directions = pygame.transform.scale(directions, (450, 200))
start_rect = start_button.get_rect(center=(800 / 2 - 125, 800 / 2 - 100))
exit_rect = exit_button.get_rect(center=(800 / 2 + 125, 800 / 2 - 100))
directions_rect = directions.get_rect(center=(800 / 2, 800 / 2 + 100))

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
direction_font_pos = (400, 700)

# Creates the title screen
class MainScreen:
    def title_screen(self):
        directionDisplay = False
        """Displays the title screen with interactive image buttons."""
        while True:
            display.blit(background, (0, 0))
            display.blit(start_button, start_rect)
            display.blit(exit_button, exit_rect)
            display.blit(directions, directions_rect)
            title_text = main_font.render("Night of the Consumer", True, (255, 255, 191))
            display.blit(title_text, title_text.get_rect(center=main_font_pos))

            if directionDisplay:
                directions_text = direction_font.render("A  and D to move and SPACE to jump", True,(255, 255, 191))
                display.blit(directions_text, directions_text.get_rect(center=direction_font_pos))


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return  # Exit title screen to start the game
                    elif exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif directions_rect.collidepoint(event.pos):
                        directionDisplay = True
                        self.show_directions()  # Call function to display directions

            pygame.display.flip()

    def show_directions(self):
        """Displays game directions or instructions."""
        directions_text = direction_font.render("A and D to move and SPACE to jump", True, (255, 255, 191))
        display.blit(directions_text, directions_text.get_rect(center=direction_font_pos))

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

    def update(self, tiles):
        """Updates the player position based on user input
        """

        # Change in x and y position
        dx = 0
        dy = 0

        # Gets user input from the keyboard
        key = pygame.key.get_pressed()

        # Moves the character based on user input
        if (key[pygame.K_SPACE] or key[pygame.K_UP]) and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not (key[pygame.K_SPACE] or key[pygame.K_UP]):
            self.jumped = False
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.left > 0:
            self.direction = 0 # Updates the direction of the sprite
            dx -= 5
        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.rect.right < 800:
            self.direction = 1 # Updates the direction of the sprite
            dx += 5

        # Flips the sprite if the player changes the direction they're facing
        if not self.direction == self.last_direction:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
            self.last_direction = self.direction # Updates the last direction

        # Adds to the y velocity value for gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Update position with collision
        dx, dy = self.check_collisions(dx, dy, tiles)

        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > 800:
            self.rect.bottom = 800
            dy = 0

        display.blit(self.image, self.rect)

    def check_collisions(self, dx, dy, tiles):
        for tile in tiles:
            # Horizontal collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0  # Stop horizontal movement on collision

            # Vertical collision
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:  # Falling
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                elif self.vel_y < 0:  # Jumping
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
        return dx, dy

class Fruit:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        display.blit(self.image, self.rect)

# Function to generate random fruits on the platforms
def spawn_fruits(platforms):
    fruits = []
    fruit_images = ['apple.png', 'pineapple.png']
    for _ in range(15):  # Spawn a number of fruits (adjustable)
        platform = random.choice(platforms)
        fruit_image = random.choice(fruit_images)
        x = platform[1].x + random.randint(0, platform[1].width - 30)
        y = platform[1].y - 30  # Place fruit slightly above the platform
        fruits.append(Fruit(fruit_image, x, y))
    return fruits

# Detect collision between monster and fruits
def check_fruit_collision(monster, fruits):
    for fruit in fruits[:]:
        if monster.rect.colliderect(fruit.rect):
            pygame.mixer.Sound.play(eating)  # Play eating sound
            fruits.remove(fruit)  # Remove the fruit after eating

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
            col_count = 0  # Initializes column counter
            for tile in row:
                if tile == 1:
                    # Assigns tile 1 in the level builder as the dirt png and rescales it
                    dirt = pygame.transform.scale(dirt, (50, 50))
                    dirt_rect = dirt.get_rect()
                    dirt_rect.x = col_count * 50  # X coordinate
                    dirt_rect.y = row_count * 50  # Y coordinate
                    tile = (dirt, dirt_rect)
                    self.tile_list.append(tile)  # Saves the tile to tile list
                if tile == 2:
                    # Assigns tile 2 in the level builder as the grass png and rescales it
                    grass = pygame.transform.scale(grass, (50, 50))
                    grass_rect = grass.get_rect()
                    grass_rect.x = col_count * 50 # X coordinate
                    grass_rect.y = row_count * 50 # Y coordinate
                    self.tile_list.append((grass, grass_rect)) # Saves the tile to tile list
                col_count += 1  # Increments the column value
            row_count += 1 # Increments the row value

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

# Level map using tiles to build the platformer
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

# Main game loop setup
level = Level(level_map)
monster = Monster(100, 800 - 130)
clock = pygame.time.Clock()
main_screen = MainScreen()
main_screen.title_screen()

loop: bool = True
score: int = 0
fruits = spawn_fruits(level.tile_list)

while loop:

    # Draws buttons and background
    display.blit(background, (0, 0))
    level.draw()
    monster.update(level.tile_list)
    for fruit in fruits:
        fruit.draw()
    check_fruit_collision(monster, fruits)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)