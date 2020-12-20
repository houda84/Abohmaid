import cv2
# Read image as gray by
img = cv2.imread('fromCamera/Feature_detection/canny_1C.png', 0)
# Canny detector with min and max threshold
edges = cv2.Canny(img, 254, 255)
# Display function
cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
cv2.imshow('Canny', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
