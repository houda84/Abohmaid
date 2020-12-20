import cv2
import numpy as np

# Read image as coloured.
img = cv2.imread('fromCamera/Feature_detection/canny_1C.png')

# Convert colour space to grey.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find edges.
edges = cv2.Canny(gray, 250, 255)

# Standard Hough line transform.
lines = cv2.HoughLines(edges, 1, np.pi / 45, 50)

# Draw standard Hough lines.
for rho, theta in lines[:, 0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

# display function.
cv2.namedWindow('S_Hough', cv2.WINDOW_NORMAL)
cv2.imshow('S_Hough', img)
cv2.waitKey(0)
cv2.destroyAllWindows()