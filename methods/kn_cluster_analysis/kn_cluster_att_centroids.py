import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
import os

# This is the make sure that it ends up in the correct directory because for some reason without it nothing works.
os.chdir("../..")  # EDMOND - YOU MAY NEED TO REMOVE THIS

def generate_pliocene_clusters(save_fig: bool = False) -> None:

    init_dataset = pd.read_csv("data/assessment.csv")  # Replace with path to assessment.csv

    # List of time periods in the Pliocene - the assessment CSV is grouped by these time periods
    sections = ["3500 ka - M2", "M2", "mPWP-1", "KM2", "mPWP-2", "G20", "G20 - 2800 ka", "iNHG"]

    # Generate 3x3 figure.
    fig, axs = plt.subplots(3, 3)
    i, j = 0, 0

    # Generate another 3x3 figure.
    _, ixs = plt.subplots(3, 3)

    for section in sections:
        # Look at a particular Pliocene time slice
        dataset = init_dataset[init_dataset.TimePeriod == section]
        # Drop any empty features
        dataset = dataset.dropna()

        # Run the k means with 3 clusters.
        kmeans = KMeans(n_clusters=3)

        # Predict the clusters based on this result
        dataset['cluster'] = kmeans.fit_predict(dataset[['d18O', 'd13C']])

        # Get the centroids of each of the clusters.
        centroids = kmeans.cluster_centers_
        cen_d18O = [i[0] for i in centroids]
        cen_d13C = [i[1] for i in centroids]

        # Add the centroids of the clusters to dataframe (repeated for each of the three clusters)
        dataset['cen_x'] = dataset.cluster.map({0: cen_d18O[0], 1: cen_d18O[1], 2: cen_d18O[2]})
        dataset['cen_y'] = dataset.cluster.map({0: cen_d13C[0], 1: cen_d13C[1], 2: cen_d13C[2]})

        # Define and map colours (red, blue, green).
        colors = ['#DF2020', '#81DF20', '#2095DF']
        # Add the colour map to the dataframe corresponding to each of the cluster ids from line 33
        dataset['c'] = dataset.cluster.map({0: colors[0], 1: colors[1], 2: colors[2]})

        # Plot the dataset, coloured according to above colourmap
        axs[i, j].scatter(dataset.d18O, dataset.d13C, c=dataset.c, alpha=0.6, s=20, marker='+')
        # Plot the dataset but not grouped according to cluster for comparison
        ixs[i, j].scatter(dataset.d18O, dataset.d13C, alpha=0.6, s=20, marker='+')

        # Plot the centroids of the clusters
        axs[i, j].scatter(cen_d18O, cen_d13C, marker='o', c=colors, s=50)

        # Plot lines from centroids to data points
        for idx, val in dataset.iterrows():
            # x (below) is a line from the value to the centroid
            x = [val.d18O, val.cen_x]
            y = [val.d13C, val.cen_y]
            # Plot both the lines
            axs[i, j].plot(x, y, c=val.c, alpha=0.2)

        # title and labels
        axs[i, j].set(title='{}'.format(section))
        ixs[i, j].set(title='{}'.format(section))

        # For each time slice, also generate a single figure with the clusters just for that slice.
        fig, ax = plt.subplots()
        fig.suptitle(section)
        ax.scatter(dataset.d18O, dataset.d13C, c=dataset.c, alpha=0.6, s=20, marker='+')
        ax.scatter(cen_d18O, cen_d13C, marker='o', c=colors, s=50)
        ax.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[1.5, 4.5], ylim=[-1, 1.5])
        # Plot lines from centroids to data points
        for _, val in dataset.iterrows():
            # x (below) is a line from the value to the centroid
            x = [val.d18O, val.cen_x]
            y = [val.d13C, val.cen_y]
            # Plot both the lines
            ax.plot(x, y, c=val.c, alpha=0.2)
            ax.annotate(val.Site, (val.d18O, val.d13C), fontsize="xx-small")

        j += 1
        if j >= 3:
            j = 0
            i += 1


    for ax in axs.flat:
        ax.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[1.5, 4.5], ylim=[-1, 1.5])
        ax.label_outer()

    for ax in ixs.flat:
        ax.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[1.5, 4.5], ylim=[-1, 1.5])
        ax.label_outer()

    if save_fig:
        plt.savefig("Cluster_Figure_01.png", format="png")
    else:
        plt.show()


if __name__ == "__main__":
    generate_pliocene_clusters(save_fig=False)