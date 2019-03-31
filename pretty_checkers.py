#!/usr/bin/env python3

import pygame
from pygame.locals import *


board_size = 800
square_size = int(board_size / 8)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

white,black,red = (255,255,255), (0,0,0), (255,0,0)

pygame.init()
screen = pygame.display.set_mode((board_size, board_size))
screen.fill(red)


def xy_to_square_center(x, y):
    my_x = (x * square_size) + (square_size / 2)
    my_y = (y * square_size) + (square_size / 2)

    return int(my_x), int(my_y)

for x in range(0, board_size, square_size * 2):
    for y in range(0, board_size, square_size):
        if (y / square_size) % 2 == 0:
            pygame.draw.rect(screen, black, (x + square_size, y, square_size, square_size))
        else:
            pygame.draw.rect(screen, black, (x,y,square_size,square_size))

x, y = xy_to_square_center(3, 4)
pygame.draw.circle(screen, red, (x, y), int(square_size / 3), 2)

pygame.display.update()
running = True

while running is True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

#
#     screen.blit(surf, (400, 400))
#     pygame.display.flip()
