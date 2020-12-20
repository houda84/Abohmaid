import cv2
import numpy as np

img = cv2.imread("fromCamera/Springback_v00/DSC_0279.JPG", 1)  # type: np.ndarray

B_min, B_max = 60, 90
G_min, G_max = 110, 140
R_min, R_max = 90, 105

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
color_th_1 = [60, 100, 15, 70, 160, 210]  # Magenta - point 2
color_th_3 = [65, 100, 80, 110, 15, 80]    # d_green - Origin
color_th_4 = [60, 110, 110, 150, 80, 130]  # y_green - Origin 2
color_th_6 = [140, 160, 80, 130, 0, 70]    # Blue - Point 1
color_th_7 = [10, 70, 130, 160, 160, 180]  # yellow - bending pin


def circle_detect_BGR(image, b_min, b_max, g_min, g_max, r_min, r_max):
    cb = image[:, :, 0]
    cg = image[:, :, 1]
    cr = image[:, :, 2]

    BRG_split = np.concatenate((cb, cg, cr), axis=1)
    cv2.namedWindow("BRG-split", cv2.WINDOW_NORMAL)
    cv2.imshow("BRG-split", BRG_split)

    ret, min_blue = cv2.threshold(cb, b_min, 255, cv2.THRESH_BINARY)  # mam2 120 , glm1 100,
    ret, max_blue = cv2.threshold(cb, b_max, 255, cv2.THRESH_BINARY_INV)  # mam2 180 , glm1 125,
    blue_filter = cv2.bitwise_and(min_blue, max_blue)
    cv2.namedWindow("blue filter", cv2.WINDOW_NORMAL)
    cv2.imshow("blue filter", blue_filter)

    ret, min_green = cv2.threshold(cg, g_min, 255, cv2.THRESH_BINARY)  # mam2 142 , glm1 120
    ret, max_green = cv2.threshold(cg, g_max, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
    green_filter = cv2.bitwise_and(min_green, max_green)
    cv2.namedWindow("green filter", cv2.WINDOW_NORMAL)
    cv2.imshow("green filter", green_filter)

    ret, min_red = cv2.threshold(cr, r_min, 255, cv2.THRESH_BINARY)  # mam2 142 , glm1 120
    ret, max_red = cv2.threshold(cr, r_max, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
    red_filter = cv2.bitwise_and(min_red, max_red)
    cv2.namedWindow("red filter", cv2.WINDOW_NORMAL)
    cv2.imshow("red filter", red_filter)

    final_img = cv2.bitwise_and(blue_filter, green_filter, red_filter)
    # cv2.namedWindow("final", cv2.WINDOW_NORMAL)
    # cv2.imshow("final", final_img)

    blured_img = cv2.medianBlur(final_img, 7)
    cv2.namedWindow("blured", cv2.WINDOW_NORMAL)
    cv2.imshow("blured", blured_img)

    circles = cv2.HoughCircles(blured_img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=15, minRadius=40,
                               maxRadius=120)

    if circles is not None:
        circles = np.uint(np.around(circles))

        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), -1)
            # draw the center of the circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 1)

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)

    # print(final_img.shape, final_img.ndim, final_img.dtype)
    # print(circles)
    # print(circles.shape)
    cv2.waitKey(0)
    return circles


def circle_detect_BGR_list(image, color_th_list):

    b_min, b_max = color_th_list[0], color_th_list[1]
    g_min, g_max = color_th_list[2], color_th_list[3]
    r_min, r_max = color_th_list[4], color_th_list[5]

    cb = image[:, :, 0]
    cg = image[:, :, 1]
    cr = image[:, :, 2]

    BRG_split = np.concatenate((cb, cg, cr), axis=1)
    cv2.namedWindow("BRG-split", cv2.WINDOW_NORMAL)
    cv2.imshow("BRG-split", BRG_split)

    ret, min_blue = cv2.threshold(cb, b_min, 255, cv2.THRESH_BINARY)  # mam2 120 , glm1 100,
    ret, max_blue = cv2.threshold(cb, b_max, 255, cv2.THRESH_BINARY_INV)  # mam2 180 , glm1 125,
    blue_filter = cv2.bitwise_and(min_blue, max_blue)
    cv2.namedWindow("blue filter", cv2.WINDOW_NORMAL)
    cv2.imshow("blue filter", blue_filter)

    ret, min_green = cv2.threshold(cg, g_min, 255, cv2.THRESH_BINARY)  # mam2 142 , glm1 120
    ret, max_green = cv2.threshold(cg, g_max, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
    green_filter = cv2.bitwise_and(min_green, max_green)
    cv2.namedWindow("green filter", cv2.WINDOW_NORMAL)
    cv2.imshow("green filter", green_filter)

    ret, min_red = cv2.threshold(cr, r_min, 255, cv2.THRESH_BINARY)  # mam2 142 , glm1 120
    ret, max_red = cv2.threshold(cr, r_max, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
    red_filter = cv2.bitwise_and(min_red, max_red)
    cv2.namedWindow("red filter", cv2.WINDOW_NORMAL)
    cv2.imshow("red filter", red_filter)


    int_filter = cv2.bitwise_and(blue_filter, green_filter)
    final_img = cv2.bitwise_and(int_filter, red_filter)
    # final_img = cv2.bitwise_and(blue_filter, green_filter, red_filter)
    cv2.namedWindow("final", cv2.WINDOW_NORMAL)
    cv2.imshow("final", final_img)

    blured_img = cv2.medianBlur(final_img, 7)
    cv2.namedWindow("blured", cv2.WINDOW_NORMAL)
    cv2.imshow("blured", blured_img)

    circles = cv2.HoughCircles(blured_img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=15, minRadius=40,
                               maxRadius=120)

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
    return circles


# yellow = circle_detect_BGR(img, B_min, B_max, G_min, G_max, R_min, R_max)
cl1 = circle_detect_BGR_list(img, color_th_7)
print(cl1)
