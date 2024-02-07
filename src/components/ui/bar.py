import pygame

class Bar:
    def __init__(self, max, back_color, front_color, width=300, height=20):
        self.amount = max
        self.max = max
        self.back_color = back_color
        self.front_color = front_color
        self.width = width
        self.height = height
        from core.engine import engine
        engine.ui_drawables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.ui_drawables.remove(self)


    def draw(self, screen):
        # Figure out amount
        filled = self.amount / self.max

        # Draw background first
        pygame.draw.rect(screen, 
                         self.back_color, 
                         pygame.Rect(self.entity.x, 
                                     self.entity.y, 
                                     self.width, 
                                     self.height))
        # Then foreground
        pygame.draw.rect(screen, 
                         self.front_color, 
                         pygame.Rect(self.entity.x, 
                                     self.entity.y, 
                                     self.width*filled, 
                                     self.height))
        
