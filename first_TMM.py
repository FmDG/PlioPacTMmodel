"""
Attempting to build the first version of the model using the PRISM data held in prism_data.db

"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import math


def plot_dist(period, dataset, show=False):
    """
    This function takes in a string defining the time period, as well as the dataset containing the mean
    d18O and d13C values for each site in the dataset and returns a plot showing where these plots are in isotope space
    for this speific time period

    :param period: A string defining the exact time period which we wish to generate a plot for.
    :param dataset: The dataset containing the
    :param show: show the plot at the end of the function
    :return: There is no return for this function, but plt.show() is required to see the plots.
    """
    fig, ax = plt.subplots()
    fig.suptitle(period)

    subset = dataset[dataset.TimePeriod == period]

    ax.scatter(x="d18O", y="d13C", data=subset, marker="+")
    ax.set(xlim=[1.8, 4.2], ylim=[-1.0, 1.0], xlabel=r'$\delta^{18}$O', ylabel="d13C")

    for index, row in subset.iterrows():
        label = row.Site

        plt.annotate(label,  # this is the text
                     (row.d18O, row.d13C),          # these are the coordinates to position the label
                     textcoords="offset points",    # how to position the text
                     xytext=(0, 10),                # distance from text to points (x,y)
                     ha='center')                   # horizontal alignment can be left, right or center

    if show:
        plt.show()
    else:
        return


def plot_subplots(dataset, periods, show=False):
    squares = int(math.ceil(math.sqrt(len(periods))))
    fig, axs = plt.subplots(squares, squares)

    i, j = 0, 0
    for x in periods:
        subset = dataset[dataset.TimePeriod == x]
        axs[i, j].scatter(x="d18O", y="d13C", data=subset, marker="+")
        axs[i, j].set(xlim=[1.8, 4.2], ylim=[-1.0, 1.0], xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', title=x)
        j += 1
        if j >= squares:
            j = 0
            i += 1

    for ax in fig.get_axes():
        ax.label_outer()

    if show:
        plt.show()


# connect to the database
connection = sqlite3.connect("data/prism_data.db")
sites = pd.read_sql("SELECT * FROM isotopes", connection)
connection.close()

# list the time periods we're using for this first run of the model
time_periods = ["3500 ka - M2", "M2", "mPWP-1", "KM2", "mPWP-2", "G20", "G20 - 2800 ka", "iNHG"]

plot_subplots(sites, time_periods)

for sx in time_periods:
    plot_dist(sx, sites)

plt.show()
