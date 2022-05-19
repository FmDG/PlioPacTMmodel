import matplotlib.pyplot as plt
from pandas import read_csv

from methods.general.general_functions import within_stddev
from statistics_functions import isotope_by_factor, plot_by_factor, lgm_by_factor

# Read the Pacific Modern Core Top Data
pacific = read_csv('data/pacific_modern.csv')

# Remove values that are more than 3 standard deviations away from the mean
pacific = within_stddev(
    within_stddev(
        pacific,
        "d18O",
        num_devs=3
    ),
    "d13C",
    num_devs=3
)

parameter, step_size = "latitude", 10
latitude_influence = isotope_by_factor(
    dataset=pacific,
    factor=parameter,
    minimum=-55,
    maximum=55,
    step_size=step_size
)

plot_by_factor(
    dataset=pacific,
    factor_dataset=latitude_influence,
    factor=parameter,
    step_size=step_size
)

parameter, step_size = "depth", 1000
plot_by_factor(
    dataset=pacific,
    factor_dataset=isotope_by_factor(
        dataset=pacific,
        factor=parameter,
        minimum=-0,
        maximum=5000,
        step_size=step_size
    ),
    factor=parameter,
    step_size=step_size
)

lgm_by_factor(pacific, "depth", "d13C")
lgm_by_factor(pacific, "latitude", "d13C")
lgm_by_factor(pacific, "depth", "d18O")
lgm_by_factor(pacific, "latitude", "d18O")

plt.show()

