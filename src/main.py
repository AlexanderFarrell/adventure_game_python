import pygame
from core.input import keys_down
from core.camera import create_screen
from components.entity import active_objs
from core.area import Area, area
from components.sprite import sprites
from data.tile_types import tile_kinds

# Set up 
pygame.init()

pygame.display.set_caption("Adventure Game")
screen = create_screen(1280, 720, "Adventure Game")

clear_color = (30, 150, 240)
running = True

area = Area("start.map", tile_kinds)


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
    for a in active_objs:
        a.update()

    # Draw Code
    screen.fill(clear_color)
    area.map.draw(screen)
    for s in sprites:
        s.draw(screen)
    pygame.display.flip()

    # Cap the frames
    pygame.time.delay(17)


# Break down Pygame
pygame.quit()