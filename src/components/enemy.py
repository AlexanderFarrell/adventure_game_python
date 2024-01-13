import random
from components.physics import Body

def on_enemy_death(entity):
    from core.area import area
    area.remove_entity(entity)
    print("Called Death")

class Enemy:
    def __init__(self, health) -> None:
        self.health = health
        self.target = None
        from core.engine import engine
        engine.active_objs.append(self)
        self.step_to_update = random.randint(0, 30)
        self.vision_range = 200
        self.walk_speed = 0.5

    def setup(self):
        from components.combat import Combat
        self.combat = self.entity.add(Combat(self.health, on_enemy_death))
        del self.health

    def update_ai(self):
        from components.physics import get_bodies_within_circle
        from components.player import Player
        seen_objects = get_bodies_within_circle(self.entity.x, self.entity.y, self.vision_range)
        found_player = False
        for s in seen_objects:
            if s.entity.has(Player):
                self.target = (s.entity.x, s.entity.y)
                found_player = True
        
        if not found_player:
            self.target = None

    def update(self):
        # Don't update as fast
        from core.engine import engine

        if engine.step % 30 == self.step_to_update:
            self.update_ai()

        if self.target is not None:
            body = self.entity.get(Body)
            prev_x = self.entity.x
            prev_y = self.entity.y
            if self.entity.x < self.target[0]:
                self.entity.x += self.walk_speed
            if self.entity.x > self.target[0]:
                self.entity.x -= self.walk_speed
            if not body.is_position_valid():
                self.entity.x = prev_x

            if self.entity.y < self.target[1]:
                self.entity.y += self.walk_speed
            if self.entity.y > self.target[1]:
                self.entity.y -= self.walk_speed
            if not body.is_position_valid():
                self.entity.y = prev_y
