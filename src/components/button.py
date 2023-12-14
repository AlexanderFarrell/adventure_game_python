import pygame

class Button:
    def __init__(self, on, click_area=pygame.Rect(0, 0, 32, 32)):
        from core.engine import engine
        engine.active_objs.append(self)
        self.click_area = click_area
        self.on = on

    def update(self):
        from core.input import is_mouse_pressed
        mouse_pos = pygame.mouse.get_pos()

        x = self.click_area.x + self.entity.x
        y = self.click_area.y + self.entity.y

        if is_mouse_pressed(0):
            if x <= mouse_pos[0] <= x + self.click_area.width and \
                y <= mouse_pos[1] <= y + self.click_area.height:
                self.on()