import pygame

class Fruit:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self,display):
        display.blit(self.image, self.rect)

# Detect collision between monster and fruits
def check_fruit_collision(monster, fruits, eating):
    for fruit in fruits[:]:
        if monster.rect.colliderect(fruit.rect):
            pygame.mixer.Sound.play(eating)  # Play eating sound
            fruits.remove(fruit)  # Remove the fruit after eating