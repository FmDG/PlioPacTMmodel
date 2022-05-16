import pandas as pd
import matplotlib.pyplot as plt

full_data = pd.read_csv("data/assessment.csv")
full_data = full_data.dropna(subset=["d18O", "d13C"])

time_periods = [["3500 ka - M2", 3500, 3320],
                ["M2", 3303, 3288],
                ["mPWP-1", 3280, 3155],
                ["KM2", 3148, 3120],
                ["mPWP-2", 3105, 3030],
                ["G20", 3025, 3000],
                ["G20 - 2800 ka", 2985, 2800],
                ["iNHG", 2800, 2700]]

for period in time_periods:
    _, ax = plt.subplots()
    ax.errorbar(data=full_data[full_data.TimePeriod == period[0]], x="d18O", y="d13C",
                xerr="std_d18O", yerr="std_d13C", fmt="+")
    ano_data = full_data[full_data.TimePeriod == period[0]]

    for k, v in ano_data[["d18O", "d13C", "Site"]].iterrows():
        ax.annotate(v[2], (v[0], v[1]))

    ax.set(xlim=[0, 5], ylim=[-1.5, 2.0], xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', title=period[0])
    plt.show()

