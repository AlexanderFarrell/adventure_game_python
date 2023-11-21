import pygame
from camera import camera

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image)
            loaded[image] = self.image
        self.x = x
        self.y = y
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x - camera.x, self.y - camera.y))

# Load things uniquely.
