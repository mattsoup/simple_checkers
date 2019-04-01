#!/usr/bin/env python3

import pygame
from pygame.locals import *
import checkers


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

def click_to_xy(x, y):
    my_x = x / square_size
    my_y = y / square_size

    return int(my_x), int(my_y)


red_list, black_list, board = checkers.game_setup(8)
running = True

def draw_piece(piece, color):
    my_x, my_y = xy_to_square_center(piece.x, piece.y)
    if piece.kinged is True:
        pygame.draw.circle(screen, color, (my_x, my_y), int(square_size / 3))
        pygame.draw.circle(screen, red, (my_x, my_y), int(square_size / 4), 2)
    else:
        pygame.draw.circle(screen, color, (my_x, my_y), int(square_size / 3))

def select_piece(x, y):
    pygame.draw.circle(screen, black, (x, y), int(square_size / 3), 2)

def draw_board(red_list, black_list):
    screen.fill(red)
    for x in range(0, board_size, square_size * 2):
        for y in range(0, board_size, square_size):
            if (y / square_size) % 2 == 0:
                pygame.draw.rect(screen, black, (x + square_size, y, square_size, square_size))
            else:
                pygame.draw.rect(screen, black, (x,y,square_size,square_size))
    pygame.display.update()

    for piece in red_list:
        draw_piece(piece, white)
    for piece in black_list:
        draw_piece(piece, black)
    pygame.display.update()


draw_board(red_list, black_list)

selected = False
valid = False
while running is True:
    if len(red_list) == 0:
        running = False
    elif len(black_list) == 0:
        running = False
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = click_to_xy(x, y)

            if checkers.identify_piece((x, y), red_list) != False:
                selected = True
                red_coords = checkers.make_tuples(red_list)
                black_coords = checkers.make_tuples(black_list)
                draw_board(red_list, black_list)

                piece = checkers.identify_piece((x, y), red_list)
                x, y = xy_to_square_center(piece.x, piece.y)
                select_piece(x, y)

            elif selected is True and (x, y) in piece.potential_moves():
                valid = checkers.one_player_check_if_valid_move((x, y), red_list, black_list, 8)
                if valid is True:
                    checkers.update_board(piece, (x, y), black_list, board)
                    piece.x = x
                    piece.y = y
                    red_coords = checkers.make_tuples(red_list)
                    black_coords = checkers.make_tuples(black_list)
                    draw_board(red_list, black_list)
                    selected = False

                    checkers.pick_move(black_list, red_list, board, board_size)
                    red_coords = checkers.make_tuples(red_list)
                    black_coords = checkers.make_tuples(black_list)
                    draw_board(red_list, black_list)
                    valid = False

            elif selected is True and (abs(x - piece.x), abs(y - piece.y)) == (2, 2):
                valid = checkers.one_player_check_if_valid_jump((x, y), (piece.x, piece.y), black_list, board)
                if valid is True:
                    checkers.update_board(piece, (x, y), black_list, board, True)
                    piece.x = x
                    piece.y = y
                    red_coords = checkers.make_tuples(red_list)
                    black_coords = checkers.make_tuples(black_list)
                    draw_board(red_list, black_list)
                    selected = False

                    checkers.pick_move(black_list, red_list, board, board_size)
                    red_coords = checkers.make_tuples(red_list)
                    black_coords = checkers.make_tuples(black_list)
                    draw_board(red_list, black_list)
                    valid = False



            pygame.display.update()


#
#     screen.blit(surf, (400, 400))
#     pygame.display.flip()
