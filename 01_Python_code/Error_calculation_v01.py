import numpy as np

# r : arc radius
# h : arc height
# c : chord length (arc width)
# ceta : total arc angle
# div : number of division (number of cords)
# divd_ceta : divided total = bended wire angle 

# half circle
height = np.array([100, 105, 95, 100])
width = np.array([200, 235, 238, 202])
divisions = np.array([20, 20, 20, 20])

# saddle curve
s_height = np.array([20, 12, 15, 21])
s_width = np.array([200, 223, 213, 205])
s_divisions = np.array([13, 13, 13, 13])


def bending_angel(h, c, div):

    r = (h / 2) + ((c ** 2) / (8 * h))
    ceta = 2 * np.arcsin(c / (2 * r))

    divd_ceta = ceta / div
    bended_angel = np.rad2deg(divd_ceta)

    absolute_error = bended_angel[0] - bended_angel
    relative_error = 100 * (absolute_error/bended_angel[0])

    results = np.vstack([bended_angel, absolute_error, relative_error])
    return results


c_result = bending_angel(height, width, divisions)
print(c_result)
s_result = bending_angel(s_height, s_width, s_divisions)
print(s_result)