import pygame
from components.sprite import Sprite, Animation
from core.input import is_key_pressed
from core.camera import camera
from components.entity import Entity
from components.label import Label
from components.physics import Body, triggers
from core.area import area
from components.inventory import Inventory
from components.ui.inventory_view import InventoryView
from core.math_ext import distance
from components.ui.bar import Bar

movement_speed = 2
inventory = Inventory(20)
message_time_seconds = 3

# Set a bunch of directions here to use later.
left = 0
up = 1
right = 2
down = 3
down_frames =  [(0,0), (1,0), (2, 0), (3, 0)]
up_frames =    [(0,1), (1,1), (2, 1), (3, 1)]
right_frames = [(0,2), (1,2), (2, 2), (3, 2)]
left_frames =  [(0,3), (1,3), (2, 3), (3, 3)]
down_still =   [(0,0)]
up_still =     [(0,1)]
right_still =  [(0,2)]
left_still =   [(0,3)]

def on_player_death(entity):
    from core.engine import engine
    engine.switch_to('Play')

class Player:
    def __init__(self, health):
        # Keep track of which direction we are facing.
        self.direction = down
        self.is_walking = False

        from core.engine import engine
        engine.active_objs.append(self)
        self.loc_label = Entity(Label("EBGaramond-Regular.ttf", 
                                         "X: 0 - Y: 0")).get(Label)
        self.message_label = Entity(Label("EBGaramond-Regular.ttf", 
                                       area.name)).get(Label)
        self.inventory_window = Entity(InventoryView(inventory))
        from core.camera import camera
        self.loc_label.entity.y = camera.height - 50

        self.loc_label.entity.x = 10
        self.message_label.entity.x = 10
        self.show_message(f"Entering {area.name}")

        self.health = health

    def setup(self):
        from components.combat import Combat
        combat = Combat(self.health, on_player_death)
        self.entity.add(combat)
        self.combat = combat
        del self.health

        self.health_bar = Entity(Bar(self.combat.max_health, 
                              (255, 0, 0), 
                              (0, 255, 0))).get(Bar); 
        
        self.health_bar.entity.x = camera.width - self.health_bar.width
        self.health_bar.entity.y = camera.height - self.health_bar.height
        
        print("Setup called")

    def breakdown(self):
        self.loc_label.entity.delete_self()
        self.message_label.entity.delete_self()
        self.inventory_window.delete_self()
        self.health_bar.entity.delete_self()
        from core.engine import engine
        engine.active_objs.remove(self)
        print("Called breakdown")

    def interact(self, mouse_pos):
        from core.engine import engine
        for usable in engine.usables:
            if usable.entity.has(Sprite):
                usable_sprite = usable.entity.get(Sprite)

                # Get the x, y, width and height of the usable's sprite
                x_sprite = usable.entity.x - camera.x
                y_sprite = usable.entity.y - camera.y
                width_sprite = usable_sprite.image.get_width()
                height_sprite = usable_sprite.image.get_height()

                # Check if the mouse is clicking this
                if x_sprite < mouse_pos[0] < x_sprite + width_sprite and \
                    y_sprite < mouse_pos[1] < y_sprite + height_sprite:

                    # Get our sprite
                    my_sprite = self.entity.get(Sprite)

                    # Calculate the distance between these two sprites, from their feet
                    d = distance(x_sprite + usable_sprite.image.get_width()/2, 
                                 y_sprite + usable_sprite.image.get_height(),
                                 self.entity.x - camera.x + my_sprite.image.get_width()/2,
                                 self.entity.y - camera.y + my_sprite.image.get_height())
                    
                    # Call the usable function
                    usable.on(self.entity, d)

                    # We only want to interact with the first thing we click. 
                    # Return prevents anymore objects being interacted with on this
                    # click
                    return
                
    def show_message(self, message):
        self.message_label.set_text(message)
        self.message_countdown = message_time_seconds * 60

    def walk_animation(self, direction, frame_coords):
        if self.direction != direction:
            self.direction = direction
            self.entity.get(Animation).set_frame_coords(frame_coords)
            self.is_walking = True

    def stop_animation(self):
        a = self.entity.get(Animation)
        self.is_walking = False
        if len(a.frame_coords) != 1:
            if self.direction == left:
                a.set_frame_coords(left_still)
            elif self.direction == right:
                a.set_frame_coords(right_still)
            elif self.direction == down:
                a.set_frame_coords(down_still)
            elif self.direction == up:
                a.set_frame_coords(up_still)
                
        
    def update(self):
        if self.message_countdown > 0:
            self.message_countdown -= 1
            if self.message_countdown <= 0:
                self.message_label.set_text("")
        self.loc_label.set_text(f"X: {int(self.entity.x/32)} - Y: {int(self.entity.y/32)}")
        previous_x = self.entity.x
        previous_y = self.entity.y
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)
        self.health_bar.amount = self.combat.health
        future_direction = None
        future_frames = None

        if is_key_pressed(pygame.K_w):
            self.entity.y -= movement_speed
            future_direction = up
            future_frames = up_frames
            
        if is_key_pressed(pygame.K_s):
            self.entity.y += movement_speed
            future_direction = down
            future_frames = down_frames

        if not body.is_position_valid():
            self.entity.y = previous_y

        if is_key_pressed(pygame.K_ESCAPE):
            from core.engine import engine
            engine.switch_to("Menu")

        from core.input import is_mouse_just_pressed
        mouse_pos = pygame.mouse.get_pos()

        if self.combat.equipped is None and inventory.equipped_slot is not None:
            print("Equipping")
            self.combat.equip(inventory.slots[inventory.equipped_slot].type)

        if self.combat.equipped is not None and inventory.equipped_slot is None:
            print("Unequipping", self.combat.equipped, inventory.equipped_slot)
            self.combat.unequip()

        if is_mouse_just_pressed(1):
            if self.combat.equipped is None or not 'range' in self.combat.equipped.stats:
                self.interact(mouse_pos)
            else:
                self.combat.perform_attack()
            
        if is_key_pressed(pygame.K_a):
            self.entity.x -= movement_speed
            future_direction = left
            future_frames = left_frames

        if is_key_pressed(pygame.K_d):
            self.entity.x += movement_speed
            future_direction = right
            future_frames = right_frames
        if not body.is_position_valid():
            self.entity.x = previous_x
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2
        if future_direction is not None:
            self.walk_animation(future_direction, future_frames)
        elif self.is_walking:
            self.stop_animation()

        for t in triggers:
            if body.is_colliding_with(t):
                t.on(self.entity)

