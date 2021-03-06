import json
import imutils
import cv2
import numpy as np
# added to put object in JSON
from shapedetector import ShapeDetector

image = cv2.imread("prova.jpg")
#w = 640
img_height, img_width, depth = image.shape
print(str(img_height) + " " + str(img_width) + " " + str(depth))
"""
scale = w / img_width
h = scale * img_height
"""
lower_red = np.array([170, 70, 50])
upper_red = np.array([180, 255, 255])

kernel1 = np.ones((8, 8), np.uint8)
kernel2 = np.ones((2, 2), np.uint8)
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
r_hls_img = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS);

mask_0 = cv2.inRange(r_hls_img, lower_red, upper_red)

mask_red = mask_0

erosion = cv2.erode(mask_red, kernel2, iterations=1)
dilatation = cv2.dilate(erosion, kernel1, iterations=1)
res = cv2.bitwise_and(resized, resized, mask=mask_red)
# thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
canny = cv2.Canny(dilatation, 80, 180, 3)

cv2.imshow('red mask', mask_red)
cv2.imshow('erosion', erosion)
cv2.imshow('dilatation', dilatation)
cv2.imshow("canny", canny)
cv2.imshow("bit wise", res)

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

# loop over the contours
for c in cnts:

    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    if M["m00"] == 0:
        M["m00"] = 1
    cX = int((M["m10"] / M["m00"])* ratio)
    cY = int((M["m01"] / M["m00"])* ratio)

    shape = sd.detect(c)
    # print(shape)
    if shape == "rectangle":
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        X = cX
        Y = cY
        msg = json.dumps({'x': X, 'y': Y})
        print(str(msg) + " sent")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (X, Y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey()
