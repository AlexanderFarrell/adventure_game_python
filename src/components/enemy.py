import random
from components.physics import Body
from data.item_types import item_types
from core.math_ext import distance

def on_enemy_death(entity):
    from core.area import area
    area.remove_entity(entity)
    print("Called Death")

class Enemy:
    def __init__(self, health, weapon_item_id) -> None:
        self.health = health
        self.weapon = item_types[weapon_item_id]
        self.target = None
        self.targeted_entity = None
        from core.engine import engine
        engine.active_objs.append(self)
        self.step_to_update = random.randint(0, 30)
        self.vision_range = 500
        self.walk_speed = 0.5

    def setup(self):
        from components.combat import Combat
        self.entity.add(Combat(self.health, on_enemy_death))
        self.combat = self.entity.get(Combat)
        self.combat.equip(self.weapon)
        del self.health

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)

    def update_ai(self):
        from components.physics import get_bodies_within_circle
        from components.player import Player
        seen_objects = get_bodies_within_circle(self.entity.x, self.entity.y, self.vision_range)
        found_player = False
        for s in seen_objects:
            if s.entity.has(Player):
                self.target = (s.entity.x, s.entity.y)
                self.targeted_entity = s.entity
                found_player = True
        
        if not found_player:
            self.target = None
            self.targeted_entity = None

    def update(self):
        # Don't update as fast
        from core.engine import engine

        if engine.step % 30 == self.step_to_update:
            self.update_ai()

        if self.targeted_entity is not None:
            weapon_range = int(self.combat.equipped.stats['range'])
            dist = distance(self.entity.x, self.entity.y, 
                            self.targeted_entity.x,
                            self.targeted_entity.y)
            if weapon_range > dist:
                from components.combat import Combat
                self.combat.attack(self.targeted_entity.get(Combat))
            
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
