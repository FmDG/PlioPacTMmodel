import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import os

os.chdir("../..")

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

def generate_single_cluster(period: str = time_periods[0], n_clusters: int = 3) -> None:

    # Load the datasets
    path_to_pliocene_data = "data/assessment.csv"
    pliocene = pd.read_csv(path_to_pliocene_data)

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
        pliocene.TimePeriod == period
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

    fig.suptitle(f'Cluster Analysis for {period}')
    sns.scatterplot(
        data=time_data,
        x="d18O",
        y="d13C",
        hue="predicted_cluster",
        palette="Set2",
        ax=ax,
    )

    for k, v in time_data[["d18O", "d13C", "Site"]].iterrows():
        ax.annotate(
            v[2],
            (v[0], v[1])
        )

    plt.show()


if __name__ == "__main__":
    generate_single_cluster(period="M2")