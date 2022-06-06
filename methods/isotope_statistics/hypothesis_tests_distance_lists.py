import random
import json
import os
import numpy as np
import scipy.stats as st

oceans = ["pacific", "n_atlantic", "s_atlantic", "southern", "indian"]
os.chdir("../..")

for ocean in oceans:
    with open("data/permanent_lists/{}_d18O_gradients.json".format(ocean), 'r') as f:
        d18O_by_distance = json.load(f)

    confidence = 0.95

    # create 95% confidence interval for population mean weight
    confidence_intervals = st.expon.interval(alpha=confidence, loc=np.mean(d18O_by_distance),
                                             scale=st.sem(d18O_by_distance))

    print("OCEAN: {}\nThe {}% Confidence Interval is {:.6f} permil/km\n-----".format(
        ocean, confidence * 100, confidence_intervals[1]))

# This is the distance between 1209 and 1208, and the d18O difference observed.
print("Between 1209 and 1208 we have {:.4f} permil/km".format((0.5/387.5)))
