import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y, hitbox = None):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image)
            loaded[image] = self.image
        self.x = x
        self.y = y
        if hitbox is not None:
            self.hitbox = hitbox
        else:
            self.hitbox = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.bounds = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def refresh_bounds(self):
        self.bounds.x = self.x + self.hitbox.x
        self.bounds.y = self.y + self.hitbox.y
        self.bounds.width = self.hitbox.width
        self.bounds.height = self.hitbox.height

    def is_colliding_with(self, other):
        x = self.x + self.hitbox.x
        y = self.y + self.hitbox.y
        other_x = other.x + other.hitbox.x
        other_y = other.y + other.hitbox.y

        if x < other_x + other.hitbox.width and \
           x + self.hitbox.width > other_x and \
           y < other_y + other.hitbox.height and \
           y + self.hitbox.height > other_y:
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Load things uniquely.
