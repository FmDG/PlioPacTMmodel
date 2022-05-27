from pandas import read_csv
from os import chdir
from json import dump

from statistics_functions import value_by_distance
from methods.general.general_functions import within_stddev

# Read the Pacific Modern Core Top Data
chdir("../..")
pacific = read_csv('data/pacific_modern.csv')
southern = read_csv('data/southern_core_tops.csv')
atlantic = read_csv('data/atlantic_core_tops.csv')

# Remove all empty values
pacific = pacific.dropna(subset="d18O")
southern = southern.dropna(subset="d18O")
atlantic = atlantic.dropna(subset="d18O")

pacific = within_stddev(
    dataset=pacific,
    parameter='d18O',
    num_devs=2
)

southern = within_stddev(
    dataset=southern,
    parameter='d18O',
    num_devs=2
)

atlantic = within_stddev(
    dataset=atlantic,
    parameter='d18O',
    num_devs=2
)

# Calculate the difference in d18O value between every core top, and then divide this by the distance between them.
pacific_d18O_by_distance, pacific_d18O = value_by_distance(
    dataset=pacific,
    value="d18O",
    differences=True
)

southern_d18O_by_distance, southern_d18O = value_by_distance(
    dataset=southern,
    value='d18O',
    differences=True,
)

atlantic_d18O_by_distance, atlantic_d18O = value_by_distance(
    dataset=atlantic,
    value='d18O',
    differences=True
)

# Store these values in a JSON file to be used in the file read_distance_lists.py
with open("data/permanent_lists/pacific_d18O_differences.json", 'w') as f:
    dump(pacific_d18O, f, indent=2)

with open("data/permanent_lists/southern_d18O_differences.json", 'w') as f:
    dump(southern_d18O, f, indent=2)

with open("data/permanent_lists/atlantic_d18O_differences.json", 'w') as f:
    dump(atlantic_d18O, f, indent=2)
