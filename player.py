import pygame
from sprite import Sprite, sprites
from input import is_key_pressed

movement_speed = 2

class Player(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.bounds = pygame.Rect(0, 0, 0, 0)

    def update(self, map):
        previous_x = self.x
        previous_y = self.y
        if is_key_pressed(pygame.K_w):
            self.y -= movement_speed
        if is_key_pressed(pygame.K_s):
            self.y += movement_speed
        if is_key_pressed(pygame.K_a):
            self.x -= movement_speed
        if is_key_pressed(pygame.K_d):
            self.x += movement_speed
        self.refresh_bounds()
        for sprite in sprites:
            if sprite != self and sprite.is_colliding_with(self):
                self.x = previous_x
                self.y = previous_y
                return
        if map.is_rect_solid(self.bounds):
            self.x = previous_x
            self.y = previous_y

