from numpy import arange
from pandas import DataFrame

from maths_functions import end_member_solver


def simple_mixing_model(d18o, d13c, input_frame, start=0.30, stop=0.70):
    answers = []
    for row in input_frame.itertuples(index=False):
        prop_array = arange(start=start, stop=stop, step=0.01)
        for p in prop_array:
            ncw = end_member_solver(row.d18O, d18o, row.d13C, d13c, p)
            answers.append([row.Site, ncw[0], ncw[1], p])
    return DataFrame(answers, columns=["Site", "NCW_d18O", "NCW_d13C", "NCW:SCW"])
