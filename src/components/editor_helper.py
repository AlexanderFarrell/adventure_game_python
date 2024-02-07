from core.input import is_key_pressed
import pygame

movement_speed = 8

class EditorHelper:
    def __init__(self):
        from core.engine import engine
        engine.active_objs.append(self)

    def update(self):
        from core.camera import camera
        if is_key_pressed(pygame.K_a):
            camera.x -= movement_speed
        if is_key_pressed(pygame.K_d):
            camera.x += movement_speed
        if is_key_pressed(pygame.K_w):
            camera.y -= movement_speed
        if is_key_pressed(pygame.K_s):
            camera.y += movement_speed
