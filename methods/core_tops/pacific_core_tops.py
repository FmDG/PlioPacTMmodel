from os import chdir

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from methods.general.general_functions import within_stddev

# Read the Pacific Modern Core Top Data
chdir("../..")

pacific_core_tops = pd.read_csv("data/pacific_modern.csv")
pacific_core_tops = pacific_core_tops.dropna(subset=["d18O"])

_, ux = plt.subplots()

pacific_core_tops = within_stddev(dataset=pacific_core_tops, parameter="d18O", num_devs=3)

pacific_core_tops = pacific_core_tops[pacific_core_tops.depth > 1000]

sns.scatterplot(
    data=pacific_core_tops,
    x="latitude",
    y="depth",
    hue="d18O",
    palette="husl",
    ax=ux,
    marker='o'
)

ux.set(title="Pacific")
ux.invert_yaxis()

plt.show()


