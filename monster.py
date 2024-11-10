import pygame

class Monster:
    def __init__(self, x, y, ):
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

    def update(self, display, tiles):
        """Updates the player position based on user input
        """

        # Change in x and y position
        dx = 0
        dy = 0

        # Gets user input from the keyboard
        key = pygame.key.get_pressed()

        # Moves the character based on user input
        if (key[pygame.K_w] or key[pygame.K_UP]) and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not (key[pygame.K_w] or key[pygame.K_UP]):
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