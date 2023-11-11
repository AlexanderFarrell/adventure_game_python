import pygame
from sprite import sprites, Sprite
from player import Player
from input import keys_down
from map import Map, TileKind


# Set up 
pygame.init()

pygame.display.set_caption("Adventure Game")
screen = pygame.display.set_mode((800, 600))

clear_color = (30, 150, 50)
running = True

tile_kinds = [
    TileKind("dirt", "images/dirt.png", False),
    TileKind("grass", "images/grass.png", False),
    TileKind("water", "images/water.png", False),
    TileKind("wood", "images/wood.png", False)
]
player = Player("images/player.png", 32*11, 32*7)
map = Map("maps/start.map", tile_kinds, 32)

Sprite("images/tree.png", 0 * 32, 0*32)
Sprite("images/tree.png", 5 * 32, 1*32)
Sprite("images/tree.png", 10*32, 4*32)
Sprite("images/tree.png", 7*32, 2*32)
Sprite("images/tree.png", 1*32, 10*32)
Sprite("images/tree.png", 12*32, -1*32)
Sprite("images/tree.png", 13*32, 12*32)
Sprite("images/tree.png", 2*32, 8*32)


# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            keys_down.remove(event.key)

    # Update Code
    player.update()

    # Draw Code
    screen.fill(clear_color)
    map.draw(screen)
    for s in sprites:
        s.draw(screen)
    pygame.display.flip()

    # Cap the frames
    pygame.time.delay(17)


# Break down Pygame
pygame.quit()