import matplotlib.pyplot as plt
from json import load
from os import chdir
import numpy as np

from methods.isotope_statistics.statistics_functions import plotting_confidence_intervals

# Read the d18O/distance data from write_gradient_lists.py
chdir("../..")

# This is the distance between 1209 and 1208, and the d18O difference observed.
print("{}km between 1209 and 1208, means a difference of 0.5 per mil is about {:.4f} per km".format(387.5, (0.5/387.5)))

time_periods = ["early_pleistocene", "inhg", 'mid_pleistocene', "mpwp"]
start, stop, num_bins = 0, 0.005, 40
for time_stamp in time_periods:
    with open("data/permanent_lists/{}_d18O_gradients.json".format(time_stamp), 'r') as f:
        d18O_gradient = load(f)

    # Determine Confidence intervals
    men, confit, _ = plotting_confidence_intervals(d18O_gradient)

    # Plot how unusual this result is.
    fig, ax = plt.subplots(figsize=(8, 8))

    fig.suptitle("{}/distance gradient for {} Ocean ({}/km)".format(r'$\delta^{18}$O', time_stamp.capitalize(), "\u2030"))

    n, _, _ = ax.hist(d18O_gradient, bins=np.linspace(start=start, stop=stop, num=num_bins), density=False)
    ax.set(xlim=[start, stop])
    ax.axvline((0.5 / 387.5), color='r', label="1208/09 {} gradient ".format(r'$\delta^{18}$O'))
    ax.text((0.5 / 387.5) + 0.00001, (max(n) / 2), "{:.6f}".format((0.5 / 387.5)), rotation=90, verticalalignment='center')
    ax.axvline(men, color='k', label="Mean")
    ax.text(men + 0.00001, (max(n) / 2), "{:.6f}".format(men), rotation=90, verticalalignment='center')
    ax.axvline(confit, color='g', label="95% Confidence Interval")
    ax.text(confit + 0.00001, (max(n)/2), "{:.6f}".format(confit), rotation=90, verticalalignment='center')
    ax.legend()

    # plt.savefig("figures/Exp_Function/{}_stats.png".format(time_stamp), format="png")


plt.show()