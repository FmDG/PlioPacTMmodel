import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

assessment_data = pd.read_csv("data/assessment.csv")
full_data = pd.read_csv("data/full_dataset.csv")

full_data = full_data.dropna(subset=["d18o", "d13C"])

full_data = full_data[full_data.age_ka.between(2200, 3600)]

data_1208 = full_data[full_data.Site == "odp1208"]
data_1209 = full_data[full_data.Site == "odp1209"]
data_1210 = full_data[full_data.Site == "odp1210"]

time_periods = [["3500 ka - M2", 3500, 3320],
                ["M2", 3303, 3288],
                ["mPWP-1", 3280, 3155],
                ["KM2", 3148, 3120],
                ["mPWP-2", 3105, 3030],
                ["G20", 3025, 3000],
                ["G20 - 2800 ka", 2985, 2800],
                ["iNHG", 2800, 2700]]


fig, axs = plt.subplots(2)


axs[0].plot(data_1210.age_ka, data_1210.d18o, label="1210", marker='+')
axs[0].plot(data_1208.age_ka, data_1208.d18o, label="1208", marker='+')
axs[0].plot(data_1209.age_ka, data_1209.d18o, label="1209", marker='+')
axs[0].invert_yaxis()

axs[1].plot(data_1210.age_ka, data_1210.d13C, label="1210", marker='+')
axs[1].plot(data_1208.age_ka, data_1208.d13C, label="1208", marker='+')
axs[1].plot(data_1209.age_ka, data_1209.d13C, label="1209", marker='+')

axs[0].legend()

plt.show()

'''for period in time_periods:
    _, ax = plt.subplots()
    ax.errorbar(data=assessment_data[assessment_data.TimePeriod == period[0]], x="d18O", y="d13C",
                xerr="std_d18O", yerr="std_d13C", fmt="+")
    ano_data = assessment_data[assessment_data.TimePeriod == period[0]]

    for k, v in ano_data[["d18O", "d13C", "Site"]].iterrows():
        ax.annotate(v[2], (v[0], v[1]))

    ax.set(xlim=[0, 5], ylim=[-1.5, 2.0], xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', title=period[0])
    plt.show()'''

