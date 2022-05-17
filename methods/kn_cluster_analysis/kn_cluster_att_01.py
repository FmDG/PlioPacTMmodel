import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import numpy

# Load the dataset
pliocene = pd.read_csv("data/assessment.csv")

# List of Sites Used
sites_list = ["odp1018", "odp1148", "odp1014", "odp1125", "odp1208", "odp1239", "dsdp594", "odp1143", "odp1241",
              "odp806", "odp849", "dsdp593"]
# List of time period
time_periods = ["3500 ka - M2", "M2", "mPWP-1", "KM2", "mPWP-2", "G20", "G20 - 2800 ka", "iNHG"]
t_0 = 0

# Number of clusters in the final model
n_clusters = 4

# Preprocessing of the data to scale it (the KM algorithm can't handle unscaled data)
preprocessor = Pipeline(
    [
        ("scaler", StandardScaler()),
    ]
)

# Clustering the data using a KMeans pipeline, the number of cluster is set above
cluster = Pipeline(
   [
       (
           "kmeans",
           KMeans(
               n_clusters=n_clusters,
               init="k-means++",
               n_init=50,
               max_iter=500,
               random_state=None,
           ),
       ),
   ]
)

# Put the preprocessing and the clustering together
combi_pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("cluster", cluster)
    ]
)

# Select the data which fits the time period selected
time_data = pliocene[pliocene.TimePeriod == time_periods[t_0]]
# Drop any empty features
time_data = time_data.dropna()
# Convert to a numpy array
features = time_data[["d18O", "d13C"]].to_numpy()

# Fit the KMeans model to the data
combi_pipe.fit(features)

# Combine the results in a dataframe
predicted_data = pd.DataFrame(
    combi_pipe["preprocessor"].transform(features),
    columns=["scaled_d18O", "scaled_d13C"],
)

predicted_data["predicted_cluster"] = combi_pipe["cluster"]["kmeans"].labels_

# --- PLOTTING REGIME ---
fig, axs = plt.subplots(1, 2)
# Add the title of the relevant time period
fig.suptitle(time_periods[t_0])

sns.scatterplot(data=predicted_data, x="scaled_d18O", y="scaled_d13C", hue="predicted_cluster", ax=axs[0])
axs[1].scatter(time_data.d18O, time_data.d13C)
for k, v in time_data[["d18O", "d13C", "Site"]].iterrows():
    axs[1].annotate(v[2], (v[0], v[1]))
plt.show()

# --- PERFORMANCE RESULTS ---
