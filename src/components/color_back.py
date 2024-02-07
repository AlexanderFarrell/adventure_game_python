import pygame

class ColorBackground:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(color)

        from core.engine import engine
        engine.ui_drawables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.ui_drawables.remove(self)

    def draw(self, screen):
        screen.blit(self.surface, (self.entity.x, self.entity.y))