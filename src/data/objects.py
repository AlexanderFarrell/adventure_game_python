from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter


entity_factories = [
    # 0
    lambda x, y, *data: Entity(Player(), Sprite("player.png"), Body(8, 48, 16, 16), x=x, y=y),

    # 1
    lambda x, y, *data: Entity(Sprite("tree.png"), Body(16, 96, 32, 32), x=x, y=y),      

    # 2
    lambda x, y, *data: Entity(Sprite("rock.png"), Body(), x=x, y=y), 

    # 3
    lambda x, y, *data: Entity(Teleporter(data[3]), x=x, y=y)
]

def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    return factory(x*32, y*32, data)

        