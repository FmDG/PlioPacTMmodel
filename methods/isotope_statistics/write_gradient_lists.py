from pandas import read_csv
from os import chdir
from json import dump

from statistics_functions import value_by_distance
from methods.general.general_functions import within_stddev

# Read the Modern Core Top Data
chdir("../..")
pacific_data = read_csv("data/core_tops/pacific_core_tops.csv")
s_atlantic_data = read_csv("data/core_tops/south_atlantic_core_tops.csv")
n_atlantic_data = read_csv("data/core_tops/north_atlantic_core_tops.csv")
indian_data = read_csv("data/core_tops/indian_core_tops.csv")
southern_data = read_csv("data/core_tops/southern_core_tops.csv")

# Drop the empty values
pacific_data = pacific_data.dropna(subset="d18O")
s_atlantic_data = s_atlantic_data.dropna(subset="d18O")
n_atlantic_data = n_atlantic_data.dropna(subset="d18O")
indian_data = indian_data.dropna(subset="d18O")
southern_data = southern_data.dropna(subset="d18O")

# pacific_data = within_stddev(dataset=pacific_data, parameter='d18O', num_devs=2)

# Calculate the difference in d18O value between every core top, and then divide this by the distance between them.
pacific_d18O_gradients = value_by_distance(dataset=pacific_data, value="d18O", full=False)
n_atlantic_d18O_gradients = value_by_distance(dataset=n_atlantic_data, value="d18O", full=False)
s_atlantic_d18O_gradients = value_by_distance(dataset=s_atlantic_data, value="d18O", full=False)
southern_d18O_gradients = value_by_distance(dataset=southern_data, value="d18O", full=False)
indian_d18O_gradients = value_by_distance(dataset=indian_data, value="d18O", full=False)


# Store these values in a JSON file to be used in the file read_gradient_lists.py
with open("data/permanent_lists/pacific_d18O_gradients.json", 'w') as f:
    dump(pacific_d18O_gradients, f, indent=2)

with open("data/permanent_lists/n_atlantic_d18O_gradients.json", 'w') as f:
    dump(n_atlantic_d18O_gradients, f, indent=2)

with open("data/permanent_lists/s_atlantic_d18O_gradients.json", 'w') as f:
    dump(s_atlantic_d18O_gradients, f, indent=2)

with open("data/permanent_lists/southern_d18O_gradients.json", 'w') as f:
    dump(southern_d18O_gradients, f, indent=2)

with open("data/permanent_lists/indian_d18O_gradients.json", 'w') as f:
    dump(indian_d18O_gradients, f, indent=2)

