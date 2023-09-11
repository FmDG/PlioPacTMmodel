import os

import pandas as pd
import geopy.distance as dst
import matplotlib.pyplot as plt
import numpy as np

from methods.isotope_statistics.statistics_functions import plotting_confidence_intervals


colours = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f']

# Some facts about 1208 and 1209
coord_1209 = (32.651660, 158.505930)
coord_1208 = (36.127160, 158.201580)
depth_1209 = 2387.2
depth_1208 = 3345.7
distance_1208_1209 = 386.5495426341468  # km
depth_1208_1209 = 0.9585  # km


def value_by_distance(dataset: pd.DataFrame, value: str = 'd18O') -> list:
    """
    Returns a selection of a dataset of locations grouped by values within a certain distance (in km).
    :param dataset: the dataset containing locations (with a latitude and longitude value), depths,
    and a value to be measured - often d18O.
    :param value: The value to be compared.
    :return: A list of dictionary entries containing the difference in "value", depth, and distance between all points
    below the threshold
    """
    # The list that is returned
    full_values = []
    # This list ensures no duplication
    identifiers = []
    # Iterate across the dataset
    for _, x in dataset.iterrows():
        # Iterate across the dataset again.
        for _, y in dataset.iterrows():
            # Make sure that this is not simply two of the same core
            if x['Core'] != y['Core']:
                # Determine the distance between the two cores
                distance_value = dst.distance(
                    (x.latitude, x.longitude),
                    (y.latitude, y.longitude)
                ).km
                # Determine if the cores are on top of each other or outside the threshold
                if distance_value != 0:
                    identify = [x["Core"], y["Core"]]
                    identify.sort()
                    # Make sure that this core has not already been measured
                    if identify in identifiers:
                        pass
                    else:
                        # Add the unique identifier to the list
                        identifiers.append(identify)
                        # Store the difference in 'Value', depth, and distance.
                        del_value = abs(float(x[value] - y[value]))
                        del_depth = abs(float(x.depth - y.depth))
                        full_values.append({"del_d18O": del_value, "del_dist": distance_value, "del_depth": del_depth,
                                            "identifier": identify})
    return full_values


def write_data_files(depth_cutoff: int = 0):
    """
    Write the distance data to CSV files
    :param depth_cutoff: is there a lower limit on depths of cores, in metres
    :return:
    """
    # LOAD THE DATA
    atlantic = pd.read_csv('data/selected_core_tops/atlantic_core_tops.csv').dropna(subset=["d18O"])
    pacific = pd.read_csv('data/selected_core_tops/pacific_core_tops.csv').dropna(subset=["d18O"])

    # SPLIT THE OCEAN DATA INTO NORTH AND SOUTH
    n_atlantic = atlantic[atlantic.latitude > 0]
    s_atlantic = atlantic[atlantic.latitude < 0]

    n_pacific = pacific[pacific.latitude > 0]
    s_pacific = pacific[pacific.latitude < 0]

    # Add all the oceans to a list
    oceans = [
        [n_atlantic, 'n_atlantic'],
        [s_atlantic, 's_atlantic'],
        [n_pacific, 'n_pacific'],
        [s_pacific, 's_pacific']
    ]

    # REMOVE ALL VALUES ABOVE A CERTAIN DEPTH
    for ocean in oceans:
        ocean[0] = ocean[0][ocean[0].depth > depth_cutoff]
        answer_frame = pd.DataFrame(value_by_distance(ocean[0], value='d18O'))
        answer_frame.to_csv("data/distance_data/{}_depth_{}.csv".format(ocean[1], depth_cutoff))


def absolute_differences_depth(*frames: pd.DataFrame, names: list, title: str = 'Figure_01', save_fig: bool = False,
                               conf_int: int = 95, depth_threshold: int = 1000):

    if len(names) != len(frames):
        raise ValueError("Must supply one name per frame")

    # Determine the shape of the figure
    sqrt_frames = int(np.ceil(np.sqrt(len(frames))))
    figure_list = []

    # Compile all the differences together where these differences exceeed the depth threshold
    for frame in frames:
        frame = frame[frame.del_depth > depth_threshold]
        # Calculate the mean and 95% conf. interval for the d18O differences
        mean_iso, conf_int_iso, _ = plotting_confidence_intervals(frame.del_d18O, conf_int=conf_int)
        figure_list.append([frame, mean_iso, conf_int_iso])

    # Set up figure
    fig, axs = plt.subplots(nrows=sqrt_frames, ncols=sqrt_frames, figsize=(12, 12), sharex='all', sharey='all')

    # Give the figure a title
    fig.suptitle(title)

    # For the iteration process
    i, j, k = 0, 0, 0

    for item in figure_list:
        # Determine the number of measurements here
        n = item[0].shape[0]
        # Offset for the vertical labels
        offset = 0.03
        # Plot the histograme of differences in d18O
        p, _, _ = axs[i, j].hist(item[0].del_d18O, bins=30, density=True, color=colours[k])
        # Add the mean difference in d18O
        axs[i, j].axvline(item[1], color='k', label="Mean")
        axs[i, j].text(item[1] + offset, (max(p) / 2), "{} = {:.4f}".format(r'$\bar{x}$', item[1]), rotation=90,
                       verticalalignment='center')
        # Add the 95% confidence interval in d18O difference
        axs[i, j].axvline(item[2], color='b', ls='--', label="95% Conf. Int.")
        axs[i, j].text(item[2] + offset, (max(p) / 2), "{} = {:.4f}".format(r'$\sigma$', item[2]), rotation=90,
                       verticalalignment='center')
        # Add a title to the subplot
        axs[i, j].set(title="{name}\n({maths} = {n})".format(name=names[k], maths=r'$n$', n=n),
                      xlabel="{} ({} VPDB)".format(r'$\Delta \delta^{18}$O', u"\u2030"),
                      ylabel='Population density')
        # Add a legend
        axs[i, j].legend(shadow=False, frameon=False)
        axs[i, j].label_outer()

        # Iterate over the frames
        i += 1
        k += 1
        if i >= sqrt_frames:
            j += 1
            i = 0

    # Save figure if necessary
    if save_fig:
        plt.savefig("figures/Figure_S4.png", format='png', dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    os.chdir('../..')
    cut_off = 2000
    threshold = 500

    n_atlantic = pd.read_csv("data/distance_data/n_atlantic_depth_{}.csv".format(cut_off))
    s_atlantic = pd.read_csv("data/distance_data/s_atlantic_depth_{}.csv".format(cut_off))
    n_pacific = pd.read_csv("data/distance_data/n_pacific_depth_{}.csv".format(cut_off))
    s_pacific = pd.read_csv("data/distance_data/s_pacific_depth_{}.csv".format(cut_off))

    absolute_differences_depth(
        n_atlantic, s_atlantic, n_pacific, s_pacific,
        names=["N. Atlantic", "S. Atlantic", "N. Pacific", "S. Pacific"],
        title="{} of intermediate and deep cores (> {} m depth)\n(Depth difference > {} m)".format(
            r'$\Delta \delta^{18}$O', cut_off, threshold
        ),
        save_fig=False,
        depth_threshold=threshold
    )






