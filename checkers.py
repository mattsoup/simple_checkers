#!/usr/bin/env python3

import random


class MoveScores():
    def __init__(self, score_types):
        if type(score_types) is not str:
            self.jump_score = score_types[0] / 10
            self.death_score = score_types[1] / 10
            self.avoid_death_score = score_types[2] / 10
            self.provide_defense_score = score_types[3] / 10
            self.distance_to_king_score = score_types[4] / 10
            self.distance_to_king_factor = score_types[5] / 100
            self.aggression_threshhold = score_types[6] / 100
            self.aggression_factor = score_types[7] / 100
            self.coward_factor = score_types[8] / 100

        elif score_types.upper() == "ZEROS":
            self.jump_score = 0
            self.death_score = 0
            self.avoid_death_score = 0
            self.provide_defense_score = 0
            self.distance_to_king_score = 0
            self.distance_to_king_factor = 0
            self.aggression_threshhold = 0
            self.aggression_factor = 0
            self.coward_factor = 0

        elif score_types.upper() == "RANDOM":
            self.jump_score = random.randint(-100, 100) / 10
            self.death_score = random.randint(-100, 100) / 10
            self.avoid_death_score = random.randint(-100, 100) / 10
            self.provide_defense_score = random.randint(-100, 100) / 10
            self.distance_to_king_score = random.randint(-100, 100) / 10
            self.distance_to_king_factor = random.randint(-100, 100) / 100
            self.aggression_threshhold = random.randint(-100, 100) / 100
            self.aggression_factor = random.randint(-100, 100) / 100
            self.coward_factor = random.randint(-100, 100) / 100

        elif score_types.upper() == "PRE-DEFINED":
            self.jump_score = 5
            self.death_score = -3
            self.avoid_death_score = 2
            self.provide_defense_score = 2
            self.distance_to_king_score = 1
            self.distance_to_king_factor = 0.5
            self.aggression_threshhold = 1.0
            self.aggression_factor = 0.8
            self.coward_factor = 0.5

        elif score_types.upper() == "1000_GENS":
            self.jump_score = 9.9
            self.death_score = -8.7
            self.avoid_death_score = 8.2
            self.provide_defense_score = 3.6
            self.distance_to_king_score = -0.68
            self.distance_to_king_factor = 0.67
            self.aggression_threshhold = -0.91
            self.aggression_factor = -0.65
            self.coward_factor = 1.16

        elif score_types.upper() == "MYSTERY":
            self.jump_score = -4.892
            self.death_score = -.236
            self.avoid_death_score = -.236
            self.provide_defense_score = 6.588
            self.distance_to_king_score = -6.312
            self.distance_to_king_factor = .2366
            self.aggression_threshhold = .3538
            self.aggression_factor = -.159
            self.coward_factor = -.4284

class PieceAttributes():
    def __init__(self, my_move_scores = None):
        self.color = ""
        self.x = None
        self.y = None
        self.kinged = False
        self.move_scores = my_move_scores

    def potential_moves(self):
        """ Finds a piece's potential moves"""

        if self.kinged is True:
            return [(self.x + 1, self.y + 1), (self.x + 1, self.y - 1),\
                    (self.x - 1, self.y + 1), (self.x - 1, self.y - 1)]
        elif self.color.upper() == "R":
            return [(self.x + 1, self.y - 1), (self.x + 1, self.y + 1)]
        else:
            return [(self.x - 1, self.y - 1), (self.x - 1, self.y + 1)]

def game_setup(board_size, score_list = []):
    my_board = [["-"] * board_size for x in range(board_size + 1)]
    if len(score_list) != 0:
        R = MoveScores(score_list)
    else:
        R = MoveScores("mystery")
    my_red_list = []
    for y in range(-1, board_size, 2):
        for x in range(0, 3):
            my_piece = PieceAttributes(R)
            my_piece.color = "r"
            my_piece.x = x
            if x == 1:
                my_piece.y = y
            else:
                my_piece.y = y - 1
            my_red_list.append(my_piece)

    for piece in my_red_list[:]: # Slice cuz ya can't iterate over a list and change it too!
        if piece.y < 0 or piece.y > board_size:
            my_red_list.remove(piece)

    B = MoveScores("zeros")
    my_black_list = []
    for y in range(0, board_size, 2):
        for x in range(1, 4):
            my_piece = PieceAttributes(B)
            my_piece.color = "b"
            my_piece.x = board_size - x
            if x == 2:
                my_piece.y = y
            else:
                my_piece.y = y + 1
            my_black_list.append(my_piece)

    for piece in my_black_list[:]:
        if  piece.y < 0 or piece.y > board_size:
            my_black_list.remove(piece)

    for piece in my_red_list:
        my_board[piece.x][piece.y] = "r"
    for piece in my_black_list:
        my_board[piece.x][piece.y] = "b"

    return my_red_list, my_black_list, my_board

def print_board(my_board_size):
    """ Prints the board"""

    for x in range(my_board_size):
        for y in range(my_board_size):
            print(board[y][x], end = "\t")
        print("\n")


def make_piece(x, y, color):
    """ Given x,y coordinates and a team color, makes an instance of PieceAttributes"""

    piece = PieceAttributes()
    piece.x = x
    piece.y = y
    piece.color = color
    return piece

def make_tuples(piece_list):
    """ Makes a list of tuples with piece coordinates"""

    coord_list = [(piece.x, piece.y) for piece in piece_list]
    return coord_list


def update_board(piece, my_move, opponent_list, board, jump = False):
    """ Updates all the pieces on the board"""

    if jump is True:
        opponent_piece = identify_piece((int((my_move[0] + piece.x) / 2),\
                                         int((my_move[1] + piece.y) / 2)), opponent_list)
        opponent_list.remove(opponent_piece)
        board[int((my_move[0] + piece.x) / 2)][int((my_move[1] + piece.y) / 2)] = "-"
    board[piece.x][piece.y] = "-"
    piece.x = my_move[0]
    piece.y = my_move[1]
    if piece.x == len(board) - 1 - 1:
        piece.kinged = True
        piece.color = "R"
    board[piece.x][piece.y] = piece.color

def identify_piece(coords, piece_list):
    """ Given coordinates, determine which piece is being referenced"""

    for piece in piece_list:
        if (piece.x, piece.y) == coords:
            return piece
    return False

def one_player_check_if_valid_jump(my_move, current_position, opponent_list, board):
    if board[my_move[0]][my_move[1]] != "-":
        return False
    elif ((my_move[0] + current_position[0]) / 2, (my_move[1] + current_position[1]) / 2) in make_tuples(opponent_list):
        return True
    else:
        return False


def one_player_check_if_valid_move(my_move, my_list, opponent_list, board_size):
    if my_move[0] < 0 or my_move[0] >= board_size or my_move[1] < 0 or my_move[1] >= board_size:
        return False
    elif (my_move[0], my_move[1]) in my_list or (my_move[0], my_move[1]) in make_tuples(opponent_list):
        return False
    else:
        return True


def check_if_opponent(my_move, current_position, my_list, opponent_list, board, skip = False):
    direction = (current_position[0] - my_move[0], current_position[1] - my_move[1])
    jump = (my_move[0] - direction[0], my_move[1] - direction[1])
    if jump[0] >= 0 and jump[0] < len(board) - 1 and jump[1] >= 0 and jump[1] < len(board) - 1\
    and board[jump[0]][jump[1]] == "-":
        if skip is False:
            board[my_move[0]][my_move[1]] = "-"
            to_remove = make_tuples(opponent_list).index((my_move[0], my_move[1]))
            del opponent_list[to_remove]
            # extra_jump = (jump[0] - direction[0], jump[1] - direction[1])
        return True, jump, True
    else:
        return False, None, None


def check_future_death(opponent_piece, my_move, current_position, board, potential_jump = False):
    """Check if a move would potentially result in being jumped the next move"""

    direction = (opponent_piece.x - my_move[0], opponent_piece.y - my_move[1])
    jump = (my_move[0] - direction[0], my_move[1] - direction[1])

    if my_move[0] == 0 or my_move[0] == len(board) - 1 - 1 or my_move[1] == 0 or\
    my_move[1] == len(board) - 1 - 1:
        return False, None
    if jump == current_position:
        return True, jump
    if jump[0] >= 0 and jump[0] < len(board) - 1 and jump[1] >= 0 and jump[1] < len(board) - 1:
        if board[jump[0]][jump[1]] == "-":
            return True, jump
        elif potential_jump == True and board[jump[0]][jump[1]].upper() == opponent_piece.color.upper():
            return True, jump
    return False, None

def check_if_valid_move(my_move, current_position, my_list, opponent_list, board, skip = False):
    """ Checks if a given move is valid or not"""

    if my_move[0] < 0 or my_move[0] >= len(board) - 1 or my_move[1] < 0 or my_move[1] >= len(board) - 1:
        return False, None, None
    elif (my_move[0], my_move[1]) in make_tuples(my_list):
        return False, None, None
    elif (my_move[0], my_move[1]) in make_tuples(opponent_list):
        return check_if_opponent(my_move, current_position, my_list, opponent_list, board, skip)
    else:
        return True, my_move, None


def distance_to_king(piece, my_board_size):
    """Finds the distance a piece is from being kinged"""

    if piece.color.upper() == "R":
        distance = my_board_size - 1 - piece.x
    else:
        distance = piece.x
    return distance

def distance_to_opponent(piece, opponent):
    """ Finds the Chessboard distance between a piece and an opponent piece"""

    distance = max([abs(piece.x - opponent.x), abs(piece.y - opponent.y)]) # Chessboard distance
    return distance

def pick_move(my_list, opponent_list, board, board_size):
    best_move_score = -10000 # Arbitrarily small
    chosen_list = []
    chosen_move_list = []
    chosen_explanation_list = []
    for piece in my_list:
        move_score, moves, explanations = evaluate_surroundings(piece, my_list, opponent_list, board, board_size)

        if len(moves) == 0:
            continue
        if move_score > best_move_score:
            chosen_list = [piece]
            chosen_move_list = [moves]
            chosen_explanation_list = [explanations]
            best_move_score = move_score
        elif move_score == best_move_score:
            chosen_list.append(piece)
            chosen_move_list.append(moves)
            chosen_explanation_list.append(explanations)

    if len(chosen_list) == 0:
        return True

    chosen_index = random.randint(0, len(chosen_list) - 1) # Randomly chooses piece from highest scoring pieces
    chosen_one = chosen_list[chosen_index]
    current_position = (chosen_one.x, chosen_one.y)

    my_move_index = random.randint(0, len(chosen_move_list[chosen_index]) - 1) # Randomly chooses from highest scoring moves from highest scoring piece
    my_move = chosen_move_list[chosen_index][my_move_index] # Randomly chooses from highest scoring moves from highest scoring piece
    my_explanation = chosen_explanation_list[chosen_index][my_move_index]

    _, my_move, _extra_jump = check_if_valid_move(my_move, current_position, my_list, opponent_list, board)
    if verbose is True:
        print("Moving {} to {} because:".format((chosen_one.x, chosen_one.y), (my_move)))
        for (reason, score) in my_explanation:
            print("{}: {}".format(reason, score))

    x = chosen_one.x
    y = chosen_one.y
    board[x][y] = "-"
    x = my_move[0]
    y = my_move[1]
    chosen_one.x = my_move[0]
    chosen_one.y = my_move[1]
    if chosen_one.color.upper() == "R" and chosen_one.x == board_size - 1:
        chosen_one.kinged = True
        chosen_one.color = "R"
    elif chosen_one.color.upper() == "B" and chosen_one.x == 0:
        chosen_one.kinged = True
        chosen_one.color = "B"
    board[x][y] = chosen_one.color

    return False

def defend_teammate(my_list, piece, potential_piece, opponent_list, board_size, board):
    my_score = 0
    for teammate in my_list:
        if teammate != piece:
            if distance_to_opponent(teammate, potential_piece) == 1 and\
            teammate.x != 0 and teammate.x != board_size - 1 and teammate.y != 0\
            and teammate.y != board_size - 1:
                for opponent_piece in opponent_list:
                    if (teammate.x, teammate.y) in opponent_piece.potential_moves():
                        future_death, jump = check_future_death(opponent_piece,\
                                             (teammate.x, teammate.y), (teammate.x, teammate.y),\
                                             board)
                        if future_death is True and jump == (potential_piece.x, potential_piece.y): # Valid move and if I don't move I could get jumped next opponent move
                            my_score += piece.move_scores.provide_defense_score
                            break

    return my_score

def becoming_king(potential_piece, piece, board_size):
    distance = 1 - (distance_to_king(potential_piece, board_size) / board_size)
    becoming_king_score = piece.move_scores.distance_to_king_factor * (distance *\
                          piece.move_scores.distance_to_king_score)

    return becoming_king_score

def find_nearest_opponent(piece, opponent_list):
    nearest_opponent_distance = 10000 # Arbitrarily large
    nearest_opponents = []
    for opponent_piece in opponent_list:
        if distance_to_opponent(piece, opponent_piece) < nearest_opponent_distance:
            nearest_opponents = [opponent_piece]
            nearest_opponent_distance = distance_to_opponent(piece, opponent_piece)
        elif distance_to_opponent(piece, opponent_piece) == nearest_opponent_distance:
            nearest_opponents.append(opponent_piece)

    return nearest_opponents, nearest_opponent_distance

def calc_distance_score(nearest_opponents, piece, potential_piece, my_list, opponent_list, nearest_opponent_distance):
    best_distance_score = ("None", 0)
    for opponent in nearest_opponents:
        distance_change = distance_to_opponent(piece, opponent) - distance_to_opponent(potential_piece, opponent)
        if len(my_list) / len(opponent_list) >= piece.move_scores.aggression_threshhold:
            total_distance_score = (distance_change * piece.move_scores.aggression_factor) * (len(my_list) / len(opponent_list))
            if total_distance_score > best_distance_score[1]:
                best_distance_score = ("Advancing towards the enemy", total_distance_score)
        elif distance_change > 0:
            best_distance_score = ("None", 0)
            break
        else:
            total_distance_score = ((-distance_change) * piece.move_scores.coward_factor) * (1 / (len(my_list) / len(opponent_list)))
            if total_distance_score > best_distance_score[1]:
                best_distance_score = ("Running away!", total_distance_score)
    if len(my_list) / len(opponent_list) <= piece.move_scores.aggression_threshhold:
        for opponent_piece in opponent_list:
            if distance_to_opponent(potential_piece, opponent_piece) <= nearest_opponent_distance:
                best_distance_score = ("None", 0)

    return best_distance_score

def evaluate_surroundings(piece, my_list, opponent_list, board, board_size):
    my_potential_moves = piece.potential_moves()

    best_move_score = -10000 # Arbitrarily small score
    best_moves = []
    best_explanation = []
    current_position = (piece.x, piece.y)
    for move in my_potential_moves: # Gonna check if I have any valid moves
        potential_jump = False
        current_move_score = 0
        score_explanation = []
        valid, my_move, _extra_jump = check_if_valid_move(move, current_position,\
                                               my_list, opponent_list, board, True)
        if valid is True: # Valid move
            potential_piece = make_piece(my_move[0], my_move[1], piece.color)
            # current_move_score += piece.move_scores.valid_score
            # score_explanation.append(("Valid move", piece.move_scores.valid_score))
            if my_move != move:
                potential_jump = True
                current_move_score += piece.move_scores.jump_score
                score_explanation.append(("Valid jump", piece.move_scores.jump_score))

            nearest_opponents, nearest_opponent_distance = find_nearest_opponent(piece, opponent_list)

            for opponent_piece in opponent_list:
                if distance_to_opponent(potential_piece, opponent_piece) == 1 and\
                my_move in opponent_piece.potential_moves() and (opponent_piece.x, opponent_piece.y) != move:
                    future_death, _ = check_future_death(opponent_piece, (potential_piece.x, potential_piece.y)\
                                                         , current_position, board, potential_jump)
                    if future_death is True: # Valid move that could result in being jumped next opponent move
                        current_move_score += piece.move_scores.death_score
                        score_explanation.append(("Expected death", piece.move_scores.death_score))

                if current_position[0] != 0 and current_position[0] != len(board) - 1 - 1\
                and current_position[1] != 0 and current_position[1] != len(board) - 1 - 1\
                and distance_to_opponent(piece, opponent_piece) == 1 and current_position\
                in opponent_piece.potential_moves():
                    future_death, _ = check_future_death(opponent_piece, current_position,\
                                                         current_position, board)
                    if future_death is True: # Valid move and if I don't move I could get jumped next opponent move
                        current_move_score += piece.move_scores.avoid_death_score
                        score_explanation.append(("Avoiding death", piece.move_scores.avoid_death_score))

            best_distance_score = calc_distance_score(nearest_opponents, piece, potential_piece, my_list, opponent_list, nearest_opponent_distance)

            if best_distance_score != ("None", 0):
                current_move_score += best_distance_score[1]
                score_explanation.append(best_distance_score)

            defend_teammate_score = defend_teammate(my_list, piece, potential_piece,\
                                                    opponent_list, board_size, board)
            if defend_teammate_score != 0:
                current_move_score += defend_teammate_score
                score_explanation.append(("Providing defense", defend_teammate_score))

            if piece.kinged is False:
                becoming_king_score = becoming_king(potential_piece, piece, board_size)
                current_move_score += becoming_king_score
                score_explanation.append(("Moving closer to being kinged", becoming_king_score))

            current_move_score = 0
            for (_explanation, score) in score_explanation:
                current_move_score += score
            if current_move_score > best_move_score:
                best_moves = [move]
                best_move_score = current_move_score
                best_explanation = [score_explanation]
            elif current_move_score == best_move_score:
                best_moves.append(move)
                best_explanation.append(score_explanation)

    return best_move_score, best_moves, best_explanation

def ask_for_piece(piece_list):
    coords = input("Piece to move (in format: x,y): ")
    coords = (int(coords.split(",")[0]) - 1, int(coords.split(",")[1]) - 1)
    piece = identify_piece(coords, red_list)

    while piece is False:
        coords = input("Piece to move (in format: x,y): ")
        coords = (int(coords.split(",")[0]) - 1, int(coords.split(",")[1]) - 1)
        piece = identify_piece(coords, red_list)

    return piece

def ask_for_move(piece, opponent_list, turn):
    valid = False
    jump = False
    while valid is False:
        move = input("Where do you want to move it? ")
        if move.upper() == "REDO":
            one_player(turn)
        move = (int(move.split(",")[0]) - 1, int(move.split(",")[1]) - 1)

        if move not in piece.potential_moves() and (abs(move[0] - piece.x), abs(move[1] - piece.y)) == (2, 2):
            print("I've got my eye on you O_o")
            valid = one_player_check_if_valid_jump(move, (piece.x, piece.y), black_list)
            if valid is True:
                jump = True
        elif move in piece.potential_moves() and board[move[0]][move[1]] == "-":
            valid = True
        else:
            print("WHATCHU DOIN THERE")

    return move, jump


def one_player(turn, red_list, black_list):
    game_over = False
    while game_over == False:
        if len(red_list) == 0:
            return "B"

        possible_moves = 0
        for piece in red_list:
            possible_moves += len(piece.potential_moves)
        if possible_moves == 0:
            return "B"

        if len(black_list) == 0:
            return "R"

        if turn % 2 == 0:
            piece = ask_for_piece(red_list)
            move, jump = ask_for_move(piece, black_list, turn)

            update_board(piece, move, black_list, jump)
            print_board()

        else:
            print("B's move")
            pick_move(black_list, red_list, board, board_size)
            print_board()

        turn += 1

def computers_only(red_list, black_list, board, board_size):
    try:
        board_size
    except NameError:
        board_size = len(board) - 1

    for turn in range(0, 500):
        if verbose == True:
            print_board(board_size)

        if len(red_list) == 0:
            return -1, turn,  len(black_list)
        elif len(black_list) == 0:
            return 1, turn, len(red_list)

        if verbose == True:
            print("Move {}".format(turn + 1))

        if turn % 2 == 0:
            if verbose == True:
                print("R's move")
            stuck = pick_move(red_list, black_list, board, board_size)
        else:
            if verbose == True:
                print("B's move")
            stuck = pick_move(black_list, red_list, board, board_size)

        if stuck is True:
            if turn <= 30:
                return 0, turn, abs(len(red_list) - len(black_list))
            elif turn % 2 == 0:
                return -1, turn, abs(len(red_list) - len(black_list))
            else:
                return 1, turn, abs(len(red_list) - len(black_list))

        if turn == 499:
            return 1, 500, abs(len(red_list) - len(black_list))

def print_scores(piece):
    for attr, value in piece.move_scores.__dict__.items():
        if attr in ("jump_score", "death_score", "avoid_death_score", "provide_defense_score", "distance_to_king_score"):
            value = value
        print(value, "\t", end = "")

    return

verbose = False
# verbose = True
if __name__ == "__main__":
    board_size = 8
    red_list, black_list, board = game_setup(board_size)
    # print_scores(red_list[0])
    print_scores(red_list[0])
    # print_scores(black_list[0])
    # print_board()
    # winner = one_player(0)
    winner, turns, ratio = computers_only(red_list, black_list, board, board_size)
    turns = 1 - (turns / 500)
    print("{}\t{}\t{}".format(winner, turns, ratio))
