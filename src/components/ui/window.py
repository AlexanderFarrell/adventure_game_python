from components.entity import Entity
from pygame import Surface

class Window:
    def __init__(self, width=32, height=32):
        self.width = width
        self.height = height
        self.items = []

    def draw(self, screen):
        screen.blit(self.surface, (self.entity.x, self.entity.y))

        
def create_window(x, y, width, height):
    return Entity(Window(width, height), x=x, y=y)