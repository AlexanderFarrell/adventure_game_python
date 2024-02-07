from core.area import Area
from data.tile_types import tile_kinds
from components.entity import Entity
from components.button import Button
from components.label import Label
from components.sprite import Sprite

def editor_press():
    from core.engine import engine
    engine.switch_to("EditorChooseFile")

def new_game():
    from core.engine import engine
    engine.switch_to("Play")

def quit_game():
    from core.engine import engine
    engine.running = False

def menu():
    Entity(Sprite("main_menu.png", is_ui=True))

    new_game_button = Entity(Label("EBGaramond-Regular.ttf", 
                                         "New Game", 80,
                                         (255, 255, 0)))
    editor_button = Entity(Label("EBGaramond-Regular.ttf", 
                                         "Editor", 80,
                                         (255, 255, 0)))
    quit_game_button = Entity(Label("EBGaramond-Regular.ttf", 
                                         "Quit Game", 80,
                                         (255, 255, 0)))
    
    new_button_size = new_game_button.get(Label).get_bounds()
    editor_button_size = editor_button.get(Label).get_bounds()
    quit_button_size = quit_game_button.get(Label).get_bounds()
    
    new_game_button.add(Button(new_game, new_button_size))
    editor_button.add(Button(editor_press, editor_button_size))
    quit_game_button.add(Button(quit_game, quit_button_size))

    from core.camera import camera
    new_game_button.x = camera.width/2 - new_button_size.width/2
    new_game_button.y = camera.height - 500
    editor_button.x = camera.width/2 - new_button_size.width/2
    editor_button.y = camera.height - 350
    quit_game_button.x = camera.width/2 - quit_button_size.width/2
    quit_game_button.y = camera.height - 200