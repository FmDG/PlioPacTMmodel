from pandas import read_csv
from os import chdir
from json import dump

from statistics_functions import value_by_distance
from methods.general.general_functions import within_stddev

# Read the Modern Core Top Data
chdir("../..")
early_pleistocene_data = read_csv("data/cluster_data/Early Pleistocene.csv")
inhg_data = read_csv("data/cluster_data/iNHG.csv")
mid_pleistocene_data = read_csv("data/cluster_data/Mid-Pliocene.csv")
mpwp_data = read_csv("data/cluster_data/mPWP.csv")

# Drop the empty values
early_pleistocene_data = early_pleistocene_data.dropna(subset="d18O")
inhg_data = inhg_data.dropna(subset="d18O")
mid_pleistocene_data = mid_pleistocene_data.dropna(subset="d18O")
mpwp_data = mpwp_data.dropna(subset="d18O")

# pacific_data = within_stddev(dataset=pacific_data, parameter='d18O', num_devs=2)

# Calculate the difference in d18O value between every core top, and then divide this by the distance between them.
EP_d18O_gradients = value_by_distance(dataset=early_pleistocene_data, value="d18O", full=False, core_name="Site")
NHG_d18O_gradients = value_by_distance(dataset=inhg_data, value="d18O", full=False, core_name="Site")
MP_d18O_gradients = value_by_distance(dataset=mid_pleistocene_data, value="d18O", full=False, core_name="Site")
MPWP_d18O_gradients = value_by_distance(dataset=mpwp_data, value="d18O", full=False, core_name="Site")


# Store these values in a JSON file to be used in the file read_gradient_lists.py
with open("data/permanent_lists/early_pleistocene_d18O_gradients.json", 'w') as f:
    dump(EP_d18O_gradients, f, indent=2)

with open("data/permanent_lists/inhg_d18O_gradients.json", 'w') as f:
    dump(NHG_d18O_gradients, f, indent=2)

with open("data/permanent_lists/mid_pleistocene_d18O_gradients.json", 'w') as f:
    dump(MP_d18O_gradients, f, indent=2)

with open("data/permanent_lists/mpwp_d18O_gradients.json", 'w') as f:
    dump(MPWP_d18O_gradients, f, indent=2)

