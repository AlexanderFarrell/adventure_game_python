from components.button import create_simple_label_button
from data.tile_types import tile_kinds
from core.area import Area
from components.entity import Entity
from components.editor_helper import EditorHelper
from components.color_back import ColorBackground
from components.button import Button
from components.sprite import Sprite
import pygame

filename = None
is_new = False
current_tool = 'Click'

def prepare_map_editor(filename_in, is_new_in):
    global filename, is_new
    filename = filename_in
    is_new = is_new_in

def back():
    from core.engine import engine
    engine.switch_to("EditorChooseFile")

def set_tool(tool):
    global current_tool
    current_tool=tool
    print(f"Tool has been set to {current_tool}")

def edit_map():
    print("Starting map editor")
    print(f"Filename: {filename} - Is New: {is_new}")

    if is_new:
        pass
    else:
        Area(filename, tile_kinds, editor_mode=True)

    from core.camera import camera
    Entity(EditorHelper())
    # Entity(ColorBackground(64, camera.height, (100, 50, 0)))

    Entity(Button(lambda: set_tool('Click'),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('mouse_tool.png', True),
           x=2,
           y=2+64*0)
    Entity(Button(lambda: set_tool("Tile"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('tile_tool.png', True),
           x=2,
           y=2+64*1)
    Entity(Button(lambda: set_tool("Save"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('save.png', True),
           x=2,
           y=2+64*2)
    Entity(Button(lambda: back(),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('cancel.png', True),
           x=2,
           y=2+64*3)
