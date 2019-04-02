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


def run_generations(run_list):
    """
    Run the combination of move scores XXX (10?) times
    """

    for run in run_list:
        for x in range(10):
            red_list, black_list, board = checkers.game_setup(8, run.move_scores)
            winner, turns, ratio = checkers.computers_only(red_list, black_list, board, 8)
            turns = 1 - (turns / 500)
            if winner == 0 and turns == 0:
                result = ratio * 0.1
            else:
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



def run_script(run_list = []):
    if run_list == []:
        run_list = [CheckersRun(np.zeros(9)) for x in range(50)]
    else:
        run_list = [CheckersRun(run_list) for x in range(50)]

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
    out = open("500gens_random_v_1000gens.txt", "a+")
    out.seek(0)
    if len(out.readlines()) > 0:
        out.seek(0)
        last_run = list(map(float, out.readlines()[-1].strip().split("\t")))[1:]
        run_script(last_run)
    run_script()













#placeholder
