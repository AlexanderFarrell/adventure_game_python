from data.tile_types import tile_kinds
from core.area import Area
from components.editor_helper import EditorHelper
from components.entity import Entity
from components.button import Button
from components.sprite import Sprite
from components.label import Label
from components.ui.scroll_view import ScrollView, create_scroll_sprite_generic
from components.ui.text_input import TextInput
import pygame

# ---- Map Editor Fields ----
filename = None             # The map file being worked on
tool = "Click"              # What should happen when you click 
current_tile_index = 0      # The current tile to place with the Tile tool
current_entity_index = 0    # The current entity to place with the Entity tool
tool_entities = None        # Any UI Entities used in the current tool
field_one = None            # A potential text field for the current tool
selected_entity = None      # The current entity selected by the click tool

# ---- Setters ----
# Changes a tile to the one selected in the scroll view
def set_filename(filename_in):
    global filename
    filename = filename_in

def set_current_tile(item, index):
    global current_tile_index
    current_tile_index = index

def set_entity(item, index):
    global current_entity_index
    current_entity_index = index

# Sets the current tool
def set_tool(new_tool):
    global tool, tool_entities, field_one
    tool = new_tool
    print(f"Tool has been set to {tool}")
    for e in tool_entities:
        e.delete_self()
        field_one = None
    tool_entities.clear()
    if tool == "Entity":
        from data.objects import entity_factories
        from core.camera import camera
        image_names = [i.icon for i in entity_factories]
        sv = Entity(ScrollView(
            image_names,
            create_scroll_sprite_generic,
            set_entity,
            64+4,
            width=(64),
            height=camera.height
        ),
        x=camera.width-32-3-3)
        tool_entities.append(sv)
    if tool == "Tile":
        from core.area import area
        from core.camera import camera
        image_names = [i.image_name for i in area.map.tile_kinds]
        sv = Entity(ScrollView(
            image_names,
            create_scroll_sprite_generic,
            set_current_tile,
            36,
            width=(32),
            height=camera.height
        ),
        x=camera.width-32-3-3)
        tool_entities.append(sv)
        field_label = Entity(Label("EBGaramond-Regular.ttf", "Brush Size"),
                             y=camera.height-50).get(Label)
        field_one = Entity(
            TextInput("EBGaramond-Regular.ttf", "1", max_text=1),
            x=field_label.get_bounds().width + 5,
            y=camera.height-50
        ).get(TextInput)
        tool_entities.append(field_label.entity) # Need to add the entities to these in video
        tool_entities.append(field_one.entity)

# ---- Map Editor Functionality ----
# Saves the map file, overriding the previous one.
def save_map():
    print("Saving not implemented yet.")

def place_tile(mouse_x, mouse_y):
    # What tile is the mouse on?
    from core.camera import camera
    x = mouse_x + camera.x
    y = mouse_y + camera.y
    from core.area import area
    try:
        global field_one
        size = int(field_one.text)
        for yy in range(size):
            for xx in range(size):
                area.map.set_tile(x + (xx*32), y + (yy*32), current_tile_index)
    except Exception as e:
        print("Error placing tile", e)

def place_entity(mouse_x, mouse_y):
    from core.camera import camera
    from core.area import area
    from data.objects import entity_factories
    x = mouse_x + camera.x
    y = mouse_y + camera.y
    entity_x = int(x / area.map.tile_size) * 32
    entity_y = int(y / area.map.tile_size) * 32
    from components.editor.entity_placeholder import EntityPlaceholder, taken_positions
    pos = x * 10000000 + y
    if not pos in taken_positions:
        taken_positions.add(pos)
        e = Entity(Sprite(entity_factories[current_entity_index].icon), 
            EntityPlaceholder(current_entity_index), 
            x=entity_x, 
            y=entity_y)
        from core.area import area
        area.entities.append(e)
    # create_entity(current_entity_index, entity_x, entity_y)
    

def click_tool(mouse_x, mouse_y):
    # Look for current entity
    from core.area import area
    for e in area.entities:
        if e.has(Sprite):
            sprite = e.get(Sprite)
            # Figure out whether the mouse is in the sprite
            if mouse_x > e.x and \
                mouse_y > e.y and \
                mouse_x < e.x + sprite.image.get_width() and \
                mouse_y < e.y + sprite.image.get_height():
                from components.editor.entity_placeholder import EntityPlaceholder
                from data.objects import entity_factories
                global selected_entity
                selected_entity = e
                id = e.get(EntityPlaceholder).id
                print(f"Selected {entity_factories[id].name}")
                return # Once we find one, stop looking. Optimization

            
def delete_tool(mouse_x, mouse_y):
    # Look for current entity
    from core.area import area
    for e in area.entities:
        if e.has(Sprite):
            sprite = e.get(Sprite)
            # Figure out whether the mouse is in the sprite
            if mouse_x > e.x and \
                mouse_y > e.y and \
                mouse_x < e.x + sprite.image.get_width() and \
                mouse_y < e.y + sprite.image.get_height():
                pos = e.x * 10000000 + e.y
                from components.editor.entity_placeholder import taken_positions
                if pos in taken_positions:
                    taken_positions.remove(pos)
                e.delete_self()
                return # Once we find one, stop looking. Optimization


# ---- User Interface ----
def back_button_press():
    global tool_entities
    tool_entities.clear()

    from core.engine import engine
    engine.switch_to("EditorChooseFile")

def on_click():
    global tool
    print("On Click Called")
    mouse_pos = pygame.mouse.get_pos()
    from core.camera import camera
    if mouse_pos[0] > camera.width-(32+3+3) or \
        (mouse_pos[0] < 64 and mouse_pos[1] < 64*4) or \
        (mouse_pos[1] > camera.height - 50):
        return
    print(tool)
    if tool == "Click":
        click_tool(mouse_pos[0], mouse_pos[1])
    elif tool == "Tile":
        place_tile(mouse_pos[0], mouse_pos[1])
    elif tool == "Entity":
        place_entity(mouse_pos[0], mouse_pos[1])
    elif tool == "Delete":
        delete_tool(mouse_pos[0], mouse_pos[1])

    
# ---- Main Editor Stage ----
def edit_map():
    global tool_entities, tool
    tool = "Click"
    tool_entities = []
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
    Entity(Button(lambda: set_tool("Entity"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('entity.png', True),
           x=2,
           y=2+64*3)
    Entity(Button(lambda: set_tool("Delete"),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('trash.png', True),
           x=2,
           y=2+64*4)
    Entity(Button(lambda: back_button_press(),
                  pygame.Rect(0, 0, 60, 60)),
           Sprite('button_background.png', True),
           Sprite('cancel.png', True),
           x=2,
           y=2+64*5)

    
