
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

# Parameters for KMeans function
kmeans_kwargs = {
        "init": "k-means++",
        "n_init": 50,
        "max_iter": 500,
        "random_state": None,
    }

axis_args = {
    "xlabel": r'$\delta^{18}$O',
    "ylabel": r'$\delta^{13}$C',
    "xlim": [1.5, 4.5],
    "ylim": [-1, 2]
}
