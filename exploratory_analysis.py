"""
Exploring the data that exists within the PRISM data directory

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
from os.path import join  # isfile - to be used if required (see line 14)

# Enter the path to the datasets
path_to_data = "data"

# Enter the Time Periods we're investigating in the format ["Name", Start, End]. These time periods are derived from the
# van der Weijst et al., 2020 paper.
time_periods = [["3500 ka - M2", 3500, 3320],
                ["M2", 3303, 3288],
                ["mPWP-1", 3280, 3155],
                ["KM2", 3148, 3120],
                ["mPWP-2", 3105, 3030],
                ["G20", 3025, 3000],
                ["G20 - 2800 ka", 2985, 2800]]

# Selects only ".csv" files in the target folder - use `isfile(join(path_to_data, f))` if selecting all files in folder.
data_files = [f for f in listdir(path_to_data) if (".csv" in f)]

# Read the csv files into a list
isotope_values = []
for entry in data_files:
    data_set = pd.read_csv(join(path_to_data, entry))
    name = entry.strip(".csv")
    for period in time_periods:
        # Select the slice which lies within the time period
        section = data_set[data_set.age_ka.between(period[2], period[1])]
        mean_d18O = section.d18o.mean()
        mean_d13C = section.d13C.mean()
        isotope_values.append([name, period[0], mean_d18O, mean_d13C])

# Create a pandas DataFrame to store the dataset
isotope_space = pd.DataFrame(isotope_values, columns=['Site', 'TimePeriod', 'd18O', "d13C"])

# Iterate over all the time periods and plot the results in carbon and oxygen isotope space
sns.relplot(data=isotope_space, x='d18O', y='d13C', col="TimePeriod", col_wrap=3, hue="Site")

plt.show()
