"""
This file takes the files contained within the data folder (currently in gitignore due to data not being publicly
accessible) and compiles them into one dataframe which is then stored in SQL database.

"""

import pandas as pd
from os import listdir
from os.path import join  # isfile - to be used if required (see line 14)
import sqlite3

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

# Open a connection to the SQL database
connector = sqlite3.connect("data/prism_data.db")


# Generates the table in the new database
c = connector.cursor()
c.execute("CREATE TABLE IF NOT EXISTS isotopes (Depth number)")
connector.commit()

# Writes the new dataframes to the database
isotope_space.to_sql('isotopes', connector, if_exists='replace')
connector.commit()

# Closes the connection to the SQL database
connector.close()

