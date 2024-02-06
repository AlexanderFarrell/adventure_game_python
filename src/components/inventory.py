import pygame
from components.physics import Trigger
from core.sound import Sound

image_path = "content/images"
pick_up_sound = Sound('pick_up.mp3')

class ItemType:
    def __init__(self, name, icon, stack_size=1, **kwargs):
        self.name = name
        self.icon_name = icon
        self.icon = pygame.image.load(image_path + "/" + icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size
        self.stats = dict()
        for key in kwargs:
            self.stats[key] = kwargs[key]

class ItemSlot:
    def __init__(self):
        self.type = None
        self.amount = 0

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.equipped_slot = None
        self.taken_slots = 0
        self.slots = []
        for _ in range(self.capacity):
            self.slots.append(ItemSlot())
        self.listener = None
        # print(str(self))

    def notify(self):
        if self.listener is not None:
            self.listener.refresh()


    def get_best(self, stat):
        best = {"power": 0, "item": None}
        for s in self.slots:
            if s.type is not None and stat in s.type.stats:
                p = int(s.type.stats[stat])
                if p > best["power"]:
                    best["power"] = p
                    best["item"] = s.type
        return best


    def add(self, item_type, amount=1):
        # First sweep for any open stacks
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amo = amount
                    if add_amo > item_type.stack_size - slot.amount:
                        add_amo = item_type.stack_size - slot.amount
                    slot.amount += add_amo
                    amount -= add_amo
                    if amount <= 0:
                        self.notify()
                        return 0
        # Next, place the item in the next slot
        for slot in self.slots:
            if slot.type == None:
                slot.type = item_type
                if item_type.stack_size < amount:
                    slot.amount = item_type.stack_size
                    self.notify()
                    return self.add(item_type, amount - item_type.stack_size)
                else:
                    slot.amount = amount
                    self.notify()
                    return 0

        return amount
        
            

    def remove(self, item_type, amount=1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    found += slot.amount
                    continue
                elif slot.amount == amount:
                    found += amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    return found
                else:
                    found += amount
                    slot.amount -= amount
                    slot.type = None
                    self.notify()
                    return found
        return found

    def has(self, item_type, amount=1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                found += slot.amount
                if found >= amount:
                    return True
        return False

    def get_index(self, item_type):
        for index, slot in enumerate(self.slots):
            if slot.type == item_type:
                return index
        return -1
    
    def __str__(self):
        s = ""
        for i in self.slots:
            if i.type is not None:
                s += str(i.type.name) + ": " + str(i.amount) + "\t"
            else:
                s += "Empty slot\t"
        return s
        

    def get_free_slots(self):
        return self.capacity - self.taken_slots
    
    def is_full(self):
        return self.taken_slots == self.capacity
    
    def get_weight(self):
        weight = 0
        for i in self.slots:
            weight += i.weight * i.amount
        return weight
    
    def get_value(self):
        value = 0
        for i in self.slots:
            value += i.value * i.amount
        return value


def pick_up(item, other):
    from components.player import Player, inventory
    if other.has(Player):
        # inventory = other.get(Inventory)
        extra = inventory.add(item.item_type, item.quantity)
        pick_up_sound.play()
        item.quantity -= item.quantity - extra
        if item.quantity <= 0:
            from core.area import area
            area.remove_entity(item.entity)
        # print(inventory)
            

class DroppedItem(Trigger):
    def __init__(self, item_type, quantity):
        self.item_type = item_type
        self.quantity = quantity
        super().__init__(lambda other: pick_up(self, other), 0, 0, 32, 32)