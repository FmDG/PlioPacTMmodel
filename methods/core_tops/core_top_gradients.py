from os import chdir
import pandas as pd

# Change to the relevant directory
chdir("../..")

pacific_data = pd.read_csv("data/core_tops/pacific_core_tops.csv")
s_atlantic_data = pd.read_csv("data/core_tops/south_atlantic_core_tops.csv")
n_atlantic_data = pd.read_csv("data/core_tops/north_atlantic_core_tops.csv")
indian_data = pd.read_csv("data/core_tops/indian_core_tops.csv")
southern_data = pd.read_csv("data/core_tops/southern_core_tops.csv")





