

class Entity:
    def __init__(self, *components, x=0, y=0):
        self.components = []
        self.x = x
        self.y = y
        for c in components:
            self.add(c, False)
        for c in components:
            g = getattr(c, "setup", None)
            if callable(g):
                c.setup()

    def delete_self(self):
        from core.area import area
        if self in area.entities:
            area.entities.remove(self)
        for c in self.components:
            g = getattr(c, "breakdown", None)
            if callable(g):
                c.breakdown()
        self.components.clear()
        print("called delete self")

    def add(self, component, perform_setup=True):
        component.entity = self
        self.components.append(component)
        if perform_setup:
            g = getattr(component, "setup", None)
            if callable(g):
                component.setup()

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
