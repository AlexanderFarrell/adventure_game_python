import pygame
from core.camera import camera

image_path = "content/images"

sprites = []
loaded = {}

def reset_sprites():
    global sprites
    sprites.clear()

class Sprite:
    def __init__(self, image):
        global sprites
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_path + "/" + image)
            loaded[image] = self.image
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.entity.x - camera.x, self.entity.y - camera.y))

# Load things uniquely.
