from pandas import read_csv
from os import chdir
import json

from methods.general.general_functions import within_stddev
from statistics_functions import value_by_distance

# Read the Pacific Modern Core Top Data
chdir("../..")
pacific = read_csv('data/pacific_modern.csv')
southern = read_csv('data/southern_core_tops.csv')
atlantic = read_csv('data/atlantic_core_tops.csv')

# Remove values that are more than 3 standard deviations away from the mean
# pacific = within_stddev(within_stddev(pacific, "d18O", num_devs=3), "d13C", num_devs=3)

# Repeat for Southern and Atlantic Ocean Core Top data
# southern = within_stddev(within_stddev(southern, "d18O", num_devs=3), "d13C", num_devs=3)
# atlantic = within_stddev(within_stddev(atlantic, "d18O", num_devs=3), "d13C", num_devs=3)

# Calculate the difference in d18O value between every core top, and then divide this by the distance between them.
pacific_d18O_by_distance = value_by_distance(
    dataset=pacific,
    value="d18O"
)

southern_d18O_by_distance = value_by_distance(
    dataset=southern,
    value='d18O'
)

atlantic_d18O_by_distance = value_by_distance(
    dataset=atlantic,
    value='d18O'
)

# Store these values in a JSON file to be used in the file read_distance_lists.py
with open("data/permanent_lists/pacific_core_distances.json", 'w') as f:
    json.dump(pacific_d18O_by_distance, f, indent=2)

with open("data/permanent_lists/southern_core_distances.json", 'w') as f:
    json.dump(southern_d18O_by_distance, f, indent=2)

with open("data/permanent_lists/atlantic_core_distances.json", 'w') as f:
    json.dump(atlantic_d18O_by_distance, f, indent=2)
