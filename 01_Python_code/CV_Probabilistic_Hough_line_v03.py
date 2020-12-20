import cv2
import numpy as np

# Read image as coloured.
img = cv2.imread('fromCamera/Feature_detection/canny_1C.png')

# Convert colour space to grey.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find edges.
edges = cv2.Canny(gray, 254, 255)

# probabilistic Hough line transform.
lines = cv2.HoughLinesP(edges, 1, np.pi / 720, 5, 10, 5)

# Draw probabilistic Hough lines.
for x1, y1, x2, y2 in lines[:, 0]:
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# display function.
cv2.namedWindow('P_Hough', cv2.WINDOW_NORMAL)
cv2.imshow('P_Hough', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
