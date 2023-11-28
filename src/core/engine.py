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

        self.active_objs = [] # Anything with an update() method which can be called

        self.background_drawables = []
        self.drawables = [] # Anything to be drawn in the world
        self.ui_drawables = [] # Anything to be drawn over the world

        self.clear_color = (30, 150, 240) # Default color if nothing else is drawn somewhere
        self.screen = create_screen(default_width, default_height, game_title) # The rectangle in the window itself
        self.states = {}
        self.current_state = None

    def register(self, state_name, func):
        self.states[state_name] = func

    def switch_to(self, state_name):
        from core.area import area
        area = None
        self.reset()
        self.current_state = state_name 
        func = self.states[state_name]
        print(f"Switching to {self.current_state}")
        func()

    def run(self):
        from core.input import keys_down

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                elif event.type == pygame.KEYUP:
                    keys_down.remove(event.key)

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

            # Draw UI Stuff
            for l in self.ui_drawables:
                l.draw(self.screen)

            pygame.display.flip()

            # Cap the frames
            pygame.time.delay(17)

            # if self.next_state is not None:
                
        pygame.quit()


    def reset(self):
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()