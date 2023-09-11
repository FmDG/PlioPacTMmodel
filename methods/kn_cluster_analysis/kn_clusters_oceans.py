from os import chdir

from matplotlib.lines import Line2D
from matplotlib.pyplot import subplots, show
from pandas import read_csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from methods.general.general_constants import time_sets, kmeans_kwargs, axis_args
from methods.kn_cluster_analysis.kn_functions import assess_cluster_model


def modern_oceans():

    # Paths to datasets
    plio_pac_path = "data/pacific_pliocene.csv"
    mod_atlan_path = "data/selected_core_tops/atlantic_core_tops.csv"
    mod_pac_path = "data/outliers_removed/pacific_modern.csv"
    mod_ocean_path = "data/all_core_tops.csv"

    title = "Comparative Modern/Pliocene Clusters"

    # Read the dataset into pandas dataframes
    pandas_data = read_csv(mod_atlan_path)

    # Overlay the Pliocene Data
    plio_data = read_csv(plio_pac_path)
    # Select the appropriate time frame
    plio_data = plio_data[plio_data.TimePeriod == "Mid-Pliocene"]
    plio_data = plio_data.dropna(subset=["d18O", "d13C"])

    # Select and drop any empty features from run
    selected = pandas_data.dropna(subset=["d18O", "d13C"])
    # Scale the features to sit with a mean of 0 and a std. dev of 1
    scaled = StandardScaler().fit_transform(selected[["d18O", "d13C"]])

    # Determine the ideal number of clusters
    num_clusters = assess_cluster_model(scaled, max_runs=8, full_return=False)

    # Run the model with this number of clusters and add the results to the dataframe.
    model_run = KMeans(n_clusters=num_clusters, **kmeans_kwargs)

    # Predict the clusters based on this result
    selected['predicted_cluster'] = model_run.fit_predict(selected[['d18O', 'd13C']])

    # Get the centroids
    centroids = model_run.cluster_centers_
    cen_d18o = [i[0] for i in centroids]
    cen_d13c = [i[1] for i in centroids]

    # Write the data to a csv file
    # selected.to_csv(path_to_exit_data)

    # Define and map colors onto the clusters defined above
    colours = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
    # Map the colours onto the selected clusters
    selected["cluster_colour"] = selected.predicted_cluster.map(
        {i: colours[i] for i in range(num_clusters)}
    )

    # Add the centroids to each point
    selected["cen_x"] = selected.predicted_cluster.map(
        {i: cen_d18o[i] for i in range(num_clusters)}
    )
    selected["cen_y"] = selected.predicted_cluster.map(
        {i: cen_d13c[i] for i in range(num_clusters)}
    )

    # define the figure
    fig, ax = subplots(1, figsize=(8, 8))

    # Plot the data coloured according to the cluster colours defined above
    ax.scatter(
        data=selected,
        x="d18O",
        y="d13C",
        c="cluster_colour",
        marker="o",
        s=10,
        alpha=0.5
    )

    minimum_x = selected.d18O.min() - 0.5
    maximum_x = selected.d18O.max() + 0.5
    difference = selected.d13C.mean() - selected.d18O.mean()

    # Select a subset of the colours for the centroids
    centroid_colours = colours[0:num_clusters]

    # Plot the centroids of the clusters
    ax.scatter(
        cen_d18o,
        cen_d13c,
        marker='+',
        c=centroid_colours,
        s=50
    )

    # Plot lines from centroids to data points
    for idx, val in selected.iterrows():
        # x (below) is a line from the value to the centroid
        x = [val.d18O, val.cen_x]
        y = [val.d13C, val.cen_y]
        # Plot both the lines
        ax.plot(x, y, c=val.cluster_colour, alpha=0.2)

    # Legend elements are created independently of MATPLOTLIB functions
    legend_elements = [
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            label='Cluster {}'.format(i+1),
            markerfacecolor=colours[i],
            markersize=5
        ) for i in range(num_clusters)
    ]

    legend_elements.append(
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            label="Pliocene Data (mid Pliocene)",
            markerfacecolor='k',
            markersize=5
        )
    )

    ax.legend(
        handles=legend_elements,
        loc='upper right'
    )

    # Plot the Pliocene Data over the top
    ax.scatter(
        data=plio_data,
        x="d18O",
        y="d13C",
        c='k',
        marker='o',
        s=10,
        alpha=1
    )

    # Annotate all the values in the plot
    for _, values in plio_data.iterrows():
        ax.annotate(values.Site, ((values.d18O + 0.05), (values.d13C + 0.05)), fontsize="xx-small")

    ax.set(title=title, xlim=[minimum_x, maximum_x], ylim=[minimum_x + difference, maximum_x + difference], **axis_args)
    ax.invert_xaxis()

    show()


if __name__ == "__main__":
    chdir("../..")
    modern_oceans()
