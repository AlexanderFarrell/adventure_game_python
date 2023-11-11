import pygame
from sprite import sprites, Sprite
from player import Player
from input import keys_down


# Set up 
pygame.init()

pygame.display.set_caption("Adventure Game")
screen = pygame.display.set_mode((800, 600))

clear_color = (30, 150, 50)
running = True

player = Player("images/player.png", 100, 100)


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
    for s in sprites:
        s.draw(screen)
    pygame.display.flip()

    # Cap the frames
    pygame.time.delay(17)


# Break down Pygame
pygame.quit()