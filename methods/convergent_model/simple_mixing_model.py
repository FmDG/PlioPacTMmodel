import matplotlib.pyplot as plt
import seaborn as sns
from pandas import read_csv
from os import chdir

from model_functions import simple_mixing_model

chdir("../..")
site_data = read_csv("data/prism_data.csv")

section_name = "G20 - 2800 ka"

subsection = site_data[site_data.TimePeriod == section_name]
subsection = subsection.dropna()

sites_list = ["odp1018", "odp1148", "odp1014", "odp1125", "odp1208", "odp1239", "dsdp594", "odp1143", "odp1241",
              "odp806", "odp849", "dsdp593"]


for site in sites_list:
    scw = subsection[subsection.Site == site]
    simple_model = simple_mixing_model(d18o=float(scw.d18O), d13c=float(scw.d13C), input_frame=subsection)

    fig, ax = plt.subplots()
    fig.suptitle(site)
    sns.kdeplot(data=simple_model, x="NCW_d18O", y="NCW_d13C", ax=ax)
    ax.scatter(float(scw.d18O), float(scw.d13C), marker="+", color="g")
    print("Completed Site: {}".format(site))
plt.show()
