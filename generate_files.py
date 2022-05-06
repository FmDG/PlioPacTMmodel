import pandas as pd
from os import listdir
from os.path import join, isfile
from re import sub


def clean_names(init_name):
    mid_name = sub('.+_', '', init_name)
    final_name = mid_name.strip(".csv")
    return final_name


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
        data_files = [f for f in listdir(path) if isfile(join(path, f))]

    # Read the csv files into a list
    isotope_values = []
    for entry in data_files:
        data_set = pd.read_csv(join(path, entry))
        name = clean_names(entry)
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


def generate_means(path, periods, from_csv=True):
    """
    This function will generate a SQL database to house all the means of the d18O and d13C values for the different
    datasets between the time periods specified in the period parameter. The final database is written to an SQL
    database which is stored in the path specified in final_path

    :param path: Path from where the files will  be found
    :param periods: Definition of the periods which the model will run on, in the format of a list of lists with the
    first item being the name of the time period, the second the start date (in ka) and the third item the end date.
    :param from_csv: A boolean that defines whether you want to only read CSV files from the folder or all the files.
    """

    # Selects the files in the path folder
    if from_csv:
        data_files = [f for f in listdir(path) if (".csv" in f)]
    else:
        data_files = [f for f in listdir(path) if isfile(join(path, f))]

    # Read the csv files into a list
    isotope_values = []
    for entry in data_files:
        data_set = pd.read_csv(join(path, entry))
        name = clean_names(entry)
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

    return isotope_space


def generate_full_data(path):
    data_files = [f for f in listdir(path) if (".csv" in f)]

    full_values = pd.DataFrame(columns=['Site', 'age_ka', 'd18o', "d13C"])

    for file_name in data_files:
        data_set = pd.read_csv(join(path, file_name))
        name = clean_names(file_name)
        data_set["Site"] = name
        full_values = pd.concat([full_values, data_set], join="inner")

    return full_values
