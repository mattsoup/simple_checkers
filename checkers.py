#!/usr/bin/env python3

import random
import math

jump_score = 5
move_score = 1
death_score = -3
avoid_death_score = 2
provide_defense_score = 2
distance_to_king_score = 1
distance_to_king_factor = 0.5
aggression_threshhold = 1.0
aggression_factor = 0.5
coward_factor = 1.0


board_size = 8

board = [["-"] * board_size for x in range(board_size + 1)]

class PieceAttributes():
    def __init__(self):
        self.color = ""
        self.x = None
        self.y = None
        self.kinged = False

    def potential_moves(self):
        if self.kinged == True:
            return [(self.x + 1, self.y + 1), (self.x + 1, self.y - 1), (self.x - 1, self.y + 1), (self.x - 1, self.y - 1)]
        elif self.color.upper() == "W":
            return [(self.x + 1, self.y - 1), (self.x + 1, self.y + 1)]
        else:
            return [(self.x - 1, self.y - 1), (self.x - 1, self.y + 1)]


# white_list = [(0,x) for x in range(0, board_size, 2)]
# white_list = list(chain.from_iterable(((0, x - 1), (1, x), (2, x - 1)) for x in range(-1, board_size, 2)))
white_list = []
for y in range(-1, board_size, 2):
    for x in range(0, 3):
        my_piece = PieceAttributes()
        my_piece.color = "w"
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
        my_piece.color = "b"
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
        board[piece.x][piece.y] = "w"
for piece in black_list:
        board[piece.x][piece.y] = "b"


def print_board():
    for x in range(board_size):
        for y in range(board_size):
            print(board[y][x], end = "\t")
        print("\n")


def make_piece(x, y, color):
    piece = PieceAttributes()
    piece.x = x
    piece.y = y
    piece.color = color
    return piece

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


def check_if_opponent(my_move, current_position, my_list, opponent_list, skip = False):
    # print("Potential jump!", player, my_move, current_position, my_list, opponent_list)
    direction = (current_position[0] - my_move[0], current_position[1] - my_move[1])
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


def check_future_death(opponent_piece, my_move, current_position):
    # print("Potential death!", player, my_move, current_position, my_list, opponent_list, move)
    if abs(opponent_piece.x - my_move[0]) == 1 and abs(opponent_piece.y - my_move[1]) == 1:
        direction = (opponent_piece.x - my_move[0], opponent_piece.y - my_move[1])
        jump = (my_move[0] - direction[0], my_move[1] - direction[1])
        # print("Jump:", jump)
        # print(list(potential_moves([opponent_piece], opponent))[0])
        # print("My move", my_move, list(potential_moves(opponent_piece)))
        if my_move not in opponent_piece.potential_moves():
            # print("Not in danger!")
            return False
        elif my_move[0] == 0 or my_move[0] == board_size - 1 or my_move[1] == 0 or my_move[1] == board_size - 1:
            # print("Moving to the edge of the board!")
            return False
        # if jump == move:
        #     return True
        # if jump == (current_position.x, current_position.y):
        if jump == current_position:
            print("Would jump me :(")
            return True
        elif jump[0] >= 0 and jump[0] < board_size and jump[1] >= 0 and jump[1] < board_size and (board[jump[0]][jump[1]] == "-" or board[jump[0]][jump[1]].upper() == opponent_piece.color.upper()):
            print("Would return my jump")
            return True
    else:
        return False


def check_if_valid_move(my_move, current_position, my_list, opponent_list, skip = False):
    if my_move[0] < 0 or my_move[0] >= board_size or my_move[1] < 0 or my_move[1] >= board_size:
        return False, None, None
    elif (my_move[0], my_move[1]) in make_tuples(my_list):
        return False, None, None
    elif (my_move[0], my_move[1]) in make_tuples(opponent_list):
        return check_if_opponent(my_move, current_position, my_list, opponent_list, skip)
    else:
        return True, my_move, None


# def potential_moves(positions):
#     if positions.kinged == True:
#         # for piece in positions:
#         #     yield [(piece.x + 1, piece.y + 1), (piece.x + 1, piece.y - 1), (piece.x - 1, piece.y + 1), (piece.x - 1, piece.y - 1)]
#         yield [(positions.x + 1, positions.y + 1), (positions.x + 1, positions.y - 1), (positions.x - 1, positions.y + 1), (positions.x - 1, positions.y - 1)]
#     elif positions.color.upper() == "W":
#         # for piece in positions:
#         #     yield [(piece.x + 1, piece.y - 1), (piece.x + 1, piece.y + 1)]
#         yield [(positions.x + 1, positions.y - 1), (positions.x + 1, positions.y + 1)]
#     else:
#         # for piece in positions:
#         #     yield [(piece.x - 1, piece.y - 1),(piece.x - 1, piece.y + 1)]
#         yield [(positions.x - 1, positions.y - 1), (positions.x - 1, positions.y + 1)]

def distance_to_king(piece):
    if piece.color.upper() == "W":
        distance = board_size - 1 - piece.x
    else:
        distance = piece.x
    return distance

def distance_to_opponent(piece, opponent):
    # distance = abs(piece.x - opponent.x) + abs(piece.y - opponent.y) # Pretty sure Manhattan distance won't work for this
    distance = max([abs(piece.x - opponent.x), abs(piece.y - opponent.y)]) # Chessboard distance
    return distance

def pick_move(my_list, opponent_list, board):
    valid = False
    attempt = 0
    best_move_score = -10000 # Arbitrarily small
    chosen_list = []
    chosen_move_list = []
    chosen_explanation_list = []
    # while valid == False:
    for piece in my_list:
        move_score, moves, explanations = evaluate_surroundings(piece, my_list, opponent_list)
        if len(moves) == 0:
                continue
        if move_score > best_move_score:
            chosen_list = [piece]
            chosen_move_list = [moves]
            chosen_explanation_list = [explanations]
            # chosen_one = my_list.index(piece)
            best_move_score = move_score
        elif move_score == best_move_score:
            chosen_list.append(piece)
            chosen_move_list.append(moves)
            chosen_explanation_list.append(explanations)

    assert len(chosen_list) > 0, "No valid moves"
    # print(chosen_list)
    # print(chosen_move_list)
    # print("Chosen list:", chosen_list, chosen_move_list)
    # piece = random.randint(0, len(my_list) - 1) # Needs to not be random
    chosen_index = random.randint(0, len(chosen_list) - 1) # Randomly chooses piece from highest scoring pieces
    # print(chosen_index, chosen_list[chosen_index])
    chosen_one = chosen_list[chosen_index]
    # chosen_one = random.choice(chosen_list[chosen_index])
    # print(chosen_one)
    current_position = (chosen_one.x, chosen_one.y)
    # my_move = random.choice(moves[chosen_one]) # Needs to not be random
    my_move_index = random.randint(0, len(chosen_move_list[chosen_index]) - 1) # Randomly chooses from highest scoring moves from highest scoring piece
    my_move = chosen_move_list[chosen_index][my_move_index] # Randomly chooses from highest scoring moves from highest scoring piece
    my_explanation = chosen_explanation_list[chosen_index][my_move_index]
    # print("My move:", my_move)
    # print(chosen_one, my_list, current_position)
    # print(my_move)
    #print(piece, my_list[piece], my_move)
    valid, my_move, extra_jump = check_if_valid_move(my_move, current_position, my_list, opponent_list)
    print("Moving {} to {} because:".format((chosen_one.x, chosen_one.y), (my_move)))
    for (reason, score) in my_explanation:
        print("{}: {}".format(reason, score))

    # while extra_jump == True:
    #     print("trying for another jump")
    #     _valid, my_move, extra_jump = check_if_valid_move(player, my_move, current_position, my_list, opponent_list)

    # else:
    x = chosen_one.x
    y = chosen_one.y
    board[x][y] = "-"
    x = my_move[0]
    y = my_move[1]
    chosen_one.x = my_move[0]
    chosen_one.y = my_move[1]
    if chosen_one.color.upper() == "W" and chosen_one.x == board_size - 1:
        chosen_one.kinged = True
        chosen_one.color = "W"
    elif chosen_one.color.upper() == "B" and chosen_one.x == 0:
        chosen_one.kinged = True
        chosen_one.color = "B"
    # for row in board:
    #         print(row)
    board[x][y] = chosen_one.color
    print_board()

def evaluate_surroundings(piece, my_list, opponent_list):
    # print("Evaluating surroundings")
    # print(player, current_position, opponent_list)
    my_potential_moves = piece.potential_moves()
    # print(my_potential_moves)

    best_move_score = -10000 # Arbitrarily small score
    # piece_score = 0
    best_moves = []
    best_explanation = []
    current_position = (piece.x, piece.y)
    for move in my_potential_moves: # Gonna check if I have any valid moves
        # print("Move:", move)
        current_move_score = 0
        score_explanation = []
        valid, my_move, _extra_jump = check_if_valid_move(move, current_position, my_list, opponent_list, True)
        if valid == True: # Valid move
            potential_piece = make_piece(my_move[0], my_move[1], piece.color)
            # piece_score += move_score
            current_move_score += move_score
            score_explanation.append(("Valid move", move_score))
            if my_move != move:
                # piece_score += jump_score # Valid move that is a jump
                current_move_score += jump_score
                score_explanation.append(("Valid jump", jump_score))

            nearest_opponent_distance = 10000 # Arbitrarily large
            nearest_opponents = []
            for opponent_piece in opponent_list:
                # print((opponent_piece.x, opponent_piece.y), distance_to_opponent(piece, opponent_piece))
                if distance_to_opponent(piece, opponent_piece) < nearest_opponent_distance:
                    nearest_opponents = [opponent_piece]
                    nearest_opponent_distance = distance_to_opponent(piece, opponent_piece)
                elif distance_to_opponent(piece, opponent_piece) == nearest_opponent_distance:
                    nearest_opponents.append(opponent_piece)

                future_death = check_future_death(opponent_piece, my_move, current_position)
                if future_death == True: # Valid move that could result in being jumped next opponent move
                    # piece_score += death_score
                    current_move_score += death_score
                    score_explanation.append(("Expected death", death_score))

                future_death = check_future_death(opponent_piece, current_position, current_position)
                if future_death == True: # Valid move and if I don't move I could get jumped next opponent move
                    # piece_score += death_score
                    current_move_score += avoid_death_score
                    score_explanation.append(("Avoiding death", avoid_death_score))

            best_distance_score = ("None", 0)
            # print("Move:", (potential_piece.x, potential_piece.y))
            for opponent in nearest_opponents:
                distance_change = distance_to_opponent(piece, opponent) - distance_to_opponent(potential_piece, opponent)
                # print("Nearest opponent:", (opponent.x, opponent.y))
                # print("Distance", distance_to_opponent(piece, opponent))
                # print("Distance change:", distance_change)
                if len(my_list) / len(opponent_list) >= aggression_threshhold:
                    total_distance_score = (distance_change * aggression_factor) * (len(my_list) / len(opponent_list))
                    if total_distance_score > best_distance_score[1]:
                        best_distance_score = ("Advancing towards the enemy", total_distance_score)
                    # piece_score += distance_change * aggression_factor
                    # current_move_score += distance_change * aggression_factor
                    # score_explanation.append(("Advancing towards the enemy", (distance_change * aggression_factor)))
                else:
                    total_distance_score = ((-distance_change) * aggression_factor) * (1 / (len(my_list) / len(opponent_list)))
                    if total_distance_score > best_distance_score[1]:
                        best_distance_score = ("Running away!", total_distance_score)
                    # piece_score += (-distance_change) * coward_factor
                    # current_move_score += (-distance_change) * coward_factor
                    # score_explanation.append(("Running away!", ((-distance_change) * coward_factor)))
            if best_distance_score != ("None", 0):
                # piece_score += best_distance_score[1]
                current_move_score += best_distance_score[1]
                score_explanation.append(best_distance_score)

            for teammate in my_list:
                if teammate != piece:
                    if (teammate.x, teammate.y) in potential_piece.potential_moves() and teammate.x != 0 and teammate.x != board_size - 1 and teammate.y != 0 and teammate.y != board_size - 1:
                        # piece_score += provide_defense_score
                        for opponent_piece in opponent_list:
                            future_death = check_future_death(opponent_piece, (teammate.x, teammate.y), (teammate.x, teammate.y))
                            if future_death == True: # Valid move and if I don't move I could get jumped next opponent move
                                # piece_score += death_score
                                current_move_score += avoid_death_score
                                score_explanation.append(("Providing defense", provide_defense_score))

                        # current_move_score += provide_defense_score
                        # score_explanation.append(("Potentially providing defense", provide_defense_score))

            if piece.kinged == False:
                distance = 1 - (distance_to_king(potential_piece) / board_size)
                # piece_score += distance_to_king_factor * (distance * distance_to_king_score)
                current_move_score += distance_to_king_factor * (distance * distance_to_king_score)
                score_explanation.append(("Moving closer to being kinged", distance_to_king_factor * (distance * distance_to_king_score)))

            current_move_score = 0
            # print(score_explanation)
            for (explanation, score) in score_explanation:
                current_move_score += score
            if current_move_score > best_move_score:
                best_moves = [move]
                best_move_score = current_move_score
                best_explanation = [score_explanation]
            elif current_move_score == best_move_score:
                best_moves.append(move)
                best_explanation.append(score_explanation)


    # score_explanation = list(set(score_explanation))
    # piece_score = 0
    # for (explanation, score) in score_explanation:
    #     piece_score += score
    # print(score_explanation, piece_score, chosen_moves)
    # print(best_move_score, best_moves, best_explanation)
    return best_move_score, best_moves, best_explanation

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
    print("Move {}".format(x + 1))
    if len(white_list) == 0 or len(black_list) == 0:
        print("Game over!")
        break
    if x % 2 == 0:
        print("W's move")
        # moves = [piece.(potential_moves() for piece in white_list]
        # moves = list(potential_moves(white_list, "W"))
        pick_move(white_list, black_list, board)
    else:
        print("B's move")
        # moves = [list(potential_moves(piece)) for piece in black_list]
        # moves = list(potential_moves(black_list, "B"))
        pick_move(black_list, white_list, board)
