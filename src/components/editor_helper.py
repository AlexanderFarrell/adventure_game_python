from core.input import is_key_pressed
from components.entity import Entity
import pygame

movement_speed = 8

# Moves the camera, and also handles mouse clicks in the world.
class EditorHelper:
    def __init__(self, on_click):
        from core.engine import engine
        engine.active_objs.append(self)
        self.on_click = on_click

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

        from core.input import is_mouse_pressed
        if is_mouse_pressed(0):
            self.on_click()

    def switch_tool(self, tool):
        if self.sidebar is not None:
            self.sidebar.delete_self()
        # if tool == 'tiles':
            # self.sidebar = Entity(PlaceTiles())