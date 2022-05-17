import pandas as pd
from kneed import KneeLocator
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib.lines import Line2D

modern = pd.read_csv("data/pacific_modern.csv")

def run_kmmodel(value, dataset):
    kmeans_kwargs = {
        "init": "k-means++",
        "n_init": 50,
        "max_iter": 500,
        "random_state": None,
    }
    run = KMeans(n_clusters=value, **kmeans_kwargs)
    run.fit(dataset)
    return run


def obtain_sse_silhouette(limit_value, scaled_features):
    sse_answers = [run_kmmodel(1, scaled_features).inertia_]
    silhouette_answers = []
    for value in range(2, limit_value):
        model_run = run_kmmodel(value, scaled_features)
        sse_answers.append(model_run.inertia_)
        score = silhouette_score(scaled_features, model_run.labels_)
        silhouette_answers.append(score)
    return sse_answers, silhouette_answers


# Remove values that are more than 3 standard deviations away from the mean
modern = modern[modern.d18O > (modern.d18O.mean() - (3 * modern.d18O.std()))]
modern = modern[modern.d13C > (modern.d13C.mean() - (3 * modern.d13C.std()))]
modern = modern[modern.d18O < (modern.d18O.mean() + (3 * modern.d18O.std()))]
modern = modern[modern.d13C < (modern.d13C.mean() + (3 * modern.d13C.std()))]

isotope_data = modern[["d18O", "d13C"]].to_numpy()
# Scale the features to sit with a mean of 0 and a std. dev of 1
scaler = StandardScaler()
isotope_data = scaler.fit_transform(isotope_data)

# Iterate over a range of values for k, obtaining the SSE (sum of squared error)
upper_limit = 8
sse, silhouette_coefficients = obtain_sse_silhouette(upper_limit, isotope_data)

# This function finds the "elbow" point of the curve of SSE against cluster
kl = KneeLocator(range(1, upper_limit), sse, curve="convex", direction="decreasing")

# Plot the predicted clusters
ideal_k = kl.elbow
final_prediction = run_kmmodel(ideal_k, isotope_data)

predicted_data = pd.DataFrame(
    isotope_data, columns=["scaled_d18O", "scaled_d13C"]
)
predicted_data["predicted_cluster"] = final_prediction.labels_

fig, ax = plt.subplots()
fig.suptitle("Modern Data")
modern["predicted_cluster"] = final_prediction.labels_

sns.scatterplot(data=modern, x="d18O", y="d13C", hue="predicted_cluster", ax=ax)
ax.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[1, 5], ylim=[-1, 2.5])

fig, axs = plt.subplots(2, 2)
# Add the title of the relevant time period
fig.suptitle("Modern")

sns.scatterplot(data=predicted_data, x="scaled_d18O", y="scaled_d13C", hue="predicted_cluster", ax=axs[0, 0])
axs[0, 0].set(title="Clustered Data")
axs[0, 1].scatter(modern.d18O, modern.d13C)
axs[0, 1].set(title="Raw Data", xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[1, 5], ylim=[-1, 2.5])

axs[1, 0].plot(range(2, upper_limit), silhouette_coefficients)
axs[1, 0].set(xlabel="Number of Clusters", ylabel="Silhouette Coeff.")

axs[1, 1].plot(range(1, upper_limit), sse)
axs[1, 1].set(xlabel="Number of Clusters", ylabel="SSE")


# Drop any empty features
fig, ax = plt.subplots()
fog, ix = plt.subplots()

fig.suptitle("Modern Data")
fog.suptitle("Modern Data")
modern = modern.dropna(subset=['d18O', 'd13C'])

# k means
kmeans = KMeans(n_clusters=3)

# Predict the clusters based on this result
modern['cluster'] = kmeans.fit_predict(modern[['d18O', 'd13C']])

# Get the centroids
centroids = kmeans.cluster_centers_
cen_d18O = [i[0] for i in centroids]
cen_d13C = [i[1] for i in centroids]

# Add to dataframe (repeated for each of the three clusters)
modern['cen_x'] = modern.cluster.map({0: cen_d18O[0], 1: cen_d18O[1], 2: cen_d18O[2]})
modern['cen_y'] = modern.cluster.map({0: cen_d13C[0], 1: cen_d13C[1], 2: cen_d13C[2]})

# Define and map colours
colors = ['#DF2020', '#81DF20', '#2095DF']
# Add the colour map to the dataframe
modern['c'] = modern.cluster.map({0: colors[0], 1: colors[1], 2: colors[2]})

# Plot the dataset, coloured according to above colourmap
ax.scatter(modern.d18O, modern.d13C, c=modern.c, alpha=0.6, s=20, marker='+')
# Plot the dataset, coloured according to above colourmap
ix.scatter(modern.d18O, modern.d13C, alpha=0.6, s=20, marker='+')

# Plot the centroids of the clusters
ax.scatter(cen_d18O, cen_d13C, marker='o', c=colors, s=50)

# Plot lines from centroids to data points
for idx, val in modern.iterrows():
    # x (below) is a line from the value to the centroid
    x = [val.d18O, val.cen_x]
    y = [val.d13C, val.cen_y]
    # Plot both the lines
    ax.plot(x, y, c=val.c, alpha=0.2)

# legend
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Cluster {}'.format(i+1),
                   markerfacecolor=mcolor, markersize=5) for i, mcolor in enumerate(colors)]
legend_elements.extend([Line2D([0], [0], marker='^', color='w', label='Centroid - C{}'.format(i+1),
                        markerfacecolor=mcolor, markersize=10) for i, mcolor in enumerate(colors)])

ax.legend(handles=legend_elements, loc='upper right', ncol=2)

ax.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[0.5, 6.0], ylim=[-1, 2.5])
ix.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[0.5, 6.0], ylim=[-1, 2.5])

# modern.to_csv("data/modern_clusters.csv")

plt.show()

