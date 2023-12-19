

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
        if distance < 60:
            print("Chopping " + subject.obj_name)
        else:
            print("I need to get closer")
    action = Action("Chop", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, Choppable.action)


class Minable(Usable):
    @staticmethod
    def on(subject, other, distance):
        if distance < 60:
            print("Mining " + subject.obj_name)
        else:
            print("I need to get closer")
    action = Action("Mine", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, Minable.action)


class NPC(Usable):
    @staticmethod
    def on(subject, other, distance):
        if distance < 60:
            print("Talking to " + subject.obj_name)
        else:
            print("I need to get closer")
    action = Action("Talk to", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, NPC.action)


class Enemy(Usable):
    def on(subject, other, distance):
        if distance < 60:
            print("Attacking " + subject.obj_name)
        else:
            print("I need to get closer")
    action = Action("Attack", on)
    
    def __init__(self, obj_name):
        super().__init__(obj_name, Enemy.action)