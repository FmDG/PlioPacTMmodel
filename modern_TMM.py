"""
Attempting to build the first version of the model using the core top data provided by Schmittner et al., 2017
(https://doi.org/10.1002/2016PA003072) and the theory of the ternary mixing model from van der Weijst et al., 2020.

"""

import pandas as pd

# read the csv file containing the core-top data
core_tops = pd.read_csv("data/schmittner_2017.csv")


