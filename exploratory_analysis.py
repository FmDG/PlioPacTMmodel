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


sns.relplot(data=isotope_space, x="d18O", y="d13C", col="TimePeriod", col_wrap=4, hue="Site")

plt.show()
