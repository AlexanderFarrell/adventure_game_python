from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter
from components.inventory import Inventory, DroppedItem
from data.item_types import item_types
from components.usable import Usable, Choppable, Minable
from components.enemy import Enemy
from components.npc import NPC

class EntityFactory:
    def __init__(self, name, factory, arg_names=[]):
        self.name = name
        self.factory = factory
        self.arg_names = arg_names

entity_factories = [
    # 0
    EntityFactory('Player', 
                 lambda args: Entity(Player(100), Sprite("player.png"), Body(8, 48, 16, 16)),
                 ), 

    # 1
    EntityFactory('Pine Tree', 
                 lambda args: Entity(Sprite("tree.png"), 
                        Body(16, 96, 32, 32), 
                        Choppable("Pine Tree", "tree_stump.png")), 
                 ),

    # 2
    EntityFactory('Rock',
                 lambda args: Entity(Sprite("rock.png"), Body(), Minable("Rock")), 
                 ), 

    # 3
    EntityFactory('Teleporter Up', 
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_up.png")),
                 ['Area File', 'Player X', 'Player Y']
                 ), 

    # 4
    EntityFactory('Teleporter Right', 
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_right.png")),
                 ['Area File', 'Player X', 'Player Y']
                 ), 

    # 5
    EntityFactory('Teleporter Down', 
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_down.png")),
                ['Area File', 'Player X', 'Player Y']
                ), 

    # 6
    EntityFactory('Teleporter Left', 
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_left.png")),
                 ['Area File', 'Player X', 'Player Y']
                 ), 

    # 7
    EntityFactory('Dropped Item', 
                 lambda args: Entity(DroppedItem(item_types[int(args[0])], int(args[1])), 
                        Sprite(item_types[int(args[0])].icon_name)),
                 ['Area File', 'Player X', 'Player Y']
                 ), 

    # 8
    EntityFactory('NPC', 
                 lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2])),
                ['Sprite', 'NPC Name', 'NPC File']
                ), 

    # 9
    EntityFactory('Enemy',
                 lambda args: Entity(Sprite(args[0]), Enemy(100, 4), Body(8, 48, 16, 16)),
                 ['Sprite']
                 )
]

def create_entity(id, x, y, data=None, index=None):
    factory = entity_factories[id].factory
    e =  factory(data)
    e.index = index
    e.x = x*32
    e.y = y*32
    return e

        