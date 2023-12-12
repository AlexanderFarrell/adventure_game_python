from components.ui.window import create_window
from math import ceil
from components.entity import Entity
from components.sprite import Sprite
from components.ui.window import Window

items_per_row = 5
padding_size = 5
gap_size = 5
item_size = 32

class InventoryView:
    def __init__(self, inventory, slot_image="inventory_slot.png"):
        from core.engine import engine
        self.inventory = inventory
        self.slot_image = slot_image

        width = padding_size + (items_per_row * item_size) + ((items_per_row-1 ) * gap_size) + padding_size
        rows = ceil(inventory.capacity / items_per_row)
        height = padding_size + (rows * item_size) + ((rows-1) * gap_size) + padding_size

        from core.camera import camera
        x = camera.width - width
        y = 0

        self.window = create_window(x, y, width, height)
        self.slot_container_sprites = []
        self.slot_sprites = []

        inventory.listener = self

        self.render()

    def render(self):
        print("Called render")
        row = 0
        column = 0
        for slot in self.inventory.slots:
            x = column * (item_size + gap_size) + self.window.x + padding_size
            y = row * (item_size + gap_size) + self.window.y + padding_size
            container_sprite = Entity(Sprite(self.slot_image, True), x=x, y=y)
            self.window.get(Window).items.append(container_sprite)
            if slot.type is not None:
                print(slot.type.name)
                item_sprite = Entity(Sprite(slot.type.icon_name, True), x=x, y=y)
                self.window.get(Window).items.append(item_sprite)
            column += 1
            if column >= items_per_row:
                column = 0
                row += 1


    def clear(self):
        for i in self.window.get(Window).items:
            i.get(Sprite).breakdown()
        self.window.get(Window).items.clear()


    def refresh(self):
        self.clear()
        self.render()

    def breakdown(self):
        pass

