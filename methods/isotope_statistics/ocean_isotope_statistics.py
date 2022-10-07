from os import chdir

import matplotlib.pyplot as plt
from pandas import read_csv
from scipy.stats import pearsonr

from methods.general.general_functions import within_stddev
from statistics_functions import isotope_by_factor, plot_by_factor


def plot_depth_variation(dataset, save_fig: bool = False) -> bool:

    parameter, step_size = "depth", 1000
    depth_influence = isotope_by_factor(
        dataset=dataset,
        factor=parameter,
        minimum=-0,
        maximum=5000,
        step_size=step_size
    )

    plot_by_factor(
        dataset=dataset,
        factor_dataset=depth_influence,
        factor=parameter,
        step_size=step_size,
        fig_title="Influence of Depth on Pacific Isotopes"
    )

    if save_fig:
        plt.savefig("figures/ocean_isotopes_figure_1.png", format='png', dpi=150)
    else:
        plt.show()

    return True


if __name__ == '__main__':
    # Read the Pacific Modern Core Top Data
    chdir("../..")
    pacific = read_csv('data/pacific_modern.csv')
    # atlantic = read_csv("data/atlantic_modern.csv")

    # Remove values that are more than 3 standard deviations away from the mean
    pacific = within_stddev(
        within_stddev(
            pacific,
            "d18O",
            num_devs=3
        ),
        "d13C",
        num_devs=3
    )

    plot_depth_variation(pacific, save_fig=False)