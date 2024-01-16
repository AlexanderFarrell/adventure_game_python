
class Combat:
    def __init__(self, health, on_death):
        self.health = health
        self.max_health = health
        self.global_cooldown = 0
        self.equipped = None
        self.regen = 0.01
        self.on_death = on_death
        from core.engine import engine
        engine.active_objs.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)

    def attack(self, other):
        if self.equipped == None:
            # If we don't have any weapon, don't attack
            # If you want to do code for unarmed attacks, 
            # put it here!
            return
        
        # If we are still on cooldown
        if self.global_cooldown > 0:
            return
        
        damage = int(self.equipped.stats['damage'])
        other.health -= damage
        self.global_cooldown = self.equipped.stats['cooldown']*60
        print(self.global_cooldown)

        from core.effect import create_hit_text, Effect
        create_hit_text(other.entity.x, other.entity.y, str(damage), (255, 0, 0))
        # Effect(self.entity.x, self.entity.y, 0, 0, 5, self.equipped.icon)

        print(f"Took {damage} damage. Has {other.health}")
        if other.health <= 0:
            other.on_death(other.entity)

    def perform_attack(self):
        if self.equipped == None:
            # If we don't have any weapon, don't attack
            # If you want to do code for unarmed attacks, 
            # put it here!
            return
        
        from components.physics import get_bodies_within_circle
        nearby_objs = get_bodies_within_circle(self.entity.x, 
                                               self.entity.y, 
                                               self.equipped.stats['range'])
        print("Nearby Objs", nearby_objs)
        for o in nearby_objs:
            print(o.entity.components)
            if o.entity.has(Combat) and o.entity != self.entity:
                self.attack(o.entity.get(Combat))
        
    def update(self):
        if self.global_cooldown > 0:
            self.global_cooldown -= 1
        if self.health < self.max_health:
            self.health += self.regen
        if self.health > self.max_health:
            self.health = self.max_health
        

