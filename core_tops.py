import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pandas import read_csv, DataFrame
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Read the Pacific Modern Core Top Data
pacific = read_csv('data/pacific_modern.csv')

# Remove values that are more than 3 standard deviations away from the mean
pacific = pacific[pacific.d18O > (pacific.d18O.mean() - (3 * pacific.d18O.std()))]
pacific = pacific[pacific.d13C > (pacific.d13C.mean() - (3 * pacific.d13C.std()))]

# Generate a list of bounding boxes
step_size = 10
bounding_box = np.arange(start=-55, stop=55, step=step_size)
answers = []
# Iterate over this list, finding the average d18O and d13C
for i in bounding_box:
    mean_d18o = pacific[pacific.latitude.between((i - (step_size/2)), (i + (step_size/2)))].d18O.mean()
    mean_d13c = pacific[pacific.latitude.between((i - (step_size/2)), (i + (step_size/2)))].d13C.mean()
    answers.append([i, mean_d18o, mean_d13c])
mean_bounding = DataFrame(answers, columns=["latitude", 'mean_d18O', 'mean_d13C'])

# Plot the Results
fig, axs = plt.subplots(1, 2)
fig.suptitle("Modern Ocean Core Tops")

sns.scatterplot(data=pacific, x="d18O", y="d13C", hue="latitude", ax=axs[0], palette="viridis")
axs[0].set(xlim=[0, 5], ylim=[-0.5, 2.0], xlabel=r'$\delta^{18}$O', ylabel=r'$\delta^{13}$C', title="Full Dataset")
sns.scatterplot(data=mean_bounding, x="mean_d18O", y="mean_d13C", hue="latitude", ax=axs[1], legend="full",
                palette="viridis")
axs[1].set(xlim=[0, 5], ylim=[-0.5, 2.0], xlabel=r'Mean $\delta^{18}$O', ylabel=r'Mean $\delta^{13}$C',
           title=r'Mean values for latitude bands of {}$\degree$'.format(step_size))


def linear_regression_model(x, y, split=True):
    x = x.values.reshape(-1, 1)
    y = y.values.reshape(-1, 1)

    regressor = LinearRegression()
    if split:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
        regressor.fit(x_train, y_train)  # training the algorithm
        y_predict = regressor.predict(x_test)
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_predict))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_predict))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_predict)))
        x_plot = x_test
    else:
        regressor.fit(x, y)
        y_predict = regressor.predict(x)
        x_plot = x

    # Print intercept and coefficient
    print_string = r'y = {:.3f} x + {:.3f} (r$^2$ = {:.3f})'.format(regressor.intercept_[0], regressor.coef_[0][0],
                                                                    regressor.score(x, y))
    print(print_string)

    _, ax = plt.subplots()
    ax.scatter(x, y,  color='gray')
    ax.plot(x_plot, y_predict, color='red', linewidth=2)
    plt.text(0.8, 0.9, print_string, horizontalalignment='center',
             verticalalignment='center', transform=ax.transAxes)

    plt.show()


linear_regression_model(mean_bounding.latitude, mean_bounding.mean_d13C, split=False)
