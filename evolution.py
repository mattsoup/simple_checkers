#!/usr/bin/env python3

import numpy as np
import checkers

class CheckersRun():
    def __init__(self, move_scores_list):
        self.move_scores = np.array(move_scores_list.copy()) # Copy so it doesn't just reference the original list
        self.result_list = []

    def mutate(self):
        for x in range(len(self.move_scores)):
            if np.random.randint(0, 100) == 0:
                self.move_scores[x] = np.random.randint(-100, 100)
            elif np.random.randint(0, 5) == 0:
                self.move_scores[x] = np.random.normal(self.move_scores[x], 5)

        self.move_scores = np.round(self.move_scores)

    def calc_mean(self):
        return np.median(self.result_list)

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



def run_generations(run_list):
    """
    Run the combination of move scores XXX (10?) times
    """

    for run in run_list:
        for x in range(10):
            red_list, black_list, board = checkers.game_setup(8, run.move_scores)
            winner, turns, ratio = checkers.computers_only(red_list, black_list, board, 8)
            turns = 1 - (turns / 1000)
            result = (winner * turns * ratio)
            run.result_list.append(result)

    return

def calculate_scores(run_list):
    """
    Calculate the game scores for all the runs
    """
    result_list = np.array([run.calc_mean() for run in run_list])
    out.write("{}\t".format(np.mean(result_list)))

    result_list = result_list.argsort()[-int(len(run_list) * 0.1):]
    desired_scores = [run_list[x] for x in result_list]
    new_run_list = []
    for scores in desired_scores:
        for x in range(10):
            new_run_list.append(CheckersRun(scores.move_scores))

    return new_run_list



def run_script():
    run_list = [CheckersRun(np.zeros(9)) for x in range(50)]
    for x in range(500):
        print("Done with {} generations\r".format(x), end = "")
        run_generations(run_list)
        run_list = calculate_scores(run_list)

        for run in run_list:
            run.mutate()
        all_scores = np.empty((len(run_list), 9))
        for x in range(len(run_list)):
            for y in range(len(run_list[x].move_scores)):
                all_scores[x][y] = run_list[x].move_scores[y]

        out.write("\t".join(map(str, np.mean(all_scores, axis = 0))))
        out.write("\n")
        # for run in run_list:
        #     print(run.move_scores)
        # print("\n")




if __name__ == "__main__":
    out = open("500gens_random_v_zeros.txt", "w")
    run_script()













#placeholder
