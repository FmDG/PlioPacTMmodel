from generate_files import generate_means, assess_means, generate_full_data
from methods.kn_cluster_analysis.kn_constants import time_periods


# Enter the path to the datasets
path_to_data = "data/PRISM_Pacific_data"

generate_means(path_to_data, time_periods).to_csv("data/prism_data.csv")

# This assessment looks at the standard deviations and the number of samples being averaged in each case to make
# sure that this is a reliable data source.
assessment = assess_means(path_to_data, time_periods).to_csv("data/assessment.csv")
full_data = generate_full_data(path_to_data).to_csv("data/full_dataset.csv")
