from core.camera import camera
import pygame

effects = []

hit_x_speed = 0
hit_y_speed = -1
hit_life = 60
hit_size = 30
hit_font = None
hit_font_file = "content/fonts/EBGaramond-Bold.ttf"

def create_hit_text(x, y, text, color=(255, 255, 255)):
    global hit_font
    if hit_font is None:
        hit_font = pygame.font.Font(hit_font_file, hit_size)
    image = hit_font.render(text, True, color)
    Effect(x, y, hit_x_speed, hit_y_speed, hit_life, image)


class Effect:
    def __init__(self, x, y, xspeed, yspeed, life, image):
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.life = life
        self.image = image
        global effects
        effects.append(self)

    def draw(self, screen):
        self.life -= 1
        self.x += self.xspeed
        self.y += self.yspeed
        if self.life <= 0:
            global effects
            effects.remove(self)
        screen.blit(self.image, (self.x - camera.x, self.y - camera.y))