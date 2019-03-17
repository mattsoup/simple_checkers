#!/usr/bin/env python3

import random
from itertools import chain

jump_score = 5
move_score = 1
death_score = -3
defense_score = 1
avoid_death_score = 2


board_size = 8

board = [["-"] * board_size for x in range(board_size + 1)]

class PieceAttributes():
    def __init__(self):
        self.color = ""
        self.x = None
        self.y = None
        self.kinged = False

# white_list = [(0,x) for x in range(0, board_size, 2)]
# white_list = list(chain.from_iterable(((0, x - 1), (1, x), (2, x - 1)) for x in range(-1, board_size, 2)))
white_list = []
for y in range(-1, board_size, 2):
    for x in range(0, 3):
        my_piece = PieceAttributes()
        my_piece.color = "W"
        my_piece.x = x
        if x == 1:
            my_piece.y = y
        else:
            my_piece.y = y - 1
        white_list.append(my_piece)

for piece in white_list[:]: # Slice cuz ya can't iterate over a list and change it too!
    if piece.y < 0 or piece.y > board_size:
        white_list.remove(piece)

# black_list = [(board_size - 1, x) for x in range(0, board_size, 2)]
# black_list = list(chain.from_iterable(((board_size - 1, x + 1), (board_size - 2, x), (board_size - 3, x + 1)) for x in range(0, board_size, 2)))
black_list = []
for y in range(0, board_size, 2):
    for x in range(1, 4):
        my_piece = PieceAttributes()
        my_piece.color = "B"
        my_piece.x = board_size - x
        if x == 2:
            my_piece.y = y
        else:
            my_piece.y = y + 1
        black_list.append(my_piece)
for piece in black_list[:]:
    if  piece.y < 0 or piece.y > board_size:
        black_list.remove(piece)

# white_list = [(0,0)]
# black_list = [(1,1), (3,3), (5,5)]
for piece in white_list:
    print((piece.x, piece.y), end = " ")
for piece in black_list:
    print((piece.x, piece.y), end = " ")
print("\n")

for piece in white_list:
        board[piece.x][piece.y] = "W"
for piece in black_list:
        board[piece.x][piece.y] = "B"


def print_board():
    for x in range(board_size):
        for y in range(board_size):
            print(board[y][x], end = "\t")
        print("\n")


def make_tuples(piece_list):
    coord_list = [(piece.x, piece.y) for piece in piece_list]
    return coord_list


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
    # print("Potential jump!", player, my_move, current_position, my_list, opponent_list)
    direction = (current_position.x - my_move[0], current_position.y - my_move[1])
    jump = (my_move[0] - direction[0], my_move[1] - direction[1])
    # print(jump)
    if jump[0] >= 0 and jump[0] < board_size and jump[1] >= 0 and jump[1] < board_size and board[jump[0]][jump[1]] == "-":
        if skip == False:
            board[my_move[0]][my_move[1]] = "-"
            to_remove = make_tuples(opponent_list).index((my_move[0], my_move[1]))
            del opponent_list[to_remove]
            extra_jump = (jump[0] - direction[0], jump[1] - direction[1])
        return True, jump, True
    else:
        return False, None, None


def check_future_death(opponent, opponent_piece, my_move, current_position):
    # print("Potential death!", player, my_move, current_position, my_list, opponent_list, move)
    if abs(opponent_piece.x - my_move[0]) == 1 and abs(opponent_piece.y - my_move[1]) == 1:
        direction = (opponent_piece.x - my_move[0], opponent_piece.y - my_move[1])
        jump = (my_move[0] - direction[0], my_move[1] - direction[1])
        # print("Jump:", jump)
        # print(list(potential_moves([opponent_piece], opponent))[0])
        # print("My move", my_move, list(potential_moves(opponent_piece)))
        if my_move not in list(potential_moves(opponent_piece))[0]:
            # print("Not in danger!")
            return False
        elif my_move[0] == 0 or my_move[0] == board_size - 1 or my_move[1] == 0 or my_move[1] == board_size - 1:
            # print("Moving to the edge of the board!")
            return False
        # if jump == move:
        #     return True
        # if jump == (current_position.x, current_position.y):
        if jump == (current_position.x, current_position.y):
            print("Would jump me :(")
            return True
        elif jump[0] >= 0 and jump[0] < board_size and jump[1] >= 0 and jump[1] < board_size and (board[jump[0]][jump[1]] == "-" or board[jump[0]][jump[1]] == opponent_piece.color):
            print("Would return my jump")
            return True
    else:
        return False


def check_if_valid_move(player, my_move, current_position, my_list, opponent_list, skip = False):
    if my_move[0] < 0 or my_move[0] >= board_size or my_move[1] < 0 or my_move[1] >= board_size:
        return False, None, None
    elif (my_move[0], my_move[1]) in make_tuples(my_list):
        return False, None, None
    elif (my_move[0], my_move[1]) in make_tuples(opponent_list):
        return check_if_opponent(player, my_move, current_position, my_list, opponent_list, skip)
    else:
        return True, my_move, None


def potential_moves(positions):
    if positions.kinged == True:
        # for piece in positions:
        #     yield [(piece.x + 1, piece.y + 1), (piece.x + 1, piece.y - 1), (piece.x - 1, piece.y + 1), (piece.x - 1, piece.y - 1)]
        yield [(positions.x + 1, positions.y + 1), (positions.x + 1, positions.y - 1), (positions.x - 1, positions.y + 1), (positions.x - 1, positions.y - 1)]
    elif positions.color == "W":
        # for piece in positions:
        #     yield [(piece.x + 1, piece.y - 1), (piece.x + 1, piece.y + 1)]
        yield [(positions.x + 1, positions.y - 1), (positions.x + 1, positions.y + 1)]
    else:
        # for piece in positions:
        #     yield [(piece.x - 1, piece.y - 1),(piece.x - 1, piece.y + 1)]
        yield [(positions.x - 1, positions.y - 1), (positions.x - 1, positions.y + 1)]

def pick_move(moves, my_list, player, board, opponent_list, skip = False):
    valid = False
    attempt = 0
    high_piece_score = -10000 # Arbitrarily small
    chosen_list = []
    chosen_move_list = []
    while valid == False:
        for piece in my_list:
            piece_score, piece_move = evaluate_surroundings(player, piece, my_list, piece, opponent_list)
            if len(piece_move) == 0:
                    continue
            if piece_score > high_piece_score:
                chosen_list = [my_list.index(piece)]
                chosen_move_list = [piece_move]
                # chosen_one = my_list.index(piece)
                high_piece_score = piece_score
            elif piece_score == high_piece_score:
                chosen_list.append(my_list.index(piece))
                chosen_move_list.append(piece_move)
        assert len(chosen_list) > 0, "No valid moves"
        # print("Chosen list:", chosen_list, chosen_move_list)
        # piece = random.randint(0, len(my_list) - 1) # Needs to not be random
        chosen_one = random.randint(0, len(chosen_list) - 1) # Randomly chooses piece from highest scoring pieces
        chosen_one = random.choice(chosen_list)
        current_position = my_list[chosen_one]
        # my_move = random.choice(moves[chosen_one]) # Needs to not be random
        my_move = random.choice(chosen_move_list[chosen_list.index(chosen_one)]) # Randomly chooses from highest scoring moves from highest scoring piece
        # print(chosen_one, my_list, current_position)
        # print(my_move)
        #print(piece, my_list[piece], my_move)
        valid, my_move, extra_jump = check_if_valid_move(player, my_move, current_position, my_list, opponent_list, skip)
        attempt += 1
        chosen_list = []
        chosen_move_list = []
        if attempt == 100:
            print("I tried {} moves but couldn't find any valid ones :(".format(attempt))
            break

    # while extra_jump == True:
    #     print("trying for another jump")
    #     _valid, my_move, extra_jump = check_if_valid_move(player, my_move, current_position, my_list, opponent_list)

    else:
        x = my_list[chosen_one].x
        y = my_list[chosen_one].y
        board[x][y] = "-"
        x = my_move[0]
        y = my_move[1]
        board[x][y] = player
        my_list[chosen_one].x = my_move[0]
        my_list[chosen_one].y = my_move[1]
        if my_list[chosen_one].color == "W" and my_list[chosen_one].x == board_size - 1:
            my_list[chosen_one].kinged = True
        elif my_list[chosen_one].color == "B" and my_list[chosen_one].x == 0:
            my_list[chosen_one].kinged = True
        # for row in board:
        #         print(row)
        print_board()

def evaluate_surroundings(player, piece, my_list, current_position, opponent_list):
    print("Evaluating surroundings")
    # print(player, current_position, opponent_list)
    if player == "W":
        opponent = "B"
    else:
        opponent = "W"
    my_potential_moves = list(potential_moves(piece))
    # print(my_potential_moves)

    high_move_score = -10000 # Arbitrarily small score
    piece_score = 0
    score_explanation = []
    chosen_moves = []
    for move in my_potential_moves[0]: # Gonna check if I have any valid moves
        # print("Move:", move)
        current_move_score = 0
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
                # print("My_position:", current_position, "My_move:", my_move)
                future_death = check_future_death(opponent, opponent_piece, my_move, current_position)
                # print(future_death)
                if future_death == True: # Valid move that could result in being jumped next opponent move
                    piece_score += death_score
                    current_move_score += death_score
                    score_explanation.append(("Expected death", death_score))
                future_death = check_future_death(opponent, opponent_piece, (current_position.x, current_position.y), current_position)
                if future_death == True: # Valid move and if I don't move I could get jumped next opponent move
                    piece_score += death_score
                    current_move_score += avoid_death_score
                    score_explanation.append(("Avoiding death", avoid_death_score))


            if current_move_score > high_move_score:
                chosen_moves = [move]
                high_move_score = current_move_score
            elif current_move_score == high_move_score:
                chosen_moves.append(move)

    # Check if teammates directly behind
    # Check how many teammates / opponents there are
    # Check if currently in danger of being jumped

    score_explanation = list(set(score_explanation))
    piece_score = 0
    for (explanation, score) in score_explanation:
        piece_score += score
    print(score_explanation, piece_score, chosen_moves)
    return piece_score, chosen_moves

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
print_board()

for x in range(0, 500):
    print("Move {}".format(x))
    if len(white_list) == 0 or len(black_list) == 0:
        print("Game over!")
        break
    if x % 2 == 0:
        print("W's move")
        moves = [list(potential_moves(piece)) for piece in white_list]
        # moves = list(potential_moves(white_list, "W"))
        pick_move(moves, white_list, "W", board, black_list)
    else:
        print("B's move")
        moves = [list(potential_moves(piece)) for piece in black_list]
        # moves = list(potential_moves(black_list, "B"))
        pick_move(moves, black_list, "B", board, white_list)
