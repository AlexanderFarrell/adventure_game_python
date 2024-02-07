from components.button import create_simple_label_button
from data.tile_types import tile_kinds
from core.area import Area
from components.entity import Entity
from components.editor_helper import EditorHelper

filename = None
is_new = False

def prepare_map_editor(filename_in, is_new_in):
    global filename, is_new
    filename = filename_in
    is_new = is_new_in

def back():
    from core.engine import engine
    engine.switch_to("EditorChooseFile")

def edit_map():
    print("Starting map editor")
    print(f"Filename: {filename} - Is New: {is_new}")

    if is_new:
        pass
    else:
        Area(filename, tile_kinds, editor_mode=True)

    Entity(EditorHelper())

    create_simple_label_button(
        back,
        "EBGaramond-ExtraBold.ttf",
        "Back",
        x=10,
        y=10
    )
