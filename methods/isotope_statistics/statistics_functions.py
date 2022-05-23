from matplotlib.pyplot import subplots
from numpy import arange, sqrt
from pandas import DataFrame
from seaborn import scatterplot
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from geopy.distance import distance

from methods.general.general_constants import axis_args


def isotope_by_factor(dataset, factor, minimum, maximum, step_size):
    # Generate a list of bounding boxes
    bounding_box = arange(
        start=minimum,
        stop=maximum,
        step=step_size
    )

    answers = []

    # Iterate over this list, finding the average d18O and d13C
    for i in bounding_box:
        mean_d18o = dataset[
            dataset[factor].between(
                (i - (step_size/2)),
                (i + (step_size/2))
            )
        ].d18O.mean()

        stddev_d18o = dataset[
            dataset[factor].between(
                (i - (step_size / 2)),
                (i + (step_size / 2))
            )
        ].d18O.std()

        mean_d13c = dataset[
            dataset[factor].between(
                (i - (step_size/2)),
                (i + (step_size/2))
            )
        ].d13C.mean()

        stddev_d13c = dataset[
            dataset[factor].between(
                (i - (step_size / 2)),
                (i + (step_size / 2))
            )
        ].d13C.std()

        answers.append([i, mean_d18o, stddev_d18o, mean_d13c, stddev_d13c])

    return DataFrame(
        answers,
        columns=[
            factor,
            'mean_d18O',
            "stddev_d18O",
            'mean_d13C',
            "stddev_d13C"
        ]
    )


def plot_by_factor(dataset, factor_dataset, factor, step_size):
    # Plot the Results
    fig, axs = subplots(
        nrows=1,
        ncols=2,
        figsize=(14, 7)
    )

    fig.suptitle("Modern Ocean Core Tops")

    scatterplot(
        data=dataset,
        x="d18O",
        y="d13C",
        hue=factor,
        ax=axs[0],
        palette="viridis"
    )

    axs[0].set(title="Full Dataset", **axis_args)

    scatterplot(
        data=factor_dataset,
        x="mean_d18O",
        y="mean_d13C",
        hue=factor,
        ax=axs[1],
        legend='full',
        palette="viridis"
    )

    axs[1].errorbar(
        data=factor_dataset,
        x="mean_d18O",
        y="mean_d13C",
        xerr="stddev_d18O",
        yerr="stddev_d13C",
        fmt="+",
        alpha=0.3
    )

    axs[1].set(title=r'Mean values for {} bands of step size={}'.format(factor, step_size), **axis_args)


def lgm_by_factor(dataset, factor, parameter):

    regressor = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(
        dataset[factor].values.reshape(-1, 1),
        dataset[parameter].values.reshape(-1, 1),
        test_size=0.2,
        random_state=0
    )

    regressor.fit(x_train, y_train)

    y_predict = regressor.predict(x_test)
    # Print intercept and coefficient
    print_string = r'{} = {:.3f} {} + {:.3f} (r$^2$ = {:.3f})'.format(
            parameter,
            regressor.intercept_[0],
            factor,
            regressor.coef_[0][0],
            regressor.score(
                dataset[factor].values.reshape(-1, 1),
                dataset[parameter].values.reshape(-1, 1)
            )
        )

    _, ax = subplots()

    ax.scatter(
        dataset[factor].values.reshape(-1, 1),
        dataset[parameter].values.reshape(-1, 1),
        color='gray'
    )

    ax.plot(
        x_test,
        y_predict,
        color='red',
        linewidth=2
    )

    ax.text(
        0.8, 0.9,
        print_string,
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes
    )

    ax.set(
        xlabel=factor,
        ylabel=parameter
    )

    print('Root Mean Squared Error:', sqrt(metrics.mean_squared_error(y_test, y_predict)))
    print(print_string)


def value_by_distance(dataset, value):
    values_over_distances = []
    distances = []

    for _, x in dataset.iterrows():
        for _, y in dataset.iterrows():
            if x.Core != y.Core:
                distance_value = distance(
                    (x.latitude, x.longitude),
                    (y.latitude, y.longitude)
                ).km

                if (distance_value != 0) and (distance_value not in distances):
                    del_value = float(x[value] - y[value])
                    values_over_distances.append(del_value / distance_value)
                    distances.append(distance)
    return values_over_distances
