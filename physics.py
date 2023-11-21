from pygame import Rect

bodies = []

class Body:
    def __init__(self, x=0, y=0, width=32, height=32):
        self.hitbox = Rect(x, y, width, height)
        bodies.append(self)

    def is_position_valid(self):
        from map import map
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        if map.is_rect_solid(x, y, self.hitbox.width, self.hitbox.height):
            return False
        for body in bodies:
            if body != self and body.is_colliding_with(self):
                return False
        return True
    
    def is_colliding_with(self, other):
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        other_x = other.entity.x + other.hitbox.x
        other_y = other.entity.y + other.hitbox.y
        if x < other_x + other.hitbox.width and \
           x + self.hitbox.width > other_x and \
           y < other_y + other.hitbox.height and \
           y + self.hitbox.height > other_y:
            return True
        else:
            return False
