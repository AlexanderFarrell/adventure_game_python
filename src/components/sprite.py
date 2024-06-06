import pygame
from core.camera import camera

image_path = "content/images"

loaded = {}

class Sprite:
    def __init__(self, image, is_ui=False):
        from core.engine import engine
        global sprites
        self.is_ui = is_ui

        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_path + "/" + image)
            loaded[image] = self.image
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if is_ui:
            engine.ui_drawables.append(self)
        else:
            engine.drawables.append(self)

    def set_image(self, image):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_path + "/" + image)
            loaded[image] = self.image

    def rotate(self, amo):
        self.image = pygame.transform.rotate(self.image, amo)

    def scale(self, x_scale, y_scale):
        self.image = pygame.transform.scale(self.image, (x_scale, y_scale))

    def breakdown(self):
        from core.engine import engine
        if self.is_ui:
            engine.ui_drawables.remove(self)
        else:
            engine.drawables.remove(self)

    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui else \
                (self.entity.x, self.entity.y)
        if pos[0] < camera.width and \
            pos[1] < camera.height and \
            pos[0] + self.width > 0 and \
            pos[1] + self.height > 0:
            screen.blit(self.image, pos)

# Load things uniquely.
