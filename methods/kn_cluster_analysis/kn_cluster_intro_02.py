from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from os import chdir

chdir("../..")
features, true_labels = make_moons(
    n_samples=250, noise=0.05, random_state=42
)

scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

# Instantiate k-means and dbscan algorithms
kmeans = KMeans(n_clusters=2)
dbscan = DBSCAN(eps=0.3)

# Fit the algorithms to the features
kmeans.fit(scaled_features)
dbscan.fit(scaled_features)

# Compute the silhouette scores for each algorithm
kmeans_silhouette = silhouette_score(scaled_features, kmeans.labels_)
dbscan_silhouette = silhouette_score(scaled_features, dbscan.labels_)

print("KMean silhouette score: {}".format(kmeans_silhouette))
print("DBScans silhouette score: {}".format(dbscan_silhouette))

"""
The ARI uses true cluster assignments to measure the similarity between true and predicted labels
"""
ari_kmeans = adjusted_rand_score(true_labels, kmeans.labels_)
ari_dbscan = adjusted_rand_score(true_labels, dbscan.labels_)

print("ARI of KMeans: {:.2f}".format(ari_kmeans))
print("ARI of DBscan: {:.2f}".format(ari_dbscan))
