from pandas import read_csv, concat
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy
from math import sqrt

pacific = read_csv('data/pacific_modern.csv')
limit = pacific.distance.mean() + pacific.distance.std()
pacific = pacific[pacific.distance < limit]


sns.scatterplot(data=pacific, x="d18O", y="d13C")

plt.show()
