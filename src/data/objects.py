from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter


entity_factories = [
    # 0
    lambda args: Entity(Player(), Sprite("player.png"), Body(8, 48, 16, 16)),

    # 1
    lambda args: Entity(Sprite("tree.png"), Body(16, 96, 32, 32)),      

    # 2
    lambda args: Entity(Sprite("rock.png"), Body()), 

    # 3
    lambda args: Entity(Teleporter("another.map"))
]

def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e =  factory(data)
    e.x = x*32
    e.y = y*32
    return e

        