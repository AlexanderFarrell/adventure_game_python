from components.entity import Entity
from components.sprite import Sprite, Animation
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter
from components.inventory import Inventory, DroppedItem
from data.item_types import item_types
from components.usable import Usable, Choppable, Minable
from components.enemy import Enemy
from components.npc import NPC

class EntityFactory:
    def __init__(self, name, icon, factory, arg_names=[], defaults=[]):
        self.name = name
        self.icon = icon
        self.factory = factory
        self.arg_names = arg_names
        self.defaults = defaults

entity_factories = [
    # 0
    EntityFactory('Player', 
                  "player.png",
                 lambda args: Entity(Player(100), Animation("player_sheet2.png", 32, 64, [(0, 0)], 10), Body(8, 48, 16, 16)),
                 ), 

    # 1
    EntityFactory('Pine Tree', 
                  'tree.png',
                 lambda args: Entity(Sprite("tree.png"), 
                        Body(16, 96, 32, 32), 
                        Choppable("Pine Tree", "tree_stump.png")), 
                 ),

    # 2
    EntityFactory('Rock',
                  'rock.png',
                 lambda args: Entity(Sprite("rock.png"), Body(), Minable("Rock")), 
                 ), 

    # 3
    EntityFactory('Teleporter Up',
                  'teleporter_up.png', 
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_up.png")),
                 ['Area File', 'Player X', 'Player Y'],
                 ['forest.map', '1', '1']
                 ), 

    # 4
    EntityFactory('Teleporter Right',
                  'teleporter_right.png', 
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_right.png")),
                 ['Area File', 'Player X', 'Player Y'],
                 ['forest.map', '1', '1']
                 ), 

    # 5
    EntityFactory('Teleporter Down', 
                  'teleporter_down.png',
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_down.png")),
                ['Area File', 'Player X', 'Player Y'],
                 ['forest.map', '1', '1']
                ), 

    # 6
    EntityFactory('Teleporter Left', 
                  'teleporter_left.png',
                 lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleporter_left.png")),
                 ['Area File', 'Player X', 'Player Y'],
                 ['forest.map', '1', '1']
                 ), 

    # 7
    EntityFactory('Dropped Item', 
                  'diamond.png',
                 lambda args: Entity(DroppedItem(item_types[int(args[0])], int(args[1])), 
                        Sprite(item_types[int(args[0])].icon_name)),
                 ['Item Type ID', 'Quantity'],
                 ['1', '1']
                 ), 

    # 8
    EntityFactory('NPC', 
                  'npc_female1.png',
                 lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2])),
                ['NPC Name', 'Sprite', 'NPC File'],
                 ['Amy', "npc_female1.png", 'amy.npc']
                ), 

    # 9
    EntityFactory('Enemy',
                  'npc_female2.png',
                 lambda args: Entity(Sprite(args[0]), Enemy(100, 4), Body(8, 48, 16, 16)),
                 ['Sprite'],
                 ['npc_female2.png']
                 )
]

def create_entity(id, x, y, data=None, index=None):
    factory = entity_factories[id].factory
    e =  factory(data)
    e.index = index
    e.x = x*32
    e.y = y*32
    return e

        