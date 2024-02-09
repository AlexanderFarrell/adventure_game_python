from components.ui.text_input import TextInput
from components.ui.scroll_view import ScrollView, create_scroll_label_generic, print_on_choose
from components.entity import Entity
from components.button import Button, create_simple_label_button
from components.label import Label
from components.sprite import Sprite

page_width = 500
new_map_input = None

def create_map():


    # Check if user wrote .map
    if len(new_map_input.text) < 4 or new_map_input.text[-4:] != ".map":
        new_map_input.max_text += 5
        new_map_input.set_text(new_map_input.text + ".map")
    print(f"Creating map {new_map_input.text}")

def load_map(name):
    print(f"Loading map {name}")

def back():
    from core.engine import engine
    engine.switch_to("Menu")

def get_maps():
    import os
    files = os.listdir("content/maps")
    files.sort()
    return files

def editor_choose_file():
    Entity(Sprite("background2.png", is_ui=True))
    global new_map_input
    maps = get_maps()

    from core.camera import camera
    page_x = camera.width/2 - page_width/2
    
    create_simple_label_button(
        back,
        "EBGaramond-ExtraBold.ttf",
        "Back",
        x=10,
        y=10
    )

    Entity(Label("EBGaramond-ExtraBold.ttf", "Create New Map"),
           x=page_x, y=20)
    new_map_input = Entity(TextInput("EBGaramond-ExtraBold.ttf", "Test", width=400),
           x=page_x,
           y=100).get(TextInput)

    create_button = Entity(Button(create_map), Label("EBGaramond-ExtraBold.ttf", "Add"),
           x=page_x+420,
           y=100)
    create_button.get(Button).click_area = new_map_input.get_bounds()
    

    Entity(Label("EBGaramond-ExtraBold.ttf", "Load Map"),
           x=page_x,
           y=150)
    Entity(ScrollView(maps, 
                      create_scroll_label_generic, 
                      load_map, 32,
                      width=500,
                      height=500), x=page_x, y=200)
    # Entity(Button())