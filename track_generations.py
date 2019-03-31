#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

headers = ["Result", "Jump score", "Death score", "Avoid Death score", "Provide Defense score", \
           "Distance to King score", "Distance to King factor", "Aggression threshhold", \
           "Aggression factor", "Coward factor"]

runs = pd.read_csv("500gens_random_v_zeros.txt", sep = "\t", names = headers)

results = runs.iloc[:,0]

for x in range(len(runs) - 1):
    plt.plot(runs.iloc[:,x])
    plt.show()

plt.plot(results)
plt.show()
