from components.button import create_simple_label_button
from data.tile_types import tile_kinds
from core.area import Area
from components.entity import Entity
from components.editor_helper import EditorHelper
from components.button import Button
from components.sprite import Sprite
from components.ui.scroll_view import ScrollView, create_scroll_sprite_generic
import pygame

filename = None
is_new = False
tool = "Click"
current_tile_index = 0
sidebar = None

def set_current_tile(item, index):
    global current_tile_index
    current_tile_index = index

def set_tool(new_tool):
    global tool, sidebar
    tool = new_tool
    print(f"Tool has been set to {tool}")
    if sidebar is not None:
        sidebar.delete_self()
    if tool == "Tile":
        from core.area import area
        from core.camera import camera
        image_names = [i.image_name for i in area.map.tile_kinds]
        sidebar = Entity(ScrollView(
            image_names,
            create_scroll_sprite_generic,
            set_current_tile,
            36,
            width=(32),
            height=camera.height
        ),
        x=camera.width-32-3-3)

def save_map():
    print("Saving not implemented yet.")

def prepare_map_editor(filename_in, is_new_in):
    global filename, is_new
    filename = filename_in
    is_new = is_new_in

def place_tile(mouse_x, mouse_y):
    # What tile is the mouse on?
    print("place tile called")

    from core.camera import camera
    x = mouse_x + camera.x
    y = mouse_y + camera.y
    from core.area import area
    area.map.set_tile(x, y, current_tile_index)

def place_entity(mouse_x, mouse_y):
    pass

def click_tool(mouse_x, mouse_y):
    pass

# User Interface
def back_button_press():
    from core.engine import engine
    engine.switch_to("EditorChooseFile")

def on_click():
    global tool
    print("On Click Called")
    mouse_pos = pygame.mouse.get_pos()
    from core.camera import camera
    if mouse_pos[0] > camera.width-(32+3+3) or (mouse_pos[0] < 64 and mouse_pos[1] < 64*4):
        return
    print(tool)
    if tool == "Click":
        click_tool(mouse_pos[0], mouse_pos[1])
    elif tool == "Tile":
        place_tile(mouse_pos[0], mouse_pos[1])

    
# Main Editor Stage
def edit_map():
    global helper
    print("Starting map editor")
    print(f"Filename: {filename} - Is New: {is_new}")

    if is_new:
        pass
    else:
        Area(filename, tile_kinds, editor_mode=True)

    from core.camera import camera
    Entity(EditorHelper(on_click)).get(EditorHelper)

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
    Entity(Button(lambda: back_button_press(),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('cancel.png', True),
           x=2,
           y=2+64*3)

    
