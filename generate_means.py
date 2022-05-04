"""
This file takes the files contained within the data folder (currently in gitignore due to data not being publicly
accessible) and compiles them into one dataframe which is then stored in SQL database.

"""

import pandas as pd
from os import listdir
from os.path import join, isfile
import sqlite3


def assess_means(path, periods, from_csv=True):
    """
    This function assess whether it is worth finding the means of the d13C and d18O value for a particular time interval
     for a certain site.

    :param path: Path from where the files will  be found
    :param periods: Definition of the periods which the model will run on, in the format of a list of lists with the
    first item being the name of the time period, the second the start date (in ka) and the third item the end date.
    :param from_csv: A boolean that defines whether you want to only read CSV files from the folder or all the files.
    """

    # Selects the files in the path folder
    if from_csv:
        data_files = [f for f in listdir(path) if (".csv" in f)]
    else:
        data_files = [f for f in listdir(path) if isfile(join(path_to_data, f))]

    # Read the csv files into a list
    isotope_values = []
    for entry in data_files:
        data_set = pd.read_csv(join(path_to_data, entry))
        name = entry.strip(".csv")
        for period in periods:
            # Select the slice which lies within the time period
            section = data_set[data_set.age_ka.between(period[2], period[1])]
            mean_d18o = section.d18o.mean()
            std_d18o = section.d18o.std()
            num_d18o = section.d18o.count()
            mean_d13c = section.d13C.mean()
            std_d13c = section.d13C.std()
            num_d13c = section.d13C.count()
            isotope_values.append([name, period[0], mean_d18o, std_d18o, num_d18o, mean_d13c, std_d13c, num_d13c])

    # Create a pandas DataFrame to store the dataset
    isotope_space = pd.DataFrame(isotope_values, columns=['Site', 'TimePeriod', 'd18O', "std_d18O", "num_d18O",
                                                          "d13C", "std_d13C", "num_d13C"])
    return isotope_space


def generate_means(path, periods, final_path, from_csv=True):
    """
    This function will generate a SQL database to house all the means of the d18O and d13C values for the different
    datasets between the time periods specified in the period parameter. The final database is written to an SQL
    database which is stored in the path specified in final_path

    :param path: Path from where the files will  be found
    :param periods: Definition of the periods which the model will run on, in the format of a list of lists with the
    first item being the name of the time period, the second the start date (in ka) and the third item the end date.
    :param final_path: The final path where the database will be stored.
    :param from_csv: A boolean that defines whether you want to only read CSV files from the folder or all the files.
    """

    # Selects the files in the path folder
    if from_csv:
        data_files = [f for f in listdir(path) if (".csv" in f)]
    else:
        data_files = [f for f in listdir(path) if isfile(join(path_to_data, f))]

    # Read the csv files into a list
    isotope_values = []
    for entry in data_files:
        data_set = pd.read_csv(join(path_to_data, entry))
        name = entry.strip(".csv")
        for period in periods:
            # Select the slice which lies within the time period
            section = data_set[data_set.age_ka.between(period[2], period[1])]
            if section.d18o.count() < 5:
                mean_d18o = None
            else:
                mean_d18o = section.d18o.mean()
            if section.d13C.count() < 5:
                mean_d13c = None
            else:
                mean_d13c = section.d13C.mean()
            isotope_values.append([name, period[0], mean_d18o, mean_d13c])

    # Create a pandas DataFrame to store the dataset
    isotope_space = pd.DataFrame(isotope_values, columns=['Site', 'TimePeriod', 'd18O', "d13C"])

    # Open a connection to the SQL database
    connector = sqlite3.connect(final_path)

    # Generates the table in the new database
    c = connector.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS isotopes (Depth number)")
    connector.commit()

    # Writes the new dataframes to the database
    isotope_space.to_sql('isotopes', connector, if_exists='replace')
    connector.commit()

    # Closes the connection to the SQL database
    connector.close()


# Enter the path to the datasets
path_to_data = "data/PRISM_Pacific_data"

# Enter the Time Periods we're investigating in the format ["Name", Start, End]. These time periods are derived from the
# van der Weijst et al., 2020 paper.
time_periods = [["3500 ka - M2", 3500, 3320],
                ["M2", 3303, 3288],
                ["mPWP-1", 3280, 3155],
                ["KM2", 3148, 3120],
                ["mPWP-2", 3105, 3030],
                ["G20", 3025, 3000],
                ["G20 - 2800 ka", 2985, 2800],
                ["iNHG", 2800, 2700]]

database_path = "data/prism_data.db"

generate_means(path_to_data, time_periods, database_path)

# This assessment looks at the standard deviations and the number of samples being averaged in each case to make
# sure that this is a reliable data source.
assessment = assess_means(path_to_data, time_periods)
