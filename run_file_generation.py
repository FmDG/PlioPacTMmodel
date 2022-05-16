from generate_files import generate_means, assess_means, generate_full_data


# Enter the path to the datasets
path_to_data = "data/PRISM_Pacific_data"

# Enter the Time Periods we're investigating in the format ["Name", Start, End]. These time periods are derived from the
# van der Weijst et al., 2020 paper.
time_periods = [["3500 ka - M2", 3500, 3320],
                ["M2", 3303, 3288],
                ["mPWP-1", 3280, 3155],
                ["KM2", 3148, 3120],
                ["mPWP-2", 3105, 3030],
                ["G20", 3025, 3000],
                ["G20 - 2800 ka", 2985, 2800],
                ["iNHG", 2800, 2700]]

generate_means(path_to_data, time_periods).to_csv("data/prism_data.csv")

# This assessment looks at the standard deviations and the number of samples being averaged in each case to make
# sure that this is a reliable data source.
assessment = assess_means(path_to_data, time_periods).to_csv("data/assessment.csv")
full_data = generate_full_data(path_to_data).to_csv("data/full_dataset.csv")
