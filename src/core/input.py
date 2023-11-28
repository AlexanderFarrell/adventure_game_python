# Keeps track of what key is down
keys_down = set()
mouse_buttons_down = set()
import pygame

def is_key_pressed(key):
    return key in keys_down

def is_mouse_pressed(button):
    return pygame.mouse.get_pressed()[button]