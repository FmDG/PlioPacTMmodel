import matplotlib.pyplot as plt
from json import load
from os import chdir
import numpy as np


# Read the d18O/distance data from write_gradient_lists.py
chdir("../..")
with open("data/permanent_lists/pacific_d18O_differences.json", 'r') as f:
    pacific_d18Os = load(f)

with open("data/permanent_lists/southern_d18O_differences.json", 'r') as f:
    southern_d18Os = load(f)

with open("data/permanent_lists/atlantic_d18O_differences.json", 'r') as f:
    atlantic_d18Os = load(f)


# Plot how unusual this result is.
_, axs = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(8, 8)
)

axs[0, 0].hist(
    pacific_d18Os,
    bins=np.linspace(
        start=-3,
        stop=3,
        num=100
    ),
    density=True
)

axs[0, 0].set(title=r'$\delta^{18}$O (Pacific)', xlim=[-3, 3], ylim=[0, 1])
axs[0, 0].axvline(0.5, color='r')

axs[1, 0].hist(
    southern_d18Os,
    bins=np.linspace(
        start=-3,
        stop=3,
        num=100
    ),
    density=True
)

axs[1, 0].set(title=r'$\delta^{18}$O (Southern)', xlim=[-3, 3], ylim=[0, 1])
axs[1, 0].axvline(0.5, color='r')

axs[0, 1].hist(
    atlantic_d18Os,
    bins=np.linspace(
        start=-3,
        stop=3,
        num=100
    ),
    density=True
)

axs[0, 1].set(title=r'$\delta^{18}$O (Atlantic)', xlim=[-3, 3], ylim=[0, 1])
axs[0, 1].axvline(0.5, color='r')

plt.show()