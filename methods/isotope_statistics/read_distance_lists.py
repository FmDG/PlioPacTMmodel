import matplotlib.pyplot as plt
import json
from os import chdir
import numpy as np


# Read the d18O/distance data from write_distance_lists.py
chdir("../..")
with open("data/permanent_lists/pacific_core_distances.json", 'r') as f:
    pacific_d18O_by_distance = json.load(f)

with open("data/permanent_lists/southern_core_distances.json", 'r') as f:
    southern_d18O_by_distance = json.load(f)

with open("data/permanent_lists/atlantic_core_distances.json", 'r') as f:
    atlantic_d18O_by_distance = json.load(f)

# This is the distance between 1209 and 1208, and the d18O difference observed.
print("{}km between 1209 and 1208, means a difference of 0.5 per mil is about {:.4f} per km".format(387.5, (0.5/387.5)))

# Plot how unusual this result is.
_, axs = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(8, 8)
)

axs[0, 0].hist(
    pacific_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=1000
    )
)

axs[0, 0].set(title=r'$\delta^{18}$O/distance (Pacific)')
axs[0, 0].axvline((0.5/387.5), color='r')

axs[1, 0].hist(
    southern_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=1000
    )
)

axs[1, 0].set(title=r'$\delta^{18}$O/distance (Southern)')
axs[1, 0].axvline((0.5/387.5), color='r')

axs[0, 1].hist(
    atlantic_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=1000
    )
)

axs[0, 1].set(title=r'$\delta^{18}$O/distance (Atlantic)')
axs[0, 1].axvline((0.5/387.5), color='r')

plt.show()
