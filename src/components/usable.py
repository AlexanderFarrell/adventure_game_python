

class Action:
    def __init__(self, name, on):
        self.name = name
        self.on = on

class Usable:
    def __init__(self, obj_name, action):
        self.obj_name = obj_name
        self.action = action
        from core.engine import engine
        engine.usables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.usables.remove(self)


class Choppable(Usable):
    @staticmethod
    def on(subject, other, distance):
        from components.player import Player
        from components.sprite import Sprite
        player = other.get(Player)
        if subject.is_chopped:
            player.show_message("This tree is already chopped")
            return
        if distance < 60:
            player.show_message("Chopping " + subject.obj_name)
            subject.entity.get(Sprite).set_image(subject.chopped_image)
            subject.is_chopped = True
        else:
            player.show_message("I need to get closer")
    action = Action("Chop", on)
    
    def __init__(self, obj_name, chopped_image):
        super().__init__(obj_name, Choppable.action)
        self.chopped_image = chopped_image
        self.is_chopped = False


class Minable(Usable):
    @staticmethod
    def on(subject, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < 60:
            player.show_message("Mining " + subject.obj_name)
        else:
            player.show_message("I need to get closer")
    action = Action("Mine", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, Minable.action)


class NPC(Usable):
    @staticmethod
    def on(subject, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < 60:
            player.show_message("Talking to " + subject.obj_name)
        else:
            player.show_message("I need to get closer")
    action = Action("Talk to", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, NPC.action)


class Enemy(Usable):
    def on(subject, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < 60:
            player.show_message("Attacking " + subject.obj_name)
        else:
            player.show_message("I need to get closer")
    action = Action("Attack", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, Enemy.action)