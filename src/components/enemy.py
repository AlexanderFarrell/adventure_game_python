
def on_enemy_death(entity):
    from core.area import area
    area.remove_entity(entity)
    print("Called Death")

class Enemy:
    def __init__(self, health) -> None:
        self.health = health

    def setup(self):
        from components.combat import Combat
        self.combat = self.entity.add(Combat(self.health, on_enemy_death))
        del self.health