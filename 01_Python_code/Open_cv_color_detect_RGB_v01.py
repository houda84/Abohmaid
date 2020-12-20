import cv2
import numpy as np

img = cv2.imread("fromCamera/DSC_0205.JPG", 1)  # type: np.ndarray
# (h, w) = img.shape[:2]

# cv2.namedWindow("img", cv2.WINDOW_NORMAL)
# cv2.imshow("img", img)
# cv2.waitKey(0)

cb = img[:, :, 0]
cg = img[:, :, 1]
cr = img[:, :, 2]

BRG_split = np.concatenate((cb, cg, cr), axis=1)
cv2.namedWindow("BRG-split", cv2.WINDOW_NORMAL)
cv2.imshow("BRG-split", BRG_split)

ret, min_blue = cv2.threshold(cb, 60, 255, cv2.THRESH_BINARY)       # mam2 120 , glm1 100,
ret, max_blue = cv2.threshold(cb, 90, 255, cv2.THRESH_BINARY_INV)   # mam2 180 , glm1 125,
blue_filter = cv2.bitwise_and(min_blue, max_blue)
cv2.namedWindow("blue filter", cv2.WINDOW_NORMAL)
cv2.imshow("blue filter", blue_filter)

ret, min_green = cv2.threshold(cg, 110, 255, cv2.THRESH_BINARY)      # mam2 142 , glm1 120
ret, max_green = cv2.threshold(cg, 140, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
green_filter = cv2.bitwise_and(min_green, max_green)
cv2.namedWindow("green filter", cv2.WINDOW_NORMAL)
cv2.imshow("green filter", green_filter)

ret, min_red = cv2.threshold(cr, 90, 255, cv2.THRESH_BINARY)      # mam2 142 , glm1 120
ret, max_red = cv2.threshold(cr, 105, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
red_filter = cv2.bitwise_and(min_red, max_red)
cv2.namedWindow("red filter", cv2.WINDOW_NORMAL)
cv2.imshow("red filter", red_filter)

final_img = cv2.bitwise_and(blue_filter, green_filter, red_filter)
cv2.namedWindow("final", cv2.WINDOW_NORMAL)
cv2.imshow("final", final_img)

blured_img = cv2.medianBlur(final_img, 7)
cv2.namedWindow("blured", cv2.WINDOW_NORMAL)
cv2.imshow("blured", blured_img)

circles = cv2.HoughCircles(blured_img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=15, minRadius=40, maxRadius=120)

if circles is not None:
    circles = np.uint(np.around(circles))

    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), -1)
        # draw the center of the circle
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 1)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow("img", img)

print(final_img.shape, final_img.ndim, final_img.dtype)
print(circles)
print(circles.shape)
cv2.waitKey(0)
