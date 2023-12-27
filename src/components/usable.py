

class Action:
    def __init__(self, name, on):
        self.name = name
        self.on = on

class Usable:
    def __init__(self, obj_name):
        self.obj_name = obj_name
        from core.engine import engine
        engine.usables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.usables.remove(self)

    def on(self, other, distance):
        print("Base on function called")


class Choppable(Usable):
    def __init__(self, obj_name, chopped_image):
        super().__init__(obj_name)
        self.chopped_image = chopped_image
        self.is_chopped = False

    def on(self, other, distance):
        from components.player import Player
        from components.sprite import Sprite
        player = other.get(Player)
        if self.is_chopped:
            player.show_message("This tree is already chopped")
            return
        if distance < 60:
            player.show_message("Chopping " + self.obj_name)
            self.entity.get(Sprite).set_image(self.chopped_image)
            self.is_chopped = True
        else:
            player.show_message("I need to get closer")


class Minable(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)

    def on(self, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < 60:
            player.show_message("Mining " + self.obj_name)
            from core.area import area
            area.remove_entity(self.entity)
        else:
            player.show_message("I need to get closer")


class Enemy(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)

    def on(self, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < 60:
            player.show_message("Attacking " + self.obj_name)
        else:
            player.show_message("I need to get closer")