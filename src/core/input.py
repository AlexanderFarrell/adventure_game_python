# Keeps track of what key is down
keys_down = set()
mouse_buttons_down = set()
mouse_buttons_just_pressed = set()
import pygame

def is_key_pressed(key):
    return key in keys_down

def is_mouse_pressed(button):
    return pygame.mouse.get_pressed()[button]

def is_mouse_just_pressed(button):
    return button in mouse_buttons_just_pressed