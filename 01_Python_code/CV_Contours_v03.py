import cv2
import numpy as np

# Read image as coloured.
image = cv2.imread('fromCamera/Feature_detection/canny_1C.png')

# Convert colour space to greyscale.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find edges (Optional) or,
edged = cv2.Canny(gray, 250, 255)

# Create Binary image filter.
ret, thresh = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY_INV)

# Find all contours.
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Find index of wire contour.
for i, k in enumerate(contours):
    txt = k.shape[0]
    if k.shape[0] > 100:
        print(i, txt)

# Make a copy of the image.
image_cont = image.copy()

# Draw wire contour only.
cv2.drawContours(image_cont, contours, 780, (0, 0, 255), 2)

# Display function.
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
cv2.imshow('Contours', image_cont)
cv2.waitKey(0)

# print(contours)
print("Number of Contours found = " + str(len(contours)))

# Calculate Convex hall from wire contour.
hull = cv2.convexHull(contours[780], False)

# Draw Convex hull function.
image_conv = image.copy()
cv2.drawContours(image_conv, [hull], 0, (0, 0, 255), 2)

# Draw Convex hull points.
hull_t = np.vstack(hull).squeeze()
for i in hull_t:
    cv2.drawMarker(image_conv,(i[0],i[1]),(0, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=15,thickness=2, line_type=cv2.LINE_AA)

# Display function.
cv2.namedWindow('Convex', cv2.WINDOW_NORMAL)
cv2.imshow('Convex', image_conv)
cv2.waitKey(0)

# Fit ellipse through Convex hull points.
ellipse = cv2.fitEllipse(hull)

# Draw ellipse.
cv2.ellipse(image, ellipse, (0, 255, 0), 2)

# Calculate Minimum enclosing circle.
(x, y), radius = cv2.minEnclosingCircle(hull)

# Draw circle.
center = (int(x), int(y))
radius = int(radius)
cv2.circle(image, center, radius, (0, 0, 255), 2)

# Calculate Minimum rotated rectangle.
rect = cv2.minAreaRect(hull)

# Draw rectangle.
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image, [box], 0, (255, 0, 0), 2)

# Display function
cv2.namedWindow('Ellipse fit', cv2.WINDOW_NORMAL)
cv2.imshow('Ellipse fit', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
