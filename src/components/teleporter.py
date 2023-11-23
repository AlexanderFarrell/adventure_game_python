from components.physics import Trigger


def teleport(area_file):
    from core.area import area
    area.load_file(area_file)
    print(area_file)


class Teleporter(Trigger):
    def __init__(self, area_file, x=0, y=0, width=32, height=32):
        super().__init__(lambda: teleport(area_file), x, y, width, height)
