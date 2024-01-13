from pygame import Rect

bodies = []
triggers = []

def reset_physics():
    global bodies, triggers
    bodies.clear()
    triggers.clear()

def get_bodies_within_circle(circle_x, circle_y, radius):
    items = []
    for body in bodies:
        if body.is_circle_colliding_with(circle_x, circle_y, radius):
            items.append(body)
    return items


class PhysicalObj:
    def __init__(self, x, y, width, height):
        self.hitbox = Rect(x, y, width, height)

    def is_circle_colliding_with(self, circle_x, circle_y, radius):
        # Credit: https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection
        body_x = self.entity.x + self.hitbox.x
        body_y = self.entity.y + self.hitbox.y
        circle_dist_x = abs(circle_x - body_x)
        circle_dist_y = abs(circle_y - body_y)

        if circle_dist_x > (self.hitbox.width/2 + radius):
            return False

        if circle_dist_y > (self.hitbox.height/2 + radius):
            return False
        
        if circle_dist_x <= (self.hitbox.width/2):
            return True
        
        if circle_dist_y <= (self.hitbox.height/2):
            return True
        
        corner_dist_squared = (circle_dist_x - self.hitbox.width/2)**2 + \
                              (circle_dist_y - self.hitbox.height/2)**2

        return corner_dist_squared <= radius**2

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


class Trigger(PhysicalObj):
    def __init__(self, on, x=0, y=0, width=32, height=32):
        super().__init__(x, y, width, height)
        triggers.append(self)
        self.on = on

    def breakdown(self):
        global triggers
        triggers.remove(self)

    # def __del__(self):
    #     triggers.remove(self)


class Body(PhysicalObj):
    def __init__(self, x=0, y=0, width=32, height=32):
        super().__init__(x, y, width, height)
        bodies.append(self)

    def breakdown(self):
        global bodies
        bodies.remove(self)

    def is_position_valid(self):
        from core.area import area
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        if area.map.is_rect_solid(x, y, self.hitbox.width, self.hitbox.height):
            return False
        for body in bodies:
            if body != self and body.is_colliding_with(self):
                return False
        return True

    # def __del__(self):
    #     bodies.remove(self)
    
    
