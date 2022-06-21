from os import listdir, chdir
from os.path import join, isfile

import pandas as pd

chdir("../..")

latitude_data = pd.read_csv("data/cluster_data/site_info.csv")
latitude_data = latitude_data.set_index('Site')
latitude_dict = latitude_data.to_dict("index")


path = "data/cluster_data"
data_files = [f for f in listdir(path) if isfile(join(path, f))]

# Read the csv files
for entry in data_files:
    data_set = pd.read_csv(join(path, entry))
    latty = []
    longy = []
    for _, value in data_set.iterrows():
        latty.append(latitude_dict[value.Site]["latitude"])
        longy.append(latitude_dict[value.Site]["longitude"])
    data_set["latitude"] = latty
    data_set["longitude"] = longy
    data_set.to_csv(join(path, entry))


