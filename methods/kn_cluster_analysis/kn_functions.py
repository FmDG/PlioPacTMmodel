from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from methods.general.general_constants import kmeans_kwargs


def assess_cluster_model(scaled_input, max_runs=8, full_return=False):
    """
    Runs cluster model for range of cluster values from 1 - 'max runs'. Returns the value with the greatest reduction in
     SSE as defined by the KneeLocator function.
    :param scaled_input: input for cluster model, as numpy array, preferably scaled with a mean of 0 and a standard
    deviation of 1.
    :param max_runs: the number of runs to iterate the process over
    :param full_return: enter true to return a list of all the SSE and silhouette scores as a function of number of
    clusters
    :return: a number which is identified as having the greatest reduction in SSE.
    """
    # Iterate over a range of values for num_clusters, obtaining the SSE (sum of squared error)
    cluster_model = KMeans(n_clusters=1, **kmeans_kwargs).fit(scaled_input)
    sse = [cluster_model.inertia_]
    silhouettes = []
    for value in range(2, max_runs):
        model_run = KMeans(n_clusters=value, **kmeans_kwargs).fit(scaled_input)
        sse.append(model_run.inertia_)
        score = silhouette_score(scaled_input, model_run.labels_)
        silhouettes.append(score)
    # This function finds the "elbow" point of the curve of SSE against cluster
    kl = KneeLocator(range(1, max_runs), sse, curve="convex", direction="decreasing")
    if full_return:
        return kl.elbow, sse, silhouettes
    else:
        return kl.elbow
