import os

import pandas as pd
import matplotlib.pyplot as plt


def investigate():
    atlantic_cd = pd.read_json('data/permanent_lists/atlantic_core_distances.json')
    pacific_cd = pd.read_json('data/permanent_lists/pacific_core_distances.json')
    southern_cd = pd.read_json('data/permanent_lists/southern_core_distances.json')

    plt.hist(atlantic_cd)
    plt.show()


if __name__ == '__main__':
    os.chdir('../..')
    investigate()


