#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def argparser():
        parser = argparse.ArgumentParser()
        parser.add_argument("--run_file", required = True, help = "File with score parameters and corresponding game winner")
        parser.add_argument("--prefix", required = False, help = "Prefix for the output file")
        parser.add_argument("--save_plot", required = False, help = "Whether to save the plots as a png", action="store_true")

        args = parser.parse_args()
        return args

args = argparser()

headers = ["Jump score", "Death score", "Avoid Death score", "Provide Defense score", \
           "Distance to King score", "Distance to King factor", "Aggression threshhold", \
           "Aggression factor", "Coward factor", "Result"]

runs = pd.read_csv(args.run_file, sep = "\t", names = headers)

runs.set_index("Result", inplace = True)

b_wins = runs.loc['B']
r_wins = runs.loc['R']
draws = runs.loc['Draw']

plt.bar(0, len(b_wins), color = "black", alpha = 0.75, edgecolor = "black")
plt.bar(1, len(r_wins), color = "red", alpha = 0.75, edgecolor = "red")
plt.bar(2, len(draws), color = "grey", alpha = 0.75, edgecolor = "grey")
plt.xticks([0,1,2], ["B wins", "R wins", "Draws"])
plt.xlabel("Result")
plt.ylabel("Number of wins")

plt.show()


fig, ax = plt.subplots(nrows = 3, ncols = 3)#, sharex = "col")
for x in range(0, len(headers) - 1):
    x_coord = int(x / 3)
    y_coord = (x % 3)

    parts = ax[x_coord, y_coord].violinplot(b_wins[headers[x]], positions = [1], points = 100, widths = 0.8, showextrema = False)
    for pc in parts['bodies']:
        pc.set_facecolor('black')
        pc.set_edgecolor('black')
        pc.set_alpha(0.75)
        pc.set_zorder(10)
        pc.set_linewidth(0.5)
    ax[x_coord, y_coord].vlines(1, np.percentile(b_wins[headers[x]], 10), np.percentile(b_wins[headers[x]], 90), zorder = 10, linewidth = 0.5)
    ax[x_coord, y_coord].hlines(np.percentile(b_wins[headers[x]], 50), 1 - 0.1, 1 + 0.1, zorder = 10, linewidth = 0.5)

    parts = ax[x_coord, y_coord].violinplot(r_wins[headers[x]], positions = [2], points = 100, widths = 0.8, showextrema = False)
    for pc in parts['bodies']:
        pc.set_facecolor('red')
        pc.set_edgecolor('red')
        pc.set_alpha(0.75)
        pc.set_zorder(10)
        pc.set_linewidth(0.5)
    ax[x_coord, y_coord].vlines(2, np.percentile(r_wins[headers[x]], 10), np.percentile(r_wins[headers[x]], 90), zorder = 10, linewidth = 0.5)
    ax[x_coord, y_coord].hlines(np.percentile(r_wins[headers[x]], 50), 2 - 0.1, 2 + 0.1, zorder = 10, linewidth = 0.5)

    parts = ax[x_coord, y_coord].violinplot(draws[headers[x]], positions = [3], points = 100, widths = 0.8, showextrema = False)
    for pc in parts['bodies']:
        pc.set_facecolor('grey')
        pc.set_edgecolor('grey')
        pc.set_alpha(0.75)
        pc.set_zorder(10)
        pc.set_linewidth(0.5)
    ax[x_coord, y_coord].vlines(3, np.percentile(draws[headers[x]], 10), np.percentile(draws[headers[x]], 90), zorder = 10, linewidth = 0.5)
    ax[x_coord, y_coord].hlines(np.percentile(draws[headers[x]], 50), 3 - 0.1, 3 + 0.1, zorder = 10, linewidth = 0.5)

    ax[x_coord, y_coord].set_ylabel(headers[x])

plt.setp(ax, xticks = [1,2,3], xticklabels = ["B wins", "R wins", "Draws"])
fig.tight_layout()
plt.show()
