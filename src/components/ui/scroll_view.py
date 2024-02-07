import pygame

padding = 3
border_color = (0, 0, 0)
background_color = (40, 180, 200)
sensitivity = 16

def create_scroll_label_generic(item, scroll_view):
    from components.entity import Entity
    from components.label import Label
    return Entity(Label("EBGaramond-Regular.ttf", item, scroll_view.item_size))

class ScrollView:
    # Items
    def __init__(self, items, on_create, on_choose, item_size, width=200, height=500):
        self.items = items
        self.child_entities = []
        self.on_create = on_create
        self.on_choose = on_choose
        self.inner_y = 0
        self.item_size = item_size

        self.click_area = pygame.rect.Rect(0, 0, width+padding*2, height+padding*2)
        self.background = pygame.surface.Surface((width+padding*2, height+padding*2))
        self.background.fill(border_color)
        pygame.draw.rect(self.background, 
                         background_color, 
                         pygame.rect.Rect(1, 1, self.background.get_width()-2, self.background.get_height()-2))
        self.surface = pygame.surface.Surface((width+padding*2, height+padding*2))
        
        from core.engine import engine
        engine.active_objs.append(self)
        engine.ui_drawables.append(self)

    def setup(self):
        self.drawables = []
        for i, item in enumerate(self.items):
            entity = self.on_create(item, self)
            entity.y = i * self.item_size
            # Reassign any drawables to us
            from core.engine import engine
            for c in entity.components:
                if c in engine.ui_drawables:
                    engine.ui_drawables.remove(c)
                    self.drawables.append(c)
            self.child_entities.append(entity)

    def get_scroll_max(self):
        return self.item_size * len(self.items) + self.click_area.height * 0.5

    def update(self):
        from core.input import is_mouse_pressed, is_key_just_pressed
        from core.engine import engine
        mouse_pos = pygame.mouse.get_pos()

        x = self.click_area.x + self.entity.x
        y = self.click_area.y + self.entity.y

        if x <= mouse_pos[0] <= x + self.click_area.width and \
            y <= mouse_pos[1] <= y + self.click_area.height:
            from core.input import scroll_delta
            self.inner_y -= scroll_delta * sensitivity
            # Clamp the position
            m = self.get_scroll_max()
            if self.inner_y < 0:
                self.inner_y = 0
            if self.inner_y > m:
                self.inner_y = m
            print(self.inner_y)
            for i, entity in enumerate(self.child_entities):
                entity.y = i * self.item_size - self.inner_y


    def draw(self, screen):
        self.surface.blit(self.background, (0, 0))
        for d in self.drawables:
            d.draw(self.surface)
        screen.blit(self.surface, (self.entity.x, self.entity.y))


    
