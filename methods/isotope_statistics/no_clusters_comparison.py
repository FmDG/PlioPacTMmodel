from os import chdir

import matplotlib.pyplot as plt
from pandas import read_csv

from methods.general.general_constants import axis_args, time_sets


def oceans_comparison(title="Comparisons"):

    # Paths to datasets
    plio_pac_path = "data/outliers_removed/pacific_pliocene.csv"
    mod_atlan_path = "data/outliers_removed/modern_atlantic.csv"
    mod_pac_path = "data/outliers_removed/pacific_modern.csv"
    mod_ocean_path = "data/outliers_removed/modern_oceans.csv"

    # Read the dataset into pandas dataframes
    atlan_data = read_csv(mod_atlan_path)
    pac_data = read_csv(mod_pac_path)
    plio_data = read_csv(plio_pac_path)

    modern_oceans = read_csv(mod_ocean_path)

    # Remove NAN values
    plio_data = plio_data.dropna(subset=["d18O", "d13C"])

    # define plotting arguments
    plot_args = {
        "x": "d18O",
        "y": "d13C",
        'marker': "+",

    }

    # Load the colours
    colours = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0']
    datasets = [atlan_data, pac_data]
    names = ["Modern Atlantic", "Modern Pacific"]

    minimum_x = modern_oceans.d18O.min() - 0.5
    maximum_x = modern_oceans.d18O.max() + 0.5
    difference = modern_oceans.d13C.mean() - modern_oceans.d18O.mean()

    fig, axs = plt.subplots(2, 2, figsize=[12, 12])
    q = 0
    p = 0

    fog, uxs = plt.subplots(figsize=[12, 12])

    for j in range(len(time_sets)):
        period = time_sets[j][0]
        used_data = plio_data[plio_data.TimePeriod == period]

        fig.suptitle("Modern and Past Pacific Ocean Isotope Space")
        fog.suptitle("Past Pacific Ocean Isotope Space")

        for i in range(len(datasets)):
            axs[q, p].scatter(
                data=datasets[i],
                c=colours[i],
                alpha=1,
                label=names[i],
                **plot_args
            )

        axs[q, p].scatter(
            data=used_data,
            c='k',
            alpha=1,
            label=period,
            **plot_args
        )

        axs[q, p].set(title=period, xlim=[minimum_x, maximum_x], ylim=[minimum_x + difference, maximum_x + difference], **axis_args)
        axs[q, p].invert_xaxis()
        axs[q, p].legend()

        uxs.scatter(
            data=used_data,
            c=colours[j],
            alpha=1,
            label=period,
            **plot_args
        )
        uxs.legend()
        uxs.invert_xaxis()
        uxs.set(xlim=[minimum_x, maximum_x], ylim=[minimum_x + difference, maximum_x + difference], **axis_args)

        # Annotate all the values in the plot
        for _, values in used_data.iterrows():
            axs[q, p].annotate(values.Site, ((values.d18O + 0.05), (values.d13C + 0.05)), fontsize="xx-small")

        q += 1
        if q >= 2:
            q = 0
            p += 1

    plt.show()


if __name__ == "__main__":
    chdir("../..")
    oceans_comparison()
