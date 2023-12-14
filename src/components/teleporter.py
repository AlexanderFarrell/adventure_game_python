from components.physics import Trigger
from components.player import Player

def teleport(area_file, player_x, player_y):
    from core.area import area
    area.load_file(area_file)
    if player_x is not None and player_y is not None:
        player = area.search_for_first(Player)
        player.x = player_x*32
        player.y = player_y*32


class Teleporter(Trigger):
    def __init__(self, area_file, player_x=None, player_y=None, x=0, y=0, width=32, height=32):
        super().__init__(lambda other: teleport(area_file, int(player_x), int(player_y)), x, y, width, height)
        print(area_file)
