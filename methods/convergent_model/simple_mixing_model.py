from os import chdir

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import read_csv

from model_functions import simple_mixing_model


def binary_mixing_model() -> None:
    """
    This function runs through all the PRISM data for the various time slices in the Pliocene. For each averaged value
    of d18O and d13C it assumes that this is the Southern Sourced Water (SCW) endmember. It goes through all the other
    sites' d18O and d13C values and tries to work out what the Northern Sourced Water (NCW) endmember would be if each
    site had between 30 - 70% SCW%. If all the values for NCW composition converge at some point then one can assume
    that this is a likely NCW endmember and that the site is a likely SCW endmember.
    """

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
        ax.scatter(subsection.d18O, subsection.d13C, marker="+", color="b")

    plt.show()


if __name__ == "__main__":
    binary_mixing_model()