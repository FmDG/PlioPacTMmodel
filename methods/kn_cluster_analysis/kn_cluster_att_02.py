import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Load the dataset
pliocene = pd.read_csv("data/assessment.csv")

# List of Sites Used
sites_list = ["odp1018", "odp1148", "odp1014", "odp1125", "odp1208", "odp1239", "dsdp594", "odp1143", "odp1241",
              "odp806", "odp849", "dsdp593"]

# List of time period
time_periods = ["3500 ka - M2", "M2", "mPWP-1", "KM2", "mPWP-2", "G20", "G20 - 2800 ka", "iNHG"]


def scale_data(dataset):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(dataset)
    return scaled_features


def select_time_data(name, dataset):
    # Select the data which fits the time period selected
    selected = dataset[dataset.TimePeriod == name]
    # Drop any empty features
    selected = selected.dropna()
    # Convert to a numpy array
    isotope_data = selected[["d18O", "d13C"]].to_numpy()
    # Scale the features to sit with a mean of 0 and a std. dev of 1
    isotope_data = scale_data(isotope_data)
    return isotope_data, selected


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


def plot_clusters(name, dataset, full_analysis=False, show=False):
    # Select the relevant time period and scale the data
    features, time_data = select_time_data(name, dataset)

    # Iterate over a range of values for k, obtaining the SSE (sum of squared error)
    upper_limit = 8
    sse, silhouette_coefficients = obtain_sse_silhouette(upper_limit, features)

    # This function finds the "elbow" point of the curve of SSE against cluster
    kl = KneeLocator(range(1, upper_limit), sse, curve="convex", direction="decreasing")

    # Plot the predicted clusters
    ideal_k = kl.elbow
    final_prediction = run_kmmodel(ideal_k, features)

    predicted_data = pd.DataFrame(
        features, columns=["scaled_d18O", "scaled_d13C"]
    )
    predicted_data["predicted_cluster"] = final_prediction.labels_

    fig, ax = plt.subplots()
    fig.suptitle("{}".format(name))
    time_data["predicted_cluster"] = final_prediction.labels_
    sns.scatterplot(data=time_data, x="d18O", y="d13C", hue="predicted_cluster", ax=ax)
    ax.set(xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', xlim=[1.5, 4.5], ylim=[-1, 1.5])
    for k, v in time_data[["d18O", "d13C", "Site"]].iterrows():
        ax.annotate(v[2], (v[0], v[1]), fontsize="xx-small")

    if full_analysis:
        fig, axs = plt.subplots(2, 2)
        # Add the title of the relevant time period
        fig.suptitle(name)

        sns.scatterplot(data=predicted_data, x="scaled_d18O", y="scaled_d13C", hue="predicted_cluster", ax=axs[0, 0])
        axs[0, 0].set(title="Clustered Data")
        axs[0, 1].scatter(time_data.d18O, time_data.d13C)
        for k, v in time_data[["d18O", "d13C", "Site"]].iterrows():
            axs[0, 1].annotate(v[2], (v[0], v[1]))
        axs[0, 1].set(title="Raw Data", xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C')

        axs[1, 0].plot(range(2, upper_limit), silhouette_coefficients)
        axs[1, 0].set(xlabel="Number of Clusters", ylabel="Silhouette Coeff.")

        axs[1, 1].plot(range(1, upper_limit), sse)
        axs[1, 1].set(xlabel="Number of Clusters", ylabel="SSE")

        if show:
            plt.show()


for period in time_periods:
    plot_clusters(period, pliocene, full_analysis=False)


plt.show()
