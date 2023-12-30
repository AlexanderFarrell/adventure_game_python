import pygame
from components.ui.window import create_window
from math import ceil
from components.entity import Entity
from components.sprite import Sprite
from components.ui.window import Window
from components.button import Button
from components.label import Label
from core.input import is_key_just_pressed

dialogue_box_width = 500  # The size, left and right, of the dialogue box in pixels
dialogue_box_height = 200 # The size, up and down, of the dialogue box in pixels
padding_bottom = 50       # Empty pixels separating the dialogue box and the bottom
                          # of the window

# Where the name of the speaker is, in the dialogue box
speaker_label_x = 50     
speaker_label_y = 25     

# Where what is being said is, in the dialogue box
content_label_x = 50      
content_label_y = 75

# Where what is being said is, in the dialogue box
helper_label_x = 50
helper_label_y = 150

# How many letters, per frame, are printed.
letter_speed = 1


active_dialogue_view = None

class DialogueView:
    def __init__(self, lines, npc, player, dialogue_box_sprite="text_box.png"):
        global active_dialogue_view
        active_dialogue_view = self
        self.lines = lines
        self.npc = npc
        self.player = player

        from core.camera import camera
        window_x = camera.width/2 - dialogue_box_width/2
        window_y = camera.height - padding_bottom - dialogue_box_height
        self.window = create_window(window_x, window_y, 
                                    dialogue_box_width, dialogue_box_height).get(Window)
        
        self.background = Entity(Sprite(dialogue_box_sprite, is_ui=True),
                                 x=window_x,
                                 y=window_y).get(Sprite)

        self.speaker_label = Entity(Label("EBGaramond-ExtraBold.ttf", "", size=25), 
                                  x=window_x + speaker_label_x, 
                                  y=window_y + speaker_label_y).get(Label)

        self.content_label = Entity(Label("EBGaramond-Regular.ttf", "", size=25), 
                                  x=window_x + content_label_x, 
                                  y=window_y + content_label_y).get(Label)

        self.helper_label = Entity(Label("EBGaramond-Medium.ttf", 
                                         "[Press Enter or Space]", 
                                         size=25), 
                                  x=window_x + helper_label_x, 
                                  y=window_y + helper_label_y).get(Label)
        
        self.window.items.append(self.background)
        self.window.items.append(self.speaker_label)
        self.window.items.append(self.content_label)
        self.window.items.append(self.helper_label)

        from core.engine import engine
        engine.active_objs.append(self)

        self.current_line = -1
        self.next_line()

    def next_line(self):
        self.current_line += 1
        if self.current_line >= len(self.lines):
            self.breakdown()
            return
        line = self.lines[self.current_line]
        if len(line) == 0:
            self.next_line()
            return
        if line[0] == '-':
            self.player_speak(line)
        elif line[0] == '!':
            self.command(line)
        elif line[0] == '$':
            self.narrate(line)
        else:
            self.npc_speak(line)


    def npc_speak(self, line):
        self.speaker_label.set_text(self.npc.obj_name)
        self.content_label.set_text(line)

    def player_speak(self, line):
        self.speaker_label.set_text("You")
        self.content_label.set_text(line[1:])

    def narrate(self, line):
        self.speaker_label.set_text("")
        self.content_label.set_text(line[1:])

    def command(self, line):
        words = line.split(" ")
        command = words[1]
        arguments = words[2:]
        if command == "give":
            from components.player import inventory
            from data.item_types import item_types
            t = item_types[int(arguments[0])]
            amount = int(arguments[1])
            excess = inventory.add(t, amount)
            amount_added = amount - excess
            if amount_added == 0:
                self.speaker_label.set_text("")
                self.content_label.set_text(f"Your inventory is full")
            else:
                self.speaker_label.set_text("")
                self.content_label.set_text(f"You receive {amount_added} {t.name}")
        elif command == "goto":
            self.current_line = int(arguments[0])-2
            print(self.current_line)
            self.next_line()
        elif command == "end":
            self.breakdown()
        elif command == "random":
            import random
            next_lines = [int(x) for x in arguments]
            result = random.choice(next_lines)
            self.current_line = result-2
            self.next_line()
        else:
            print(f"Unknown command {command}")

    def update(self):
        if is_key_just_pressed(pygame.K_SPACE) or is_key_just_pressed(pygame.K_RETURN):
            self.next_line()

        if is_key_just_pressed(pygame.K_w) or is_key_just_pressed(pygame.K_a) \
            or is_key_just_pressed(pygame.K_s) or is_key_just_pressed(pygame.K_d) \
                or is_key_just_pressed(pygame.K_ESCAPE):
            self.breakdown()

    def breakdown(self):
        from core.engine import engine
        from core.area import area
        engine.active_objs.remove(self)
        for c in self.window.items:
            c.breakdown()