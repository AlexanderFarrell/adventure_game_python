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

    # def validate_position(self):
    #     for body in bodies:
    #         self.validate_position_with(body)

    # def validate_position_with(self, other):
    #     left = self.entity.x + self.hitbox.x
    #     top = self.entity.y + self.hitbox.y
    #     right = left + self.hitbox.width
    #     bottom = top + self.hitbox.height

    #     o_left = other.entity.x + other.hitbox.x
    #     o_top = other.entity.y + other.hitbox.y
    #     o_right = o_left + other.hitbox.width
    #     o_bottom = o_top + other.hitbox.height

    #     is_in_x = o_left < left < o_right or o_left < right < o_right
    #     is_in_y = o_top < top < o_bottom or o_top < bottom < o_bottom

    #     if is_in_x and o_top < top < o_bottom:
    #         self.entity.y = o_bottom
    #         print(left, top, right, bottom, o_left, o_top, o_right, o_bottom)
    #     if is_in_x and o_top < bottom < o_bottom:
    #         self.entity.y = o_top - self.hitbox.height
    #         print(left, top, right, bottom, o_left, o_top, o_right, o_bottom)
    #     if is_in_y and o_left < left < o_right:
    #         self.entity.x = o_right
    #         print(left, top, right, bottom, o_left, o_top, o_right, o_bottom)
    #     if is_in_y and o_left < right < o_right:
    #         self.entity.x = o_left - self.hitbox.width
    #         print(left, top, right, bottom, o_left, o_top, o_right, o_bottom)
        

        
