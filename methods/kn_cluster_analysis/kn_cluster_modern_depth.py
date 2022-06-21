import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import subplots, show
from pandas import read_csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from os import chdir
from shapefile import Reader
from mpl_toolkits import mplot3d

from methods.general.general_constants import kmeans_kwargs
from methods.general.general_functions import within_stddev
from methods.kn_cluster_analysis.kn_functions import assess_cluster_model

# Change the working directory to sit at the start of the folder architecture
chdir("../..")

# Chose the core tops to look at
ocean = "Atlantic"
path_to_data = "data/core_tops/atlantic_core_tops.csv"

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
model_run = KMeans(n_clusters=num_clusters, **kmeans_kwargs).fit(scaled)
selected["predicted_cluster"] = model_run.labels_

# Write the data to a csv file (if desired)
# path_to_exit_data = "data/cluster_data/{}.csv".format("modern_clusters")
# selected.to_csv(path_to_exit_data)

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

show()
