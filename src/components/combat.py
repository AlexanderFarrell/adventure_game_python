from core.sound import Sound

class Combat:
    def __init__(self, health, on_death):
        self.health = health
        self.max_health = health
        self.global_cooldown = 0
        self.equipped = None
        self.regen = 0.01
        self.on_death = on_death
        self.weapon_sprite = None
        self.sound = None
        from core.engine import engine
        engine.active_objs.append(self)

    def equip(self, item):
        from components.entity import Entity
        from components.sprite import Sprite
        self.equipped = item
        if self.equipped is None:
            return
        print("equipping", self.equipped)
        if 'sound' in self.equipped.stats:
            self.sound = Sound(self.equipped.stats['sound'])
        self.weapon_sprite = Entity(Sprite(self.equipped.icon_name)).get(Sprite)

    def unequip(self):
        print("calling unequip")
        self.equipped = None    
        self.weapon_sprite = None
        self.sound = None
        print("Weapon sprite", self.weapon_sprite)
            

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        self.weapon_sprite = None

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
        if self.sound is not None:
            self.sound.play()

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
        
        if not 'range' in self.equipped.stats:
            # Weapon has no range
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
            
        if self.weapon_sprite is not None:
            self.weapon_sprite.entity.x = self.entity.x
            self.weapon_sprite.entity.y = self.entity.y + 16
        

