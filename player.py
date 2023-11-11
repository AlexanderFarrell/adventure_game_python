import pygame
from sprite import Sprite
from input import is_key_pressed

movement_speed = 2

class Player(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        if is_key_pressed(pygame.K_w):
            self.y -= movement_speed
        if is_key_pressed(pygame.K_s):
            self.y += movement_speed
        if is_key_pressed(pygame.K_a):
            self.x -= movement_speed
        if is_key_pressed(pygame.K_d):
            self.x += movement_speed

