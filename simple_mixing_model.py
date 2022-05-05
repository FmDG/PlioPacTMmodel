import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

site_data = pd.read_csv("data/prism_data.csv")

section_name = "G20 - 2800 ka"

subsection = site_data[site_data.TimePeriod == section_name]
subsection = subsection.dropna()

site_names = ["h1_odp1018", "h6_odp1148", "h3_odp1014", "h15_odp1125", "h2_odp1208", "h12_odp1239", "h16_dsdp594",
             "h7_odp1143", "h8_odp1241", "h9_odp806", "h10_odp849", "mp1_odp1123", "h14_dsdp593", "h13_odp846",
              "odp1123"]

# Let us declare Site 849 one end-member
scw = subsection[subsection.Site == "h10_odp849"]
scw_d18o = float(scw.d18O)
scw_d13c = float(scw.d13C)


def bmm_solver(x_0, x_1, x_2, y_0, y_1, y_2):
    """
    If we know the end-member d13C and d18O values, then for a given site d18O and d13C we can generate two different
    proportions of NCW:SCW that fit the equations.
    :param x_0: Site d18O
    :param x_1: NCW d18O
    :param x_2: SCW d18O
    :param y_0: Site d13C
    :param y_1: NCW d13C
    :param y_2: SCW d13C
    :return: p_1 and p_2 are the possible proportions of NCW:SCW
    """
    p_1 = (x_0 - x_2)/(x_1 - x_2)
    p_2 = (y_0 - y_2)/(y_1 - y_2)
    return p_1, p_2


def end_member_solver(x_0, x_2, y_0, y_2, p):
    """
    If we have the proportion of NCW:SCW and the composition of one endmember and the site composition we can work out
    the composition of the other end-member
    :param x_0: Site d18O
    :param x_2: SCW d18O
    :param y_0: Site d13C
    :param y_2: SCW d13C
    :param p: Proportion of NCW:SCW
    :return: x_1: NCW d18O
             y_1: NCW d13C
    """
    x_1 = (x_0 + ((p-1) * x_2))/p
    y_1 = (y_0 + ((p-1) * y_2))/p
    return [x_1, y_1]


answers = []
for row in subsection.itertuples(index=False):
    prop_array = np.arange(start=0.50, stop=0.99, step=0.01)
    for p in prop_array:
        ncw = end_member_solver(row.d18O, scw_d18o, row.d13C, scw_d13c, p)
        answers.append([row.Site, ncw[0], ncw[1], p])


answer_array = pd.DataFrame(answers, columns=["Site", "NCW_d18O", "NCW_d13C", "NCW:SCW"])

fig, ax = plt.subplots()
sns.scatterplot(data=answer_array, x="NCW_d18O", y="NCW_d13C", hue="NCW:SCW", ax=ax)
ax.scatter(scw_d18o, scw_d13c, marker="+", color="g", linewidths=5)

sns.jointplot(data=answer_array, x="NCW_d18O", y="NCW_d13C", kind="kde")
plt.show()
