from generate_files import assess_means
from methods.general.general_constants import time_sets
from os import chdir

chdir("../..")

# Enter the path to the datasets
path_to_data = "data/PRISM_Pacific_data"

assess_means(path_to_data, time_sets).to_csv("data/pacific_pliocene.csv")
