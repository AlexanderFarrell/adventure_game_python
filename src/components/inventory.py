import pygame

class ItemType:
    def __init__(self, name, icon, stack_size=1):
        self.name = name
        self.icon = pygame.image.load(icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size

class ItemSlot:
    def __init__(self):
        self.type = None
        self.amo = 0

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.taken_slots = 0
        self.slots = []
        for _ in range(self.slot_count):
            self.slots.append(ItemSlot())
        

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
                        return 0
        # Next, place the item in the next slot
        for slot in self.slots:
            if slot.type == None:
                slot.type = item_type
                if item_type.stack_size < amount:
                    slot.amount = item_type.stack_size
                    return self.add(item_type, amount - item_type.stack_size)
                else:
                    slot.amount = amount
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
                    return found
                else:
                    found += amount
                    slot.amount -= amount
                    slot.type = None
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

    def get_free_slots(self):
        return self.capacity - self.taken_slots
    
    def is_full(self):
        return self.taken_slots == 0
    
    def get_weight(self):
        weight = 0
        for i in self.slots:
            weight += i.weight
        return weight
    
    def get_value(self):
        value = 0
        for i in self.slots:
            value += i.value
        return value


