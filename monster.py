import pygame

class Monster:
    IMAGE_PATH = 'monster.PNG'
    IMAGE_SIZE = (80, 80)
    GRAVITY = 1
    MAX_FALL_SPEED = 10
    JUMP_STRENGTH = -15
    MOVE_SPEED = 5
    FLOOR_LIMIT = 800

    # Load and scale image once
    _base_image = pygame.transform.scale(pygame.image.load(IMAGE_PATH), IMAGE_SIZE)

    def __init__(self, x, y):
        """Initializes a new monster with initial position data"""
        self.image = Monster._base_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.last_direction = 1
        self.vel_y = 0
        self.jumped = False

    def update(self, display, tiles):
        dx, dy = 0, 0
        key = pygame.key.get_pressed()

        # Jumping
        if (key[pygame.K_w] or key[pygame.K_UP]):
            if not self.jumped:
                self.vel_y = Monster.JUMP_STRENGTH
                self.jumped = True
        else:
            self.jumped = False

        # Horizontal movement
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if self.rect.left > 0:
                self.direction = 0
                dx -= Monster.MOVE_SPEED
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.rect.right < 800:
                self.direction = 1
                dx += Monster.MOVE_SPEED

        # Flip sprite if direction changed
        if self.direction != self.last_direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.last_direction = self.direction

        # Apply gravity
        self.vel_y = min(self.vel_y + Monster.GRAVITY, Monster.MAX_FALL_SPEED)
        dy += self.vel_y

        # Collision detection
        dx, dy = self.check_collisions(dx, dy, tiles)

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Floor boundary
        if self.rect.bottom > Monster.FLOOR_LIMIT:
            self.rect.bottom = Monster.FLOOR_LIMIT
            self.vel_y = 0

        display.blit(self.image, self.rect)

    def check_collisions(self, dx, dy, tiles):
        future_rect_x = self.rect.move(dx, 0)
        future_rect_y = self.rect.move(0, dy)

        for _, tile_rect in tiles:
            if tile_rect.colliderect(future_rect_x):
                dx = 0
            if tile_rect.colliderect(future_rect_y):
                if self.vel_y > 0:  # Falling
                    dy = tile_rect.top - self.rect.bottom
                elif self.vel_y < 0:  # Jumping
                    dy = tile_rect.bottom - self.rect.top
                self.vel_y = 0
        return dx, dy
