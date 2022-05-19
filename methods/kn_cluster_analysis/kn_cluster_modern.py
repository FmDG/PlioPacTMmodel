from matplotlib.lines import Line2D
from matplotlib.pyplot import subplots, show
from pandas import read_csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from kn_constants import kmeans_kwargs, axis_args
from kn_functions import assess_cluster_model, within_stddev

path_to_modern_data = "data/pacific_modern.csv"

# Read the datasets into pandas dataframe
mode_data = read_csv(path_to_modern_data)

selected = within_stddev(within_stddev(mode_data, "d13C"), "d18O")
selected = selected.dropna(subset=["d18O", "d13C"])
# Scale the features to sit with a mean of 0 and a std. dev of 1
scaled = StandardScaler().fit_transform(selected[["d18O", "d13C"]])

# Determine the ideal number of clusters
num_clusters = assess_cluster_model(scaled, max_runs=8, full_return=False)

# Run the model with this number of clusters and add the results to the dataframe.
model_run = KMeans(n_clusters=num_clusters, **kmeans_kwargs).fit(scaled)
selected["predicted_cluster"] = model_run.labels_

# Write the data to a csv file
path_to_exit_data = "data/cluster_data/{}.csv".format("modern_clusters")
# selected.to_csv(path_to_exit_data)

# Define and map colors onto the clusters defined above
colours = ['r', 'g', 'b', 'y', 'm', 'c', 'k']
selected["cluster_colour"] = selected.predicted_cluster.map(
    {i: colours[i] for i in range(num_clusters)}
)

fig, ax = subplots(1, figsize=(8, 8))

# Plot the data coloured according to the cluster colours defined above
ax.scatter(
    data=selected,
    x="d18O",
    y="d13C",
    c="cluster_colour",
    marker="o",
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

ax.set(title="Modern", **axis_args)

show()
