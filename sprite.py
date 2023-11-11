import pygame

sprites = []

class Sprite:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Load things uniquely.
