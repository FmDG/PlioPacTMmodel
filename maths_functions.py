"""
Mathematical functions listed in van der Weijst, 2020 paper
"""


def bmm_solver(x_0, x_1, x_2, y_0, y_1, y_2):
    """
    If we know the end-member d13C and d18O values, then for a given site d18O and d13C we can generate two different
    proportions of NCW:SCW that fit the equations.
    :param x_0: Site d18O
    :param x_1: NCW d18O
    :param x_2: SCW d18O
    :param y_0: Site d13C
    :param y_1: NCW d13C
    :param y_2: SCW d13C
    :return: p_1 and p_2 are the possible proportions of NCW:SCW
    """
    p_1 = (x_0 - x_2)/(x_1 - x_2)
    p_2 = (y_0 - y_2)/(y_1 - y_2)
    return p_1, p_2


def end_member_solver(x_0, x_2, y_0, y_2, p):
    """
    If we have the proportion of NCW:SCW and the composition of one endmember and the site composition we can work out
    the composition of the other end-member
    :param x_0: Site d18O
    :param x_2: SCW d18O
    :param y_0: Site d13C
    :param y_2: SCW d13C
    :param p: Proportion of NCW:SCW
    :return: x_1: NCW d18O
             y_1: NCW d13C
    """
    x_1 = (x_0 + ((p-1) * x_2))/p
    y_1 = (y_0 + ((p-1) * y_2))/p
    return [x_1, y_1]


def generate_d18o_ncw(d13c_ncw1, d13c_ncw2, d13c_site, d13c_scw, d18o_ncw1, d18o_ncw2, d18o_site, d18o_scw):
    d18o_ncw = ((d13c_ncw2 - ((d13c_ncw2 - d13c_ncw1)/(d18o_ncw2 - d18o_ncw1))*d18o_ncw2) - (d13c_site - ((d13c_site - d13c_scw)/(d18o_site - d18o_scw))*d18o_site))/(((d13c_site-d13c_scw)/(d18o_site-d18o_scw)) - ((d13c_ncw2-d13c_ncw1)/(d18o_ncw2-d18o_ncw1)))
    return d18o_ncw


def generate_d13c_ncw(d13c_site, d13c_scw, d18o_site, d18o_scw, d18o_ncw):
    d13c_ncw = (((d13c_site - d13c_scw)/(d18o_site - d18o_scw))*d18o_ncw) + d13c_site - (((d13c_site - d13c_scw)/(d18o_site - d18o_scw))*d18o_site)
    return d13c_ncw
