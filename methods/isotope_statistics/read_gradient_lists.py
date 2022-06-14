import matplotlib.pyplot as plt
from json import load
from os import chdir
import numpy as np

from methods.isotope_statistics.statistics_functions import plotting_confidence_intervals

# Read the d18O/distance data from write_gradient_lists.py
chdir("../..")

# This is the distance between 1209 and 1208, and the d18O difference observed.
print("{}km between 1209 and 1208, means a difference of 0.5 per mil is about {:.4f} per km".format(387.5, (0.5/387.5)))

oceans = ["pacific", "n_atlantic", 's_atlantic', "indian", "southern"]
start, stop, num_bins = 0, 0.003, 100
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8))
fig.suptitle("{}/distance gradient for Global Oceans ({}/km)".format(r'$\delta^{18}$O', "\u2030"))
i, j = 0, 0

for ocean in oceans:
    with open("data/permanent_lists/{}_d18O_gradients.json".format(ocean), 'r') as f:
        d18O_gradient = load(f)

    # Determine Confidence intervals
    men, confit, _ = plotting_confidence_intervals(d18O_gradient)

    # Plot how unusual this result is.

    n, _, _ = axs[i][j].hist(d18O_gradient, bins=np.linspace(start=start, stop=stop, num=num_bins), density=False)
    axs[i][j].set(xlim=[start, stop], title="{}".format(ocean.capitalize()))
    axs[i][j].axvline((0.5 / 387.5), color='r', label="1208/09")
    axs[i][j].text((0.5 / 387.5) + 0.00001, (max(n) / 2), "{:.6f}".format((0.5 / 387.5)), rotation=90, verticalalignment='center')
    axs[i][j].axvline(men, color='k', label="Mean")
    axs[i][j].text(men + 0.00001, (max(n) / 2), "{:.6f}".format(men), rotation=90, verticalalignment='center')
    axs[i][j].axvline(confit, color='g', label="95% Conf Int")
    axs[i][j].text(confit + 0.00001, (max(n)/2), "{:.6f}".format(confit), rotation=90, verticalalignment='center')
    axs[i][j].legend()

    j += 1
    if j >= 3:
        j = 0
        i += 1

    #plt.savefig("figures/Exp_Function/{}_stats.png".format(ocean), format="png")


plt.show()
