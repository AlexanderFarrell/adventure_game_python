from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter
from components.inventory import Inventory, DroppedItem
from data.item_types import item_types
from components.usable import Usable, Choppable, Minable, NPC, Enemy


entity_factories = [
    # 0
    lambda args: Entity(Player(), Sprite("player.png"), Body(8, 48, 16, 16)),

    # 1
    lambda args: Entity(Sprite("tree.png"), 
                        Body(16, 96, 32, 32), 
                        Choppable("Pine Tree", "tree_stump.png")),      

    # 2
    lambda args: Entity(Sprite("rock.png"), Body(), Minable("Rock")), 

    # 3
    lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_up.png")),

    # 4
    lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_right.png")),

    # 5
    lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_down.png")),

    # 6
    lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_left.png")),

    # 7
    lambda args: Entity(DroppedItem(item_types[int(args[0])], int(args[1])), Sprite(item_types[int(args[0])].icon_name))
]

def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e =  factory(data)
    e.x = x*32
    e.y = y*32
    return e

        