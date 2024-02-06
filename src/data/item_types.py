from components.inventory import ItemType

item_types = [
    ItemType("Diamond", "diamond.png", 5),
    ItemType("Axe", "axe.png", 1, chop_power=10),
    ItemType("Pickaxe", "pickaxe.png", 1, mine_power=10),
    ItemType("Sword", "sword.png", 1, 
             damage=10, cooldown=0.5, range=50, sound='sword1.mp3'),
    ItemType("Weak Sword", "sword.png", 1, 
             damage=2, cooldown=0.5, range=50, sound='sword1.mp3')
]
