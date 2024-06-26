import pygame
from components.sprite import Sprite
from core.input import is_key_pressed
from core.camera import camera
from components.entity import Entity
from components.label import Label
from components.physics import Body, triggers
from core.area import area


movement_speed = 2

class Player:
    def __init__(self):
        self.loc_label = Entity(Label("main/EBGaramond-Regular.ttf", 
                                         "X: 0 - Y: 0")).get(Label)
        self.area_label = Entity(Label("main/EBGaramond-Regular.ttf", 
                                       area.name)).get(Label)
        
        from core.camera import camera
        self.loc_label.entity.y = camera.height - 50

        self.loc_label.entity.x = 10
        self.area_label.entity.x = 10
        
        from core.engine import engine
        engine.active_objs.append(self)

    def update(self):
        self.loc_label.set_text(f"X: {self.entity.x} - Y: {self.entity.y}")
        previous_x = self.entity.x
        previous_y = self.entity.y
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)

        if is_key_pressed(pygame.K_w):
            self.entity.y -= movement_speed
        if is_key_pressed(pygame.K_s):
            self.entity.y += movement_speed
        if not body.is_position_valid():
            self.entity.y = previous_y

        if is_key_pressed(pygame.K_a):
            self.entity.x -= movement_speed
        if is_key_pressed(pygame.K_d):
            self.entity.x += movement_speed
        if not body.is_position_valid():
            self.entity.x = previous_x
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2

        for t in triggers:
            if body.is_colliding_with(t):
                t.on()

