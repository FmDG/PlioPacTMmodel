import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

path_to_pliocene_data = "data/assessment.csv"
path_to_modern_data = "data/pacific_modern.csv"


# Load the datasets
pliocene = pd.read_csv(path_to_pliocene_data)
modern = pd.read_csv(path_to_modern_data)

# List of Sites Used
sites_list = [
    "odp1018",
    "odp1148",
    "odp1014",
    "odp1125",
    "odp1208",
    "odp1239",
    "dsdp594",
    "odp1143",
    "odp1241",
    "odp806",
    "odp849",
    "dsdp593"
]

# List of time periods
time_periods = [
    "3500 ka - M2",
    "M2",
    "mPWP-1",
    "KM2",
    "mPWP-2",
    "G20",
    "G20 - 2800 ka",
    "iNHG"
]

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
time_data = pliocene[
    pliocene.TimePeriod == time_periods[t_0]
]

# Drop any empty features
time_data = time_data.dropna()
# Convert to a numpy array
features = time_data[["d18O", "d13C"]].to_numpy()

# Fit the KMeans model to the data
combi_pipe.fit(features)

# Add the results to a dataframe
time_data["predicted_cluster"] = combi_pipe["cluster"]["kmeans"].labels_

# --- PLOTTING REGIME ---
fig, ax = plt.subplots()
# Add the title of the relevant time period

fig.suptitle(time_periods[t_0])

sns.scatterplot(
    data=time_data,
    x="d18O",
    y="d13C",
    hue="predicted_cluster",
    ax=ax
)

for k, v in time_data[["d18O", "d13C", "Site"]].iterrows():
    ax.annotate(
        v[2],
        (v[0], v[1])
    )

plt.show()

# --- PERFORMANCE RESULTS ---