import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Qt5Agg')

# Read curve points from  grasshopper
gh_points_csv = np.loadtxt(fname="Read_Files/PointsToNumbers_from_Grasshopper_V01.csv")

# Parse data for x and y values
x_curve_gh = gh_points_csv[0::3]
y_curve_gh = gh_points_csv[1::3]

# Create x1, x2, y1 and y2 arrays
x1_curve_gh = x_curve_gh[0:-1]  # remove last value
x2_curve_gh = x_curve_gh[1:]    # shift ndarray -1
y1_curve_gh = y_curve_gh[0:-1]
y2_curve_gh = y_curve_gh[1:]


# Define distance function for y feed. dist = sqrt(dx**2 + dy**2).
def distance(x1, x2, y1, y2):
    dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
    return dist


# Define a function to calculate rotation angels between consecutive lines.
def slope_points_rad(x1, x2, y1, y2):
    # normal arctan function dose not return signed values.
    # move lines to origin by calculating delta.
    dx = x2 - x1
    dy = y2 - y1
    # Get all signed slopes by using arctan2 function.
    slopes = np.arctan2(dy, dx)
    # vectorised ndarray operation to get the change in slope between all lines.
    slope_1 = slopes[0:-1]
    slope_2 = slopes[1:]
    return slope_1 - slope_2


# Calculate y feed
y_feed = distance(x1_curve_gh, x2_curve_gh, y1_curve_gh, y2_curve_gh)

# Calculate x feed (wire bending angels)
x_feed = np.rad2deg(slope_points_rad(x1_curve_gh, x2_curve_gh, y1_curve_gh, y2_curve_gh))

# Read motion table from Ansys , Zeros already added
di_motion_v02 = pd.read_excel("Read_Files/End_Mid_Motion_v02.xlsx", nrows=89)
di_motion_v02_data = pd.DataFrame(di_motion_v02, columns=["pin_Angel", "x2_mot", "y2_mot", "x1_mot", "y1_mot"])
di_motion_v02_np = np.array(di_motion_v02_data)

# Parse Motion data into relative ndarrays.
x1_mot = di_motion_v02_np[:, 3] + 10
y1_mot = di_motion_v02_np[:, 4]
x2_mot = di_motion_v02_np[:, 1]
y2_mot = di_motion_v02_np[:, 2]
pin_mot_deg = di_motion_v02_np[:, 0].astype('int')

# Read springBack data from Ansys then add zeros before origin adjustments.
di_sb_r3 = pd.read_excel("Read_Files/DW_DP_Mah_V01.xlsx")
# assumed angels
pin_angel_deg = np.array([0, 5, 10, 15, 20, 30, 45, 60, 75, 90, 110, 130])
# read only data column excluding header (default behaviour)
di_sb_r3_data = pd.DataFrame(di_sb_r3, columns=["DP 0"])
# convert pandas DataFrame to numpy ndarray
di_sb_r3_np = np.array(di_sb_r3_data)
# Transpose dose not wor on 1d ndarray, Horizontal stack is used instead
di_sb_r3_np = np.hstack(di_sb_r3_np)

# Parse Motion data into relative ndarrays.
# slicing data to 8 1d arrays loaded and unloaded lists for midPoint(x1, y1), endPoint(x2,  y2)
# Loaded wire lists
x1_loaded = di_sb_r3_np[6::8]
x1_loaded = np.insert(x1_loaded, 0, 0) + 10  # add zero and add 10 to correct mid point origin.
y1_loaded = di_sb_r3_np[7::8]
y1_loaded = np.insert(y1_loaded, 0, 0)
x2_loaded = di_sb_r3_np[2::8]  # endPoint
x2_loaded = np.insert(x2_loaded, 0, 0)
y2_loaded = di_sb_r3_np[3::8]
y2_loaded = np.insert(y2_loaded, 0, 0)

# unLoaded wire lists
x1_unloaded = di_sb_r3_np[4::8]
x1_unloaded = np.insert(x1_unloaded, 0, 0) + 10  # add 10 to correct mid point origin.
y1_unloaded = di_sb_r3_np[5::8]
y1_unloaded = np.insert(y1_unloaded, 0, 0)
x2_unloaded = di_sb_r3_np[0::8]  # endPoint
x2_unloaded = np.insert(x2_unloaded, 0, 0)
y2_unloaded = di_sb_r3_np[1::8]
y2_unloaded = np.insert(y2_unloaded, 0, 0)


#  Define function to calculate slope using dy/dx formula.
def slope_rad(x1, x2, y1, y2):
    # improve performance by using vectorised operations instead of looping.
    # create an ndarray for Tan 90 to avoid singularities.
    base_90 = np.ones_like(x1) * 90
    # Create an ndarray for slopes in Q2 and mirror it to Q1.
    slope_q1 = np.arctan((y2 - y1) / (x2 - x1)) * -1
    # Create an ndarray for slopes in Q1, move it to q2 and get positive values.
    slope_q2 = (np.arctan((y2 - y1) / (x2 - x1)) - np.pi) * -1
    # Piecewise operation to select relative values and return them.
    return np.select([x2 < x1, x2 == x1, x2 > x1], [slope_q1, base_90, slope_q2])


# Calculate Motion slope for wires
mot_slope_rad = slope_rad(x1_mot, x2_mot, y1_mot, y2_mot)
mot_slope_deg = np.rad2deg(mot_slope_rad)

# Calculate slopes for loaded wires.
loaded_slope_rad = slope_rad(x1_loaded, x2_loaded, y1_loaded, y2_loaded)
loaded_slope_deg = np.rad2deg(loaded_slope_rad)

# Calculate slopes for unloaded wires.
unloaded_slope_rad = slope_rad(x1_unloaded, x2_unloaded, y1_unloaded, y2_unloaded)
unloaded_slope_deg = np.rad2deg(unloaded_slope_rad)

# Calculate springBack slope for wires.
spring_back_deg = loaded_slope_deg - unloaded_slope_deg


fig_a, ax = plt.subplots()
# ax.plot(loaded_slope_deg, spring_back)
ax.scatter(loaded_slope_deg, spring_back_deg)
# plt.draw()
plt.show()


fig_b, ax = plt.subplots()
ax.plot(x1_loaded, y1_loaded)
ax.scatter(x1_loaded, y1_loaded)
ax.plot(x2_loaded, y2_loaded)
ax.scatter(x2_loaded, y2_loaded)

for i in np.arange(x1_loaded.size):
    temp_x1x2 = (x1_loaded[i], x2_loaded[i])
    temp_y1y2 = (y1_loaded[i], y2_loaded[i])
    ax.plot(temp_x1x2, temp_y1y2, ":", "b")
    ax.scatter(temp_x1x2, temp_y1y2)
plt.show()
fig_c, ax = plt.subplots()
ax.plot(pin_angel_deg, loaded_slope_deg - pin_angel_deg)
ax.scatter(pin_angel_deg, loaded_slope_deg - pin_angel_deg)
# ax.scatter(loaded_slope_deg, spring_back)
plt.show()
# print(di_sp_r3_data)
# print(di_sp_r3_np.dtype)
# print(di_sp_r3_np.shape)
fig_c.savefig("test.eps", facecolor="#f1f1f1")

