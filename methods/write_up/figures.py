import os

import pandas as pd
import geopy.distance as dst
import matplotlib.pyplot as plt
import numpy as np

from methods.isotope_statistics.statistics_functions import plotting_confidence_intervals


# Some facts about 1208 and 1209
coord_1209 = (32.651660, 158.505930)
coord_1208 = (36.127160, 158.201580)
depth_1209 = 2387.2
depth_1208 = 3345.7
distance_1208_1209 = 386.5495426341468  # km
depth_1208_1209 = 0.9585  # km

colours = ['#7fc97f', '#beaed4', '#fdc086']


def value_by_distance(dataset: pd.DataFrame, value: str = 'd18O', threshold: int = 500) -> list:
    """
    Returns a selection of a dataset of locations grouped by values within a certain distance (in km).
    :param dataset: the dataset containing locations (with a latitude and longitude value), depths,
    and a value to be measured - often d18O.
    :param value: The value to be compared.
    :param threshold: The distance threshold within which points must lie.
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
                if (distance_value != 0) and (distance_value < threshold):
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


def write_data_files(threshold: int = 500):
    """
    Write the distance data to CSV files
    :param threshold: threshold for distance between points
    :return:
    """
    # LOAD THE DATA
    atlantic = pd.read_csv('data/selected_core_tops/atlantic_core_tops.csv').dropna(subset=["d18O"])
    pacific = pd.read_csv('data/selected_core_tops/pacific_core_tops.csv').dropna(subset=["d18O"])

    pacific = pd.DataFrame(value_by_distance(pacific, value='d18O', threshold=threshold))
    atlantic = pd.DataFrame(value_by_distance(atlantic, value='d18O', threshold=threshold))

    pacific.to_csv("data/distance_data/pacific_distances_{}.csv".format(threshold))
    atlantic.to_csv("data/distance_data/atlantic_distances_{}.csv".format(threshold))


def isotope_by_depth(pacific_data: pd.DataFrame, atlantic_data: pd.DataFrame, title: str = 'Figure',
                     save_fig: bool = False):
    """
    Plots up the difference in isotopes between sites within the threshold over the distance
    :param pacific_data:
    :param atlantic_data:
    :param title:
    :param save_fig:
    :return:
    """
    # Define figure
    fig, axs = plt.subplots(
        nrows=2,
        ncols=2,
        sharex='col',
        figsize=(8, 8)
    )

    # Define the limit of the x values
    x_limit = 20

    # Make sure we don't get any divide by 0 errors
    atlantic = atlantic_data[atlantic_data.del_depth != 0]
    pacific = pacific_data[pacific_data.del_depth != 0]

    # Determine the mean and 95% confidence intervals for the distributions
    mean_iso_depth_atl, conf_int_iso_depth_atl, _ = plotting_confidence_intervals(
        (atlantic.del_d18O / (atlantic.del_depth/1000))
    )
    mean_iso_depth_pac, conf_int_iso_depth_pac, _ = plotting_confidence_intervals(
        (pacific.del_d18O / (pacific.del_depth/1000))
    )

    mean_iso_dist_atl, conf_int_iso_dist_atl, _ = plotting_confidence_intervals((atlantic.del_d18O / atlantic.del_dist))
    mean_iso_dist_pac, conf_int_iso_dist_pac, _ = plotting_confidence_intervals((pacific.del_d18O / pacific.del_dist))

    fig.suptitle(title)

    # Plot up the histograms
    n, _, _ = axs[0, 0].hist(
        (atlantic.del_d18O / (atlantic.del_depth/1000)),
        bins=np.linspace(
            start=0,
            stop=x_limit,
            num=100
        ),
        density=False,
        color=colours[0]
    )

    axs[0, 0].axvline(
        (0.5 / 0.9585),
        color='r',
        label="1208/09"
    )

    axs[0, 0].text(
        (0.5 / 0.9585) + 0.5,
        (max(n) / 2),
        "{} = {:.6f}".format('z', (0.5 / 0.9585)),
        rotation=90,
        verticalalignment='center'
    )

    axs[0, 0].axvline(
        mean_iso_depth_atl,
        color='k',
        label="Mean"
    )

    axs[0, 0].text(
        mean_iso_depth_atl + 0.5,
        (max(n) / 2),
        "{} = {:.6f}".format(r'$\bar{x}$', mean_iso_depth_atl),
        rotation=90,
        verticalalignment='center'
    )

    axs[0, 0].axvline(
        conf_int_iso_depth_atl,
        color='g',
        label="95% Conf Int"
    )

    axs[0, 0].text(
        conf_int_iso_depth_atl + 0.5,
        (max(n) / 2),
        "{} = {:.6f}".format(r'$\sigma$', conf_int_iso_depth_atl),
        rotation=90,
        verticalalignment='center'
    )

    n, _, _ = axs[1, 0].hist((pacific.del_d18O / (pacific.del_depth/1000)),
                             bins=np.linspace(start=0, stop=x_limit, num=100), density=False, color=colours[1])
    axs[1, 0].axvline((0.5 / 0.9585), color='r', label="1208/09")
    axs[1, 0].text((0.5 / 0.9585) + 0.5, (max(n) / 2), "{} = {:.6f}".format('z', (0.5 / 0.9585)), rotation=90,
                   verticalalignment='center')
    axs[1, 0].axvline(mean_iso_depth_pac, color='k', label="Mean")
    axs[1, 0].text(mean_iso_depth_pac + 0.5, (max(n) / 2), "{} = {:.6f}".format(r'$\bar{x}$', mean_iso_depth_pac), rotation=90, verticalalignment='center')
    axs[1, 0].axvline(conf_int_iso_depth_pac, color='g', label="95% Conf Int")
    axs[1, 0].text(conf_int_iso_depth_pac + 0.5, (max(n) / 2), "{} = {:.6f}".format(r'$\sigma$', conf_int_iso_depth_pac), rotation=90, verticalalignment='center')

    axs[0, 0].set(xlim=[0, x_limit], title='Atlantic')
    axs[1, 0].set(xlabel='{}/depth ({}/km)'.format(r'$\delta^{18}$O', u"\u2030"), title="Pacific")

    # Distance d18O differences
    x_limit = 0.05
    n, _, _ = axs[0, 1].hist(
        (atlantic.del_d18O / atlantic.del_dist),
        bins=np.linspace(
            start=0,
            stop=x_limit,
            num=100
        ),
        density=False,
        color=colours[0]
    )
    axs[0, 1].axvline((0.5 / 386.5495426341468), color='r', label="1208/09")
    axs[0, 1].text((0.5 / 386.5495426341468) + 0.001, (max(n) / 2),
                   "{} = {:.6f}".format('z', (0.5 / 386.5495426341468)),
                   rotation=90,
                   verticalalignment='center')
    axs[0, 1].axvline(mean_iso_dist_atl, color='k', label="Mean")
    axs[0, 1].text(mean_iso_dist_atl + 0.001, (max(n) / 2), "{} = {:.6f}".format(r'$\bar{x}$', mean_iso_dist_atl), rotation=90,
                   verticalalignment='center')
    axs[0, 1].axvline(conf_int_iso_dist_atl, color='g', label="95% Conf Int")
    axs[0, 1].text(conf_int_iso_dist_atl + 0.001, (max(n) / 2), "{} = {:.6f}".format(r'$\sigma$', conf_int_iso_dist_atl), rotation=90,
                   verticalalignment='center')

    n, _, _ = axs[1, 1].hist(
        (pacific.del_d18O / pacific.del_dist),
        bins=np.linspace(
            start=0,
            stop=x_limit,
            num=100
        ),
        density=False,
        color=colours[1]
    )
    axs[1, 1].axvline((0.5 / 386.5495426341468), color='r', label="1208/09")
    axs[1, 1].text((0.5 / 386.5495426341468) + 0.001, (max(n) / 2), "{} = {:.6f}".format('z', (0.5 / 386.5495426341468)), rotation=90,
                   verticalalignment='center')
    axs[1, 1].axvline(mean_iso_dist_pac, color='k', label="Mean")
    axs[1, 1].text(mean_iso_dist_pac + 0.001, (max(n) / 2), "{} = {:.6f}".format(r'$\bar{x}$', mean_iso_dist_pac), rotation=90,
                   verticalalignment='center')
    axs[1, 1].axvline(conf_int_iso_dist_pac, color='g', label="95% Conf Int")
    axs[1, 1].text(conf_int_iso_dist_pac + 0.001, (max(n) / 2), "{} = {:.6f}".format(r'$\sigma$', conf_int_iso_dist_pac), rotation=90,
                   verticalalignment='center')

    axs[0, 1].set(xlim=[0, x_limit], title='Atlantic')
    axs[1, 1].set(xlabel='{}/distance ({}/km)'.format(r'$\delta^{18}$O', u"\u2030"), title="Pacific")

    if save_fig:
        plt.savefig("figures/figure_01.png", format='png', dpi=150)
    else:
        plt.show()


def absolute_differences(pacific_data: pd.DataFrame, atlantic_data: pd.DataFrame, title: str = 'Figure_01',
                         save_fig: bool = False, conf_int: int = 95):

    mean_iso_atl, conf_int_iso_atl, _ = plotting_confidence_intervals(atlantic_data.del_d18O, conf_int=conf_int)
    mean_iso_pac, conf_int_iso_pac, _ = plotting_confidence_intervals(pacific_data.del_d18O, conf_int=conf_int)

    # Set up figure
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 8), sharex='all')

    fig.suptitle(title)

    n, _, _ = axs[0].hist(atlantic_data.del_d18O, bins=30, density=True, color=colours[0])
    axs[0].axvline(conf_int_iso_atl, color='b', ls='--', label="95% Conf Int")
    axs[0].text(conf_int_iso_atl + 0.01, (max(n) / 2), "{} = {:.6f}".format(r'$\sigma$', conf_int_iso_atl),
                rotation=90, verticalalignment='center')
    axs[0].axvline(mean_iso_atl, color='k', label="Mean")
    axs[0].text(mean_iso_atl + 0.01, (max(n) / 2), "{} = {:.6f}".format(r'$\bar{x}$', mean_iso_atl), rotation=90,
                verticalalignment='center')

    n, _, _ = axs[1].hist(pacific_data.del_d18O, bins=30, density=True, color=colours[1])
    axs[1].axvline(conf_int_iso_pac, color='b', ls='--', label="95% Conf Int")
    axs[1].text(conf_int_iso_pac + 0.01, (max(n) / 2), "{} = {:.6f}".format(r'$\sigma$', conf_int_iso_pac),
                rotation=90, verticalalignment='center')
    axs[1].axvline(mean_iso_pac, color='k', label="Mean")
    axs[1].text(mean_iso_pac + 0.01, (max(n) / 2), "{} = {:.6f}".format(r'$\bar{x}$', mean_iso_atl), rotation=90,
                verticalalignment='center')

    axs[0].set(title='Atlantic')
    axs[1].set(xlabel="{} ({} VPDB)".format(r'$\Delta \delta^{18}$O', u"\u2030"), title='Pacific')

    for ax in axs:
        ax.legend(shadow=False)
        ax.set(ylabel='Population Density', ylim=[0, 3.2])

    if save_fig:
        plt.savefig("figures/figure_s4.png", format='png', dpi=150)
    else:
        plt.show()


if __name__ == '__main__':
    os.chdir('../..')

    limit = 500
    absolute_differences(
        atlantic_data=pd.read_csv("data/distance_data/atlantic_distances_{}.csv".format(limit)),
        pacific_data=pd.read_csv("data/distance_data/pacific_distances_{}.csv".format(limit)),
        title='Oxygen Isotope Differences within {}km limit'.format(limit),
        save_fig=True,
        conf_int=95
    )


