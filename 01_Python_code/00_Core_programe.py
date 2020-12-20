import cv2
import numpy as np
import os
from timeit import default_timer as timer
from matplotlib import pyplot as plt
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import json
from scipy import linalg as la
from scipy import optimize
import sympy
import matplotlib as mpl

mpl.use("macosx")
# mpl.use("qt5agg")

sympy.init_printing()
img = cv2.imread("fromCamera/Springback_v00/DSC_0279.JPG", 1)  # type: np.ndarray
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

height = img.shape[0]

''' initial set
color_th_1 = [50, 100, 10, 60, 140, 170]  #
# color_th_11 = [50, 100, 10, 60, 140, 170]  # v1
color_th_2 = [80, 120, 50, 100, 60, 110]  #
color_th_3 = [70, 110, 100, 150, 15, 80]
color_th_4 = [60, 110, 110, 150, 80, 130]  #
color_th_41 = [60, 100, 110, 150, 80, 120]  # v1
color_th_42 = [50, 90, 110, 150, 80, 120]  # v2
color_th_5 = [140, 160, 120, 150, 40, 90]
color_th_6 = [130, 150, 80, 130, 0, 70]    #
color_th_7 = [30, 70, 140, 160, 160, 180]  #
color_th_8 = [40, 80, 30, 80, 145, 180]
'''
# flash 0214

c1 = [70, 120, 100, 120, 120, 140]  # d_green - Origin
c2 = [110, 150, 110, 130, 140, 160]  # y_green - Origin 2
c3 = [130, 190, 120, 135, 150, 190]  # yellow - bending pin
# c3 = [130, 170, 120, 135, 150, 190]  # yellow - bending pin
c4 = [70, 130, 110, 130, 80, 110]  # Blue - Point 1
# c4 = [70, 120, 110, 130, 80, 100]  # Blue - Point 1
c5 = [70, 115, 150, 200, 130, 150]  # Magenta - point 2

colors = [c1, c2, c3, c4, c5]


def circle_detect_LAB_list(image, color_th_list):

    l_min, l_max = color_th_list[0], color_th_list[1]
    a_min, a_max = color_th_list[2], color_th_list[3]
    b_min, b_max = color_th_list[4], color_th_list[5]

    l = image[:, :, 0]
    a = image[:, :, 1]
    b = image[:, :, 2]

    lab_split = np.concatenate((l, a, b), axis=1)
    cv2.namedWindow("LAB-split", cv2.WINDOW_NORMAL)
    cv2.imshow("LAB-split", lab_split)

    ret, min_l = cv2.threshold(l, l_min, 255, cv2.THRESH_BINARY)
    ret, max_l = cv2.threshold(l, l_max, 255, cv2.THRESH_BINARY_INV)
    l_filter = cv2.bitwise_and(min_l, max_l)

    cv2.namedWindow("L filter", cv2.WINDOW_NORMAL)
    cv2.imshow("L filter", l_filter)

    ret, min_a = cv2.threshold(a, a_min, 255, cv2.THRESH_BINARY)
    ret, max_a = cv2.threshold(a, a_max, 255, cv2.THRESH_BINARY_INV)
    a_filter = cv2.bitwise_and(min_a, max_a)

    cv2.namedWindow("A filter", cv2.WINDOW_NORMAL)
    cv2.imshow("A filter", a_filter)

    ret, min_b = cv2.threshold(b, b_min, 255, cv2.THRESH_BINARY)
    ret, max_b = cv2.threshold(b, b_max, 255, cv2.THRESH_BINARY_INV)
    b_filter = cv2.bitwise_and(min_b, max_b)

    cv2.namedWindow("B filter", cv2.WINDOW_NORMAL)
    cv2.imshow("B filter", b_filter)

    int_filter = cv2.bitwise_and(l_filter, a_filter)
    final_img = cv2.bitwise_and(int_filter, b_filter)

    cv2.namedWindow("final", cv2.WINDOW_NORMAL)
    cv2.imshow("final", final_img)

    blured_img = cv2.medianBlur(final_img, 7)

    cv2.namedWindow("blured", cv2.WINDOW_NORMAL)
    cv2.imshow("blured", blured_img)

    circles = cv2.HoughCircles(blured_img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=15, minRadius=40,
                               maxRadius=100)

    if circles is not None:
        circles = np.uint(np.around(circles))

        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 15)
            # draw the center of the circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 15)

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)

    # print(final_img.shape, final_img.ndim, final_img.dtype)
    # print(circles)
    # print(circles.shape)
    cv2.waitKey(0)

    if circles is not None:
        x = circles[0][0][0]
        y = circles[0][0][1]
        if circles.size > 3:
            print("more circles detected")
    else:
        print("missing marker")
        x, y = 0, 0
    return x, y


rty = circle_detect_LAB_list(lab, c3)

motion_dir = '/fromCamera/Motion_v00'
motion_dir_test = '/fromCamera/Motion_v00/unedited'
springback_dir = '/Users/khetamdouba/PycharmProjects/Pyserial_test/fromCamera/springback_v00'


def marker_detect_dir(directory):
    start = timer()
    b = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".JPG"):
            cwd = os.path.join(directory, filename)
            print(f"analysing: {cwd}")
            img = cv2.imread(cwd, 1)
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        else:
            continue

        a = []

        for i in colors:
            # del cl1
            X, Y = circle_detect_LAB_list(lab, i)
            # if not cl1[0]:
            #     cl1 = np.ndarray([0, 0])
            a.append(X)
            a.append(Y)
        print(a)
        b.append(a)
    print(b)
    end = timer()
    time = round(end - start, 2)
    print(f"Processing time in seconds: {time} for {len(b)} picture")

    return b


# motion = marker_detect_dir(motion_dir)
# np.savetxt("ndarray/motion_out.csv", motion, fmt="%.1f", delimiter=",")
motion = np.genfromtxt("ndarray/motion_out_modified.csv", delimiter=",")

# spring_back = marker_detect_dir(springback_dir)
# np.savetxt("ndarray/springback_out.csv", spring_back, fmt="%.1f", delimiter=",")
springback = np.genfromtxt("ndarray/springback_out.csv", delimiter=",")


# o1_x, o1_y, o2_x, o2_y, ben_x, ben_y, p1_x, p1_y, p2_x, p2_y

def coord_breakdown(array):
    # correct all y values
    array[:, 1::2] = height - array[:, 1::2]

    # move all to origin
    array[:, 0::2] = array[:, 0::2] - array[:, 0, np.newaxis]
    array[:, 1::2] = array[:, 1::2] - array[:, 1, np.newaxis]

    # Split arrays
    be_x = array[:, 4]
    be_y = array[:, 5]
    p1_x = array[:, 6]
    p1_y = array[:, 7]
    p2_x = array[:, 8]
    p2_y = array[:, 9]
    delta_w_x = p2_x - p1_x
    delta_w_y = p2_y - p1_y

    # attributes for bender coordinates
    coord_breakdown.be_x = be_x
    coord_breakdown.be_y = be_y

    # calculate angels
    rad_bender = np.arctan2(be_y, be_x)
    bender_angles = np.rad2deg(rad_bender)

    rad_wire = np.arctan2(delta_w_y, delta_w_x)
    wire_angles = np.rad2deg(rad_wire)

    # translate quadrants to real world angles
    wire_angles = 90 - wire_angles
    bender_angles = 90 - bender_angles
    # wire_angles = np.select([wire_angles > 90, wire_angles < 90], [wire_angles - 90, 90 - wire_angles])

    return bender_angles, wire_angles


mo_bender_angles, mo_wire_angles = coord_breakdown(motion)
mo_bender_angles -= mo_bender_angles[0]
mo_wire_angles -= mo_wire_angles[0]

sb_bender_angles, sb_wire_angles = coord_breakdown(springback)
sb_bender_angles -= sb_bender_angles[0] - 1.5
sb_bender_angles = sb_bender_angles[1::2]
sb_bender_angles = np.insert(sb_bender_angles, 0, 0)


sb_wire_angles -= sb_wire_angles[0]
sb_wire_angles_CV_measurements = sb_wire_angles[2::2]
sb_wire_delta = sb_wire_angles[1::2] - sb_wire_angles[2::2]
sb_bender_delta = sb_bender_angles[1::2]
# print(bender_angles, wire_angles)
sb_bender_angles_manual_measurements = np.array([0, 5, 10, 15, 20, 30, 45, 60, 75, 90, 95])
sb_wire_angles_manual_measurements = np.array([0, 1, 7, 13.5, 21, 35, 56.5, 78.5, 99.5, 118, 126])
sb_bender_angles_cv_delta = sb_bender_angles_manual_measurements - sb_bender_angles
sb_wire_angles_CV_measurements = np.insert(sb_wire_angles_CV_measurements, 0, 0)
sb_wire_angles_CV_delta_real = sb_wire_angles_manual_measurements - sb_wire_angles_CV_measurements
# cubic regression
x = np.linspace(0, 130, 200)
x_minor = np.array([9, 3.48])
Y = sb_bender_angles_manual_measurements
X = sb_wire_angles_manual_measurements
A = np.vstack([X ** 0, X ** 1, X ** 2, X ** 3])
sol, r, rank, sv = la.lstsq(A.T, Y)
y_fit = sol[0] + sol[1] * x + sol[2] * x ** 2 + sol[3] * x ** 3

y_fit_minor = sol[0] + sol[1] * x_minor + sol[2] * x_minor ** 2 + sol[3] * x_minor ** 3


def plotfigsize(figheight, ratio):
    cm2i = 1 / 2.54
    figehightcm = figheight * cm2i
    figwid = figheight * cm2i * ratio
    return figehightcm, figwid


def plot_rotation_verification():

    fig, ax = plt.subplots()  # type:figure.Figure, axes.Axes
    # fig, ax = plt.subplots(figsize=plotfigsize(9, 3/4))

    # ax.plot(sb_bender_angles, sb_wire_delta, ls="-", lw=1, color="r", label="Clockwise rotation")
    ax.plot(sb_bender_angles_manual_measurements, sb_bender_angles_cv_delta, ls="-", lw=1, color="r", label="Bender CV measurement error")
    ax.plot(sb_wire_angles_manual_measurements[:-1], sb_wire_angles_CV_delta_real[:-1], ls="-", lw=1, color="b", label="Wire CV measurement error")
    ax.plot([0, 130], [1, 1], ls="--", lw=1, color="k", label="Target tolerance")
    ax.plot([0, 130], [-1, -1], ls="--", lw=1, color="k")
    # ax.plot(sb_wire_angles[1:-2:2], sb_wire_delta[0:-1], ls="-", lw=1, color="r", label="Clockwise rotation")
    # ax.scatter(calib_angels, x_positive, color="r")

    # ax.plot(x, y_fit, ls=":", lw=1, color="b", label="Counter-clockwise rotation")

    ax.set_xlabel("Manual measurement (Degree)")
    ax.set_ylabel("Error_CV measurement (Degree)")

    ax.set_xlim(0, 120)
    ax.set_ylim(-2, 2)
    # ax.set_xlim(0, 135)
    # ax.set_ylim(3.5, 7.5)

    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
    # ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))

    ax.grid(color="gray", which="both", linestyle=':', linewidth=0.5)

    ax.set_title("Computer vision measurements verification")
    ax.legend()

    # fig.savefig('/Users/khetamdouba/desktop/interpolation 1.png', dpi=1000)

    plt.show()


# plot_rotation_verification()