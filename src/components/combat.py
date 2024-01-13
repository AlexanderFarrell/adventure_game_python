
class Combat:
    def __init__(self, health, on_death):
        self.health = health
        self.global_cooldown = 0
        self.equipped = None
        self.on_death = on_death

    def attack(self, other):
        if self.equipped == None:
            # If we don't have any weapon, don't attack
            # If you want to do code for unarmed attacks, 
            # put it here!
            return
        
        other.health -= int(self.equipped.stats['damage'])
        self.global_cooldown = self.equipped.stats['cooldown']
        print(f"Took {self.equipped.stats['damage']} damage. Has {other.health}")
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
        

