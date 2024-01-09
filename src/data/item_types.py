from components.inventory import ItemType

item_types = [
    ItemType("Diamond", "diamond.png", 5),
    ItemType("Axe", "axe.png", 1, chop_power=10),
    ItemType("Pickaxe", "pickaxe.png", 1, mine_power=10)
]
