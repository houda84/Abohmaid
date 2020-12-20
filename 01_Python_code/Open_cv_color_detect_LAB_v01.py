import cv2
import numpy as np

img = cv2.imread("fromCamera/DSC_0208.JPG", 1)  # type: np.ndarray
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# (h, w) = img.shape[:2]



l = lab[:, :, 0]
a = lab[:, :, 1]
b = lab[:, :, 2]

lab_split = np.concatenate((l, a, b), axis=1)
cv2.namedWindow("LAB-split", cv2.WINDOW_NORMAL)
cv2.imshow("LAB-split", lab_split)

ret, min_L = cv2.threshold(l, 120, 255, cv2.THRESH_BINARY)       # mam2 120 , glm1 100,
ret, max_L = cv2.threshold(l, 130, 255, cv2.THRESH_BINARY_INV)   # mam2 180 , glm1 125,
L_filter = cv2.bitwise_and(min_L, max_L)
# cv2.namedWindow("blue filter", cv2.WINDOW_NORMAL)
# cv2.imshow("blue filter", L_filter)

ret, min_a = cv2.threshold(a, 105, 255, cv2.THRESH_BINARY)      # mam2 142 , glm1 120
ret, max_a = cv2.threshold(a, 125, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
a_filter = cv2.bitwise_and(min_a, max_a)
# cv2.namedWindow("green filter", cv2.WINDOW_NORMAL)
# cv2.imshow("green filter", a_filter)

ret, min_b = cv2.threshold(b, 140, 255, cv2.THRESH_BINARY)      # mam2 142 , glm1 120
ret, max_b = cv2.threshold(b, 160, 255, cv2.THRESH_BINARY_INV)  # mam2 177 , glm1 130,
b_filter = cv2.bitwise_and(min_b, max_b)
# cv2.namedWindow("red filter", cv2.WINDOW_NORMAL)
# cv2.imshow("red filter", b_filter)

intr_img = cv2.bitwise_and(L_filter, a_filter,)
final_img = cv2.bitwise_and(intr_img, b_filter)
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
