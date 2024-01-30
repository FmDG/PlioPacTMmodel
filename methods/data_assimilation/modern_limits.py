import os

import pandas as pd
from spatial_geometry import enclosing_points
import matplotlib.pyplot as plt

# Change to the correct database
os.chdir("../..")

# Load the required data
full_data = pd.read_csv("data/modern_oceans.csv")

full_data = full_data.dropna(subset=["d13C", "d18O"])

# Extract data from column1 and column2 into separate lists
d13C = full_data['d13C'].tolist()
d18O = full_data['d18O'].tolist()

extent = enclosing_points(d13C, d18O)

# Extract x and y coordinates from the list of lists
x_trig, y_trig = zip(*extent)

# Append the first vertex at the end to close the polygon
x_trig += (x_trig[0],)
y_trig += (y_trig[0],)

fig, ax = plt.subplots()

# Plot the d13C and d18O space
ax.scatter(d13C, d18O, marker="+")

# Create a scatterplot with a polygon
ax.plot(x_trig, y_trig, linestyle='-', color='red', label="Minimum Enclosing Area")
ax.set(ylabel="d18O", xlabel="d13C", title="Modern Stable Isotope Distribution (Pacific Ocean)")

plt.show()
