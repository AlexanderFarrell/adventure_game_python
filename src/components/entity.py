active_objs = []

class Entity:
    def __init__(self, *components, x=0, y=0):
        self.components = []
        self.x = x
        self.y = y
        for c in components:
            self.add(c)

    def add(self, component):
        component.entity = self
        self.components.append(component)

    def remove(self, kind):
        c = self.get(kind)
        if c is not None:
            c.entity = None
            self.components.remove(c)

    def has(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return True
        return False

    def get(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return c
        return None    
        
