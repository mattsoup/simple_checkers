#!/usr/bin/env python3

import random

jump_score = 1
move_score = 1
death_score = -1
defense_score = 1


board_size = 9

board = [["-"] * board_size for x in range(board_size)]

white_list = [(0,x) for x in range(0, board_size, 2)]
black_list = [(board_size - 1, x) for x in range(0, board_size, 2)]

white_list = [(0,0)]
black_list = [(1,1), (3,3), (5,5)]
print(white_list, black_list)

for (x,y) in white_list:
        board[x][y] = "W"
for (x,y) in black_list:
        board[x][y] = "B"

for row in board:
        print(row)

def update_board(player, current_position, my_move, my_list, opponent_list):
    board[current_position[0]][current_position[1]] = "-"
    board[my_move[0]][my_move[1]] = player
    my_list.remove(current_position)
    my_list.append(my_move)
    if ((my_move[0] + current_position[0]) / 2, (my_move[1] + current_position[1]) / 2) in opponent_list:
        opponent_list.remove(((my_move[0] + current_position[0]) / 2, (my_move[1] + current_position[1]) / 2))
        board[int((my_move[0] + current_position[0]) / 2)][int((my_move[1] + current_position[1]) / 2)] = "-"

def one_player_check_if_valid_jump(my_move, current_position, my_list, opponent_list):
    if board[my_move[0]][my_move[1]] != "-":
        return False
    elif ((my_move[0] + current_position[0]) / 2, (my_move[1] + current_position[1]) / 2) in opponent_list:
        return True
    else:
        return False

def one_player_check_if_valid_move(player, my_move, current_position, my_list, opponent_list):
    if my_move[0] < 0 or my_move[0] >= board_size or my_move[1] < 0 or my_move[1] >= board_size:
        return False
    elif (my_move[0], my_move[1]) in my_list or (my_move[0], my_move[1]) in opponent_list:
        return False
    else:
        return True

def check_if_opponent(player, my_move, current_position, my_list, opponent_list, skip = False):
    print("Potential jump!", player, my_move, current_position, my_list, opponent_list)
    direction = (current_position[0] - my_move[0], current_position[1] - my_move[1])
    jump = (my_move[0] - direction[0], my_move[1] - direction[1])
    print(jump)
    if jump[0] >= 0 and jump[0] < board_size and jump[1] >= 0 and jump[1] < board_size and board[jump[0]][jump[1]] == "-":
        if skip == False:
            print("Jump!")
            board[my_move[0]][my_move[1]] = "-"
            opponent_list.remove((my_move[0], my_move[1]))
            extra_jump = (jump[0] - direction[0], jump[1] - direction[1])
            print(jump)
        return True, jump, True
    else:
        return False, None, None

def check_future_death(player, my_move, current_position, my_list, opponent_list, move):
    direction = (current_position[0] - my_move[0], current_position[1] - my_move[1])
    jump = (my_move[0] - direction[0], my_move[1] - direction[1])
    if jump == move: # removed: jump[0] >= 0 and jump[0] < board_size and jump[1] >= 0 and jump[1] < board_size and
        return True, jump, True
    else:
        return False, None, None

def check_if_valid_move(player, my_move, current_position, my_list, opponent_list, skip = False):
    if my_move[0] < 0 or my_move[0] >= board_size or my_move[1] < 0 or my_move[1] >= board_size:
        return False, None, None
    elif (my_move[0], my_move[1]) in my_list:
        return False, None, None
    elif (my_move[0], my_move[1]) in opponent_list:
        return check_if_opponent(player, my_move, current_position, my_list, opponent_list, skip)
    else:
        return True, my_move, None

def potential_moves(positions, player):
    if player == "W":
        for (x, y) in positions:
            yield [(x + 1, y - 1), (x + 1, y + 1)]
    else:
        for (x, y) in positions:
            yield [(x - 1, y - 1),(x - 1, y + 1)]

def pick_move(moves, my_list, player, board, opponent_list, skip = False):
    valid = False
    attempt = 0
    high_piece_score = -10000 # Arbitrarily small
    while valid == False:
        for piece in my_list:
            piece_score, piece_move = evaluate_surroundings(player, my_list, piece, opponent_list)
            if piece_score > high_piece_score:
                    chosen_one = my_list.index(piece)
                    high_piece_score = piece_score
        # piece = random.randint(0, len(my_list) - 1) # Needs to not be random
        piece = chosen_one # Not random anymore
        current_position = my_list[piece]
        my_move = random.choice(moves[piece]) # Needs to not be random
        #print(piece, my_list[piece], my_move)
        valid, my_move, extra_jump = check_if_valid_move(player, my_move, current_position, my_list, opponent_list, skip)
        attempt += 1
        if attempt == 1000:
            print("I tried {} moves but couldn't find any valid ones :(".format(attempt))
            break

    # while extra_jump == True:
    #     print("trying for another jump")
    #     _valid, my_move, extra_jump = check_if_valid_move(player, my_move, current_position, my_list, opponent_list)

    else:
        x = my_list[piece][0]
        y = my_list[piece][1]
        board[x][y] = "-"
        x = my_move[0]
        y = my_move[1]
        board[x][y] = player
        my_list[piece] = my_move
        for row in board:
                print(row)

def evaluate_surroundings(player, my_list, current_position, opponent_list):
    print("Evaluating surroundings")
    print(player, my_list, current_position, opponent_list)
    if player == "W":
        opponent = "B"
    else:
        opponent = "W"
    my_potential_moves = list(potential_moves([current_position], player))
    print(my_potential_moves)

    high_move_score = -10000 # Arbitrarily small score
    current_move_score = 0
    piece_score = 0
    score_explanation = []
    for move in my_potential_moves[0]:
        print(move)
        valid, my_move, _extra_jump = check_if_valid_move(player, move, current_position, my_list, opponent_list, True)
        if valid == True: # Valid move
            piece_score += move_score
            current_move_score += move_score
            score_explanation.append(("Valid move", move_score))
            if my_move != move:
                piece_score += jump_score # Valid move that is a jump
                current_move_score += jump_score
                score_explanation.append(("Valid jump", jump_score))
            for opponent_piece in opponent_list:
                future_death, _, _ = check_future_death(opponent, my_move, opponent_piece, opponent_list, list(my_move), move)
                print(future_death)
                if future_death == True: # Valid move that could result in being jumped next opponent move
                    piece_score += death_score
                    current_move_score += death_score
                    score_explanation.append(("Expected death", death_score))
        if current_move_score > high_move_score:
            chosen_move = move
            high_move_score = current_move_score
    # Check if teammates directly behind
    # Check how many teammates / opponents there are
    print(score_explanation)
    return piece_score, chosen_move

def one_player():
    game_over = False
    turn = 0
    while game_over == False:
        print("W: {}".format(white_list))
        print("B: {}".format(black_list))
        valid = False
        if turn % 2 == 0:
            for position in white_list:
                print(position)
            piece = input("Piece to move (in format: x,y): ")
            piece = (int(piece.split(",")[0]), int(piece.split(",")[1]))

            while piece not in white_list:
                piece = input("Piece to move (in format: x,y): ")
                piece = (int(piece.split(",")[0]), int(piece.split(",")[1]))

            while valid == False:
                move = input("Where do you want to move it? ")
                move = (int(move.split(",")[0]), int(move.split(",")[1]))

                if move[0] < 0 or move[0] >= board_size or move[1] < 0 or move[1] >= board_size:
                    print("That's not on the board!")
                elif ((move[0] - piece[0]), abs(move[1] - piece[1])) == (1,1): # Can only move down the board
                    print("Checking if valid move")
                    valid = one_player_check_if_valid_move("W", move, piece, white_list, black_list)
                elif (abs(move[0] - piece[0]), abs(move[1] - piece[1])) == (2,2):
                    print("Checking if valid jump")
                    valid = one_player_check_if_valid_jump(move, piece, white_list, black_list)
                else:
                    print("WHATCHU DOIN THERE")

            update_board("W", piece, move, white_list, black_list)

        else:
            print("B's move")
            moves = list(potential_moves(black_list, "B"))
            pick_move(moves, black_list, "B", board, white_list)

        turn += 1
        if len(white_list) == 0 or len(black_list) == 0:
            print("Game over!")
            break

#one_player()

for x in range(0, 5):
    print("Move {}".format(x))
    if len(white_list) == 0 or len(black_list) == 0:
        print("Game over!")
        break
    if x % 2 == 0:
        print("W's move")
        moves = list(potential_moves(white_list, "W"))
        pick_move(moves, white_list, "W", board, black_list)
    else:
        print("B's move")
        moves = list(potential_moves(black_list, "B"))
        pick_move(moves, black_list, "B", board, white_list)
