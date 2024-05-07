import pygame
pygame.init()

engine = None
default_width = 1280
default_height = 720

class Engine:
    def __init__(self, game_title) -> None:
        from core.camera import create_screen
        global engine
        engine = self
        self.step = 0

        self.active_objs = [] # Anything with an update() method which can be called

        # Layers of what order things are drawn. UI Drawables draw over Background for example
        self.background_drawables = []
        self.drawables = [] # Anything to be drawn in the world
        self.ui_drawables = [] # Anything to be drawn over the world

        self.usables = []

        self.effects = []

        self.clear_color = (30, 150, 240) # Default color if nothing else is drawn somewhere
        self.screen = create_screen(default_width, default_height, game_title) # The rectangle in the window itself
        self.stages = {}
        self.current_stage = None

    def register(self, stage_name, func):
        self.stages[stage_name] = func

    def switch_to(self, stage_name):
        from core.area import area
        area = None
        self.reset()
        self.current_stage = stage_name 
        func = self.stages[stage_name]
        print(f"Switching to {self.current_stage}")
        func()

    def run(self):
        from core.input import keys_down, mouse_buttons_down, \
                mouse_buttons_just_pressed, keys_just_pressed, \
                reset_scroll
        self.running = True
        while self.running:
            reset_scroll()
            mouse_buttons_just_pressed.clear()
            keys_just_pressed.clear()
            self.step += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                    keys_just_pressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    keys_down.remove(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons_down.add(event.button)
                    mouse_buttons_just_pressed.add(event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_buttons_down.remove(event.button)
                elif event.type == pygame.MOUSEWHEEL:
                    from core.input import add_scroll_delta
                    add_scroll_delta(event.y)
                elif event.type == pygame.TEXTINPUT:
                    from core.input import text_input_listeners
                    for t in text_input_listeners:
                        t.text_input(event.text)

            # Update Code
            for a in self.active_objs:
                a.update()

            # Draw Code
            self.screen.fill(self.clear_color)
            
            # Draw background items like the tiles
            for b in self.background_drawables:
                b.draw(self.screen)

            # Draw the main objects
            for s in self.drawables:
                s.draw(self.screen)

            # Draw Effects
            from core.effect import effects
            for e in effects:
                e.draw(self.screen)

            # Draw UI Stuff
            for l in self.ui_drawables:
                l.draw(self.screen)


            pygame.display.flip()

            # Cap the frames
            pygame.time.delay(17)
                
        pygame.quit()


    def reset(self):
        from core.area import area
        if area is not None:
            e = area.entities.copy()
            for a in e:
                a.delete_self()
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()
        self.usables.clear()
        self.effects.clear()
        from core.effect import effects
        effects.clear()