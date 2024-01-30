import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import subplots, show
from pandas import read_csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from shapefile import Reader

from methods.general.general_constants import kmeans_kwargs
from methods.general.general_functions import within_stddev
from methods.kn_cluster_analysis.kn_functions import assess_cluster_model


def modern_depth_clusters():
    # Chose the core tops to look at
    ocean = "Pacific"
    path_to_data = "data/selected_core_tops/pacific_core_tops.csv"

    # Overlay the Pliocene Data
    plio_data = read_csv("data/pacific_pliocene.csv")
    # Select the appropriate time frame
    plio_data = plio_data[plio_data.TimePeriod == "Mid-Pliocene"]
    plio_data = plio_data.dropna(subset=["d18O", "d13C"])

    # Read the datasets into pandas dataframe
    mode_data = read_csv(path_to_data)

    # Remove those values which do not sit within phi Standard Deviations
    phi = 2
    selected = within_stddev(within_stddev(mode_data, "d13C", num_devs=phi), "d18O", num_devs=phi)

    # Remove those values which have no d18O and d13C values
    selected = selected.dropna(subset=["d18O", "d13C"])

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

    # Add the centroids to each point
    selected["cen_x"] = selected.predicted_cluster.map(
        {i: cen_d18o[i] for i in range(num_clusters)}
    )
    selected["cen_y"] = selected.predicted_cluster.map(
        {i: cen_d13c[i] for i in range(num_clusters)}
    )

    # Define and map colors onto the clusters defined above
    colours = ['r', 'g', 'b', 'm', 'y', 'c', 'k']
    selected["cluster_colour"] = selected.predicted_cluster.map(
        {i: colours[i] for i in range(num_clusters)}
    )

    # Read a shapefile of the world's coastlines
    coastline_shp_path = "data/coastlines/ne_10m_coastline.shp"
    coastline_sf = Reader(coastline_shp_path)

    # Define the figure to be in 3D
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # Add the coastlines to a plot
    for shape in coastline_sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        # Plot the points with a depth (zs) of 0,
        ax.plot3D(
            xs=x, ys=y, zs=0,
            color='k',
            linewidth=0.5)
        # Limit the plot to the boundaries of a map
        ax.set(xlim=[-180, 180], ylim=[-90, 90])

    # Plot the clusters
    ax.scatter3D(
        xs=selected.longitude, ys=selected.latitude, zs=(selected.depth * -1),
        c=selected.cluster_colour,
        marker='o',
        s=10
    )

    # Legend elements are created independently of MATPLOTLIB functions
    legend_elements = [
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            label='Cluster {}'.format(i+1),
            markerfacecolor=colours[i],
            markersize=5
        ) for i in range(num_clusters)]

    ax.legend(handles=legend_elements, loc='upper right')

    fig.suptitle("Modern {} Ocean".format(ocean))

    ## Figure 2 Ocean Map
    fig = plt.figure()

    ax1 = plt.subplot2grid(shape=(3, 5), loc=(0, 0), rowspan=3)
    ax2 = plt.subplot2grid(shape=(3, 5), loc=(0, 1), colspan=4, rowspan=3)

    fig.suptitle("Modern {} Ocean".format(ocean))

    for shape in coastline_sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        # Plot the points with a depth (zs) of 0,
        ax2.plot(
            x, y,
            color='k',
            linewidth=0.5
        )
        # Limit the plot to the boundaries of a map
        ax2.set(xlim=[-180, 180], ylim=[-90, 90])

    # Plot the clusters
    ax2.scatter(
        x=selected.longitude, y=selected.latitude,
        c=selected.cluster_colour,
        marker='o',
        s=10
    )

    # Plot the clusters (Latitude:Depth)
    ax1.scatter(
        x=(selected.depth * -1), y=selected.latitude,
        c=selected.cluster_colour,
        marker='o',
        s=10
    )
    ax1.set(ylabel="Latitude ({})".format(r'$\degree$'), xlabel="Depth (m)", ylim=[-90, 90])

    # Centroids Figure 3

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
            label='Cluster {}'.format(i + 1),
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

    ax.set(title="Clusters", xlim=[minimum_x, maximum_x], ylim=[minimum_x + difference, maximum_x + difference], xlabel=r'$\delta^{18}$O',
    ylabel=r'$\delta^{13}$C')
    ax.invert_xaxis()

    show()


if __name__ == "__main__":
    os.chdir("../..")
    modern_depth_clusters()
