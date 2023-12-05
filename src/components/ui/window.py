from components.entity import Entity
from pygame import Surface

class Window:
    def __init__(self, width=32, height=32, color=(128, 128, 128)):
        self.width = width
        self.height = height
        self.color = color

        self.surface = Surface((width, height))
        self.surface.fill(color)
        from core.engine import engine
        #engine.ui_back_drawables.append(self)

        self.items = []

    def draw(self, screen):
        screen.blit(self.surface, (self.entity.x, self.entity.y))

        
def create_window(x, y, width, height, color=(128, 128, 128)):
    return Entity(Window(width, height, color), x=x, y=y)