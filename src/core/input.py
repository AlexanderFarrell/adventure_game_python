# Keeps track of what key is down
keys_down = set()
keys_just_pressed = set()
mouse_buttons_down = set()
mouse_buttons_just_pressed = set()
text_input_listeners = []
scroll_delta = 0
import pygame

def is_key_pressed(key):
    return key in keys_down

def is_key_just_pressed(key):
    return key in keys_just_pressed

def is_mouse_pressed(button):
    return pygame.mouse.get_pressed()[button]

def is_mouse_just_pressed(button):
    return button in mouse_buttons_just_pressed

def add_scroll_delta(amount):
    global scroll_delta
    scroll_delta += amount
    print(scroll_delta)

def reset_scroll():
    global scroll_delta
    scroll_delta = 0