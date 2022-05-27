import random
import json
import os
import numpy as np
import scipy.stats as st

oceans = ["pacific", "atlantic", "southern"]
os.chdir("../..")

for ocean in oceans:
    with open("data/permanent_lists/{}_core_distances.json".format(ocean), 'r') as f:
        d18O_by_distance = json.load(f)

    # Select a random sample from the whole
    sample = np.asarray(d18O_by_distance)
    confidence = 0.95

    # create 95% confidence interval for population mean weight
    confidence_intervals = st.norm.interval(alpha=confidence, loc=np.mean(sample), scale=st.sem(sample))

    print("OCEAN: {}\nThe {}% Confidence Intervals are {:.6f} and {:.6f} permil/km\n-----".format(ocean,
                                                                                                  confidence * 100,
                                                                                                  confidence_intervals[0],
                                                                                                  confidence_intervals[1]
                                                                                      ))
    # This is the distance between 1209 and 1208, and the d18O difference observed.

print("Between 1209 and 1208 we have {:.4f} permil/km".format((0.5/387.5)))
