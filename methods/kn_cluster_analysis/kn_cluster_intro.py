"""
Some Notes on Clustering Algorithms

Partitional clustering divides data objects into non-overlapping groups. In other words, no object can be a member of
more than one cluster, and every cluster must have at least one object. This requires specifying the number of clusters,
k, which will be used by the algorithm.

Hierarchical clustering determines cluster assignments by building a hierarchy. This is implemented by either a
bottom-up or a top-down approach:
- Agglomerative clustering is the bottom-up approach. It merges the two points that are the most similar until all
points have been merged into a single cluster.
- Divisive clustering is the top-down approach. It starts with all points as one cluster and splits the least similar
clusters at each step until only single data points remain.

Density-based clustering determines cluster assignments based on the density of data points in a region. Clusters are
assigned where there are high densities of data points separated by low-density regions.

"""

import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

features, true_labels = make_blobs(
    n_samples=200,
    centers=3,
    cluster_std=2.75,
    random_state=None
)

'''
- Machine learning algorithms need to consider all features on an even playing field. That means the values for all 
features must be transformed to the same scale.
- The process of transforming numerical features to use the same scale is known as feature scaling. It’s an important 
data preprocessing step for most distance-based machine learning algorithms because it can have a significant impact on 
the performance of your algorithm.
'''

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

'''
Here are the parameters used in this example:
- init controls the initialization technique. The standard version of the k-means algorithm is implemented by setting 
init to "random". Setting this to "k-means++" employs an advanced trick to speed up convergence, which you’ll use later.
- n_clusters sets k for the clustering step. This is the most important parameter for k-means.
- n_init sets the number of initializations to perform. This is important because two runs can converge on different 
cluster assignments. The default behavior for the scikit-learn algorithm is to perform ten k-means runs and return the results of the one with the lowest SSE.
- max_iter sets the number of maximum iterations for each initialization of the k-means algorithm.
'''

kmeans = KMeans(
    init="random",
    n_clusters=3,
    n_init=10,
    max_iter=300,
    random_state=42
)

kmeans.fit(scaled_features)

# The lowest SSE value
print("The Lowest SSE Value: {}".format(kmeans.inertia_))

# Final locations of the centroid
print("The final locations of the centroids: \n{}".format(kmeans.cluster_centers_))

# The number of iterations required to converge
print("The number of iterations required to converge: {}".format(kmeans.n_iter_))

# Five predicted labels
print("Five predicted labels: {}".format(kmeans.labels_[:5]))

# Five true labels
print("Five true labels: {}".format(true_labels[:5]))

"""
These are often used as complementary evaluation techniques rather than one being preferred over the other. To perform 
the elbow method, run several k-means, increment k with each iteration, and record the SSE:
"""

kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

# A list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)

'''
When you plot SSE as a function of the number of clusters, notice that SSE continues to decrease as you increase k. As 
more centroids are added, the distance from each point to its closest centroid will decrease.

There’s a sweet spot where the SSE curve starts to bend known as the elbow point. The x-value of this point is thought 
to be a reasonable trade-off between error and number of clusters. In this example, the elbow is located at x=3:
'''

plt.style.use("fivethirtyeight")
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

'''
Determining the elbow point in the SSE curve isn’t always straightforward. If you’re having trouble choosing the elbow 
point of the curve, then you could use a Python package, kneed, to identify the elbow point programmatically:
'''

kl = KneeLocator(
    range(1, 11), sse, curve="convex", direction="decreasing"
)

print("Knee Locator elbow position: {}".format(kl.elbow))

'''
The silhouette coefficient is a measure of cluster cohesion and separation. It quantifies how well a data point fits 
into its assigned cluster based on two factors:

How close the data point is to other points in the cluster
How far away the data point is from points in other clusters
Silhouette coefficient values range between -1 and 1. Larger numbers indicate that samples are closer to their clusters 
than they are to other clusters.
'''

# A list holds the silhouette coefficients for each k
silhouette_coefficients = []

# Notice you start at 2 clusters for silhouette coefficient
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    score = silhouette_score(scaled_features, kmeans.labels_)
    silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(range(2, 11), silhouette_coefficients)
plt.xticks(range(2, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
plt.show()
