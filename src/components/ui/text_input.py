from components.label import Label
import pygame

background_color = (11,11,11)
border_color = (255, 255, 255)
padding = 5
cursor_width = 2

class TextInput(Label):
    def __init__(self, font, text="", size=32, max_text=20, width=400, color=(255, 255, 255), on_change=None):
        super().__init__(font, text, size, color)
        self.on_change = on_change
        self.active = False
        self.text = text
        self.max_text = max_text
        from core.engine import engine
        from core.input import text_input_listeners
        text_input_listeners.append(self)
        engine.active_objs.append(self)
        self.width = 200
        self.blink_step = False

        self.click_area = pygame.rect.Rect(0, 0, self.width+padding*2, size+padding*2)
        self.cursor = pygame.surface.Surface((cursor_width, size))
        self.cursor.fill(color)

        self.background = pygame.surface.Surface((width+padding*2, size+padding*2))
        self.background.fill(border_color)
        pygame.draw.rect(self.background, 
                         background_color, 
                         pygame.rect.Rect(1, 1, self.background.get_width()-2, self.background.get_height()-2))

    def update(self):
        from core.input import is_mouse_pressed, is_key_just_pressed
        from core.engine import engine
        mouse_pos = pygame.mouse.get_pos()

        if self.active and is_key_just_pressed(pygame.K_BACKSPACE):
            self.set_text(self.text[:-1])

        self.blink_step = engine.step % 120 > 60

        x = self.click_area.x + self.entity.x
        y = self.click_area.y + self.entity.y

        if is_mouse_pressed(0):
            if x <= mouse_pos[0] <= x + self.click_area.width and \
                y <= mouse_pos[1] <= y + self.click_area.height:
                self.active = True
            else:
                self.active = False


    def text_input(self, text):
        if not self.active:
            return
        self.text += text
        if len(self.text) > self.max_text:
            self.text = self.text[:20]
        self.set_text(self.text)
        if self.on_change is not None:
            self.on_change()

    def breakdown(self):
        from core.input import text_input_listeners
        text_input_listeners.remove(self)
        from core.engine import engine
        engine.ui_drawables.remove(self)

    def draw(self, screen):
        screen.blit(self.background, (self.entity.x, self.entity.y))
        super().draw(screen)
        if self.blink_step and self.active:
            screen.blit(self.cursor, (self.entity.x + self.surface.get_width() + padding, 
                                      self.entity.y + padding))



