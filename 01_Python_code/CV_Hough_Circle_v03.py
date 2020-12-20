import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# mpl.use('Qt5Agg')

img = cv2.imread('/Users/khetamdouba/PycharmProjects/Pyserial_test/fromCamera/DSC_0205.JPG', 1)  #type: np.ndarray
print(img.shape, img.size, img.ndim, img.dtype)
# rimg = np.rot90(img, k=-1)
# cimg = rimg[1150:1750, 1700:1900]
cimg = img
plt.imshow(cimg)
plt.show()

# cv2.namedWindow("window", cv2.WINDOW_NORMAL)
# cv2.imshow('window', cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cimg = cv2.medianBlur(cimg, 5)
gcimg = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
# circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 1)
cimg = cv2.cvtColor(gcimg, cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(gcimg, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=0, maxRadius=0)
if circles is not None:
    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 5)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 6)

print(circles)
cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.imshow('window', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.imshow(cimg)
# plt.show()
