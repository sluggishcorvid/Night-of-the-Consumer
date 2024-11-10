import pygame, random
from fruit import Fruit

class Level:
    def __init__(self, data):
        """Adds tiles for the platforms of the game based on the level map

        :param data:
        """
        self.tile_list = []
        self.spawn_points = []  # List to store potential fruit spawn points

        # Defines the images for the dirt and grass pngs
        dirt = pygame.image.load("dirt.PNG").convert_alpha()
        grass = pygame.image.load("ground.PNG").convert_alpha()

        row_count = 0 # Initializes row counter
        for row in data:
            # Assigns a blank tile for the level builder
            col_count = 0  # Initializes column counter
            for tile in row:
                if tile == 3:
                    # Store potential fruit spawn points when tile is 0
                    self.spawn_points.append((col_count * 50, row_count * 50))
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

    def draw(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])


def spawn_fruits(level):
    fruits = []
    fruit_images = ['apple.png', 'pineapple.png']

    for spawn_point in level.spawn_points:
        if random.random() < 0.2:  # Adjust the probability as needed for more or fewer fruits
            fruit_image = random.choice(fruit_images)
            fruit = Fruit(fruit_image, spawn_point[0], spawn_point[1])
            fruits.append(fruit)

    return fruits