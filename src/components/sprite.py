import pygame
from core.camera import camera

image_path = "content/images"

sprites = []
loaded = {}

def reset_sprites():
    global sprites
    sprites.clear()

class Sprite:
    def __init__(self, image, is_ui=False):
        global sprites
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_path + "/" + image)
            loaded[image] = self.image
        sprites.append(self)
        self.is_ui = is_ui

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui else \
                (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)

# Load things uniquely.
