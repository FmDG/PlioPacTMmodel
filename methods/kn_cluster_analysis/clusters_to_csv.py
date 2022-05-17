import pandas as pd
from os import listdir
from os.path import join, isfile
from re import sub

latitude_data = pd.read_csv("data/cluster_data/site_info.csv")
latitude_data = latitude_data.set_index('Site')
latitude_dict = latitude_data.to_dict("index")


path = "../../data/cluster_data"
data_files = [f for f in listdir(path) if isfile(join(path, f))]

# Read the csv files
for entry in data_files:
    data_set = pd.read_csv(join(path, entry))
    latty = []
    longy = []
    for k, v in data_set.iterrows():
        latty.append(latitude_dict[v.Site]["latitude"])
        longy.append(latitude_dict[v.Site]["longitude"])
    data_set["latitude"] = latty
    data_set["longitude"] = longy
    data_set.to_csv(join(path, entry))


