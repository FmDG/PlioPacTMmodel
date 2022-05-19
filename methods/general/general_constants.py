
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
    ["3500 ka - M2", 3500, 3320],
    ["M2", 3303, 3288],
    ["mPWP-1", 3280, 3155],
    ["KM2", 3148, 3120],
    ["mPWP-2", 3105, 3030],
    ["G20", 3025, 3000],
    ["G20 - 2800 ka", 2985, 2800],
    ["iNHG", 2800, 2700]
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
    "xlim": [0.5, 5.5],
    "ylim": [-2, 3]
}

# These are time intervals from a variety of sources covering larger areas than the van der Weijst section
time_sets = [
    ["iNHG", 2750, 2400],
    ["mPWP", 3300, 3000],
    ["Mid-Pliocene", 4000, 3300],
    ["Early Pleistocene", 2400, 1500]
]
