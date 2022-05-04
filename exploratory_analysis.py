import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

# Open connection to SQL database
connection = sqlite3.connect("data/prism_data.db")
# Load the database as a Pandas Dataframe
isotope_space = pd.read_sql("SELECT * FROM isotopes", connection)
# Close the connection to the SQL database.
connection.close()

# Plot the isotope space for each time slice
sns.relplot(data=isotope_space, x="d18O", y="d13C", col="TimePeriod", col_wrap=4, hue="Site")

# Plot the site data
site_data = isotope_space[isotope_space.Site == "h16_dsdp594"]
sns.relplot(data=site_data, x="d18O", y="d13C", hue="TimePeriod")

# Plot the TimePeriod data
time_data = isotope_space[isotope_space.TimePeriod == "3500 ka - M2"]
sns.relplot(data=time_data, x="d18O", y="d13C", hue="Site")

plt.show()