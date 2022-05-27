import matplotlib.pyplot as plt
from json import load
from os import chdir
import numpy as np


# Read the d18O/distance data from write_distance_lists.py
chdir("../..")
with open("data/permanent_lists/pacific_core_distances.json", 'r') as f:
    pacific_d18O_by_distance = load(f)

with open("data/permanent_lists/southern_core_distances.json", 'r') as f:
    southern_d18O_by_distance = load(f)

with open("data/permanent_lists/atlantic_core_distances.json", 'r') as f:
    atlantic_d18O_by_distance = load(f)

# This is the distance between 1209 and 1208, and the d18O difference observed.
print("{}km between 1209 and 1208, means a difference of 0.5 per mil is about {:.4f} per km".format(387.5, (0.5/387.5)))
high_point = 5500

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
    ),
    density=True
)

axs[0, 0].set(title=r'$\delta^{18}$O/distance (Pacific)', ylim=[0, high_point])
axs[0, 0].axvline((0.5/387.5), color='r')

axs[1, 0].hist(
    southern_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=1000
    ),
    density=True
)

axs[1, 0].set(title=r'$\delta^{18}$O/distance (Southern)', ylim=[0, high_point])
axs[1, 0].axvline((0.5/387.5), color='r')

axs[0, 1].hist(
    atlantic_d18O_by_distance,
    bins=1000,
    density=True
)

axs[0, 1].set(title=r'$\delta^{18}$O/distance (Atlantic)', ylim=[0, 1])
axs[0, 1].axvline((0.5/387.5), color='r')


# Plot how unusual this result is.
_, ax = plt.subplots(figsize=(8, 8))
ax.hist(
    pacific_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=100
    ),
    alpha=0.2,
    label="Pacific",
    density=True
)
ax.hist(
    southern_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=100
    ),
    alpha=0.2,
    label="Southern",
    density=True
)

ax.hist(
    atlantic_d18O_by_distance,
    bins=np.linspace(
        start=-0.002,
        stop=0.002,
        num=100
    ),
    alpha=0.2,
    label="Atlantic",
    density=True
)

ax.axvline((0.5/387.5), color='r')
ax.legend()


plt.show()
