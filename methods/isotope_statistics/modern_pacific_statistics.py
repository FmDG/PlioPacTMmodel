from matplotlib.pyplot import show
from pandas import read_csv
from os import chdir
from scipy.stats import pearsonr

from methods.general.general_functions import within_stddev
from statistics_functions import isotope_by_factor, plot_by_factor, lgm_by_factor

# Read the Pacific Modern Core Top Data
chdir("../..")
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
depth_influence = isotope_by_factor(
    dataset=pacific,
    factor=parameter,
    minimum=-0,
    maximum=5000,
    step_size=step_size
)

plot_by_factor(
    dataset=pacific,
    factor_dataset=depth_influence,
    factor=parameter,
    step_size=step_size
)

for x in ["latitude", "depth", "longitude"]:
    for y in ["d18O", "d13C"]:
        pearson_stat, p_01 = pearsonr(pacific[x], pacific[y])
        print('For {x} against {y}, Pearson statistics are stat={stats}, p={p_val}'.format(
            x=x,
            y=y,
            stats=pearson_stat,
            p_val=p_01
        ))

show()
