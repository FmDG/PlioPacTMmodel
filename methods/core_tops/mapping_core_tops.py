import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
from methods.general.general_functions import within_stddev
from os import chdir

# Read the Pacific Modern Core Top Data
chdir("../..")

core_tops = pd.read_csv("data/schmittner_2017.csv")
core_tops = core_tops.dropna(subset=["d18O", "d13C"])

core_tops = within_stddev(
    dataset=within_stddev(
        dataset=core_tops,
        parameter="d13C",
        num_devs=3
    ),
    parameter="d18O",
    num_devs=3
)

coastline_shp_path = "data/coastlines/ne_10m_coastline.shp"
# Reading the shape file by using reader function of the shape lib
coastline_sf = shp.Reader(coastline_shp_path)

fig, ax = plt.subplots(figsize=(15, 8))

for shape in coastline_sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    ax.plot(x, y, 'k-', linewidth=0.5)
    ax.set(xlim=[-180, 180], ylim=[-90, 90])

sns.scatterplot(
    data=core_tops,
    x="longitude",
    y="latitude",
    hue="d18O",
    palette="viridis",
    ax=ax,
    marker='o'
)

plt.show()

