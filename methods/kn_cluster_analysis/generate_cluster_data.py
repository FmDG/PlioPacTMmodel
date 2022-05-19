from generate_files import assess_means
from kn_constants import time_sets

# Enter the path to the datasets
path_to_data = "data/PRISM_Pacific_data"

assess_means(path_to_data, time_sets).to_csv("data/pacific_pliocene.csv")
