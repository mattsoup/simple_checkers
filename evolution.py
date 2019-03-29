#!/usr/bin/env python3

import numpy as np
import checkers

def pick_move_scores(scores_list):
    """
    Pick move scores to run checkers with
    [jump_score, death_score, avoid_death_score, provide_defense_score, distance_to_king_score\
     distance_to_king_factor, aggression_threshhold, aggression_factor, coward_factor]
    """
    for x in range(len(scores_list)):
        if np.random.randint(0,2) == 0:
            scores_list[x] = np.random.randint(scores_list[x], 5)

    return scores_list



def run_generations():
    """
    Run the combination of move scores XXX (10?) times
    """
    red_list, black_list, board = checkers.game_setup(8)
    for x in range(10):
        winner, turns, ratio = checkers.computers_only(red_list, black_list, board)

    return

def calculate_scores():
    """
    Calculate the game scores for all the runs
    """
    return




run_generations()

















if __name__ == "__main__":
    pass













#placeholder
