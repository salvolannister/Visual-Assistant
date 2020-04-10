from typing import Any, Union

import cv2
import math

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # c stay for contour
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        #skips small or non convex object
        if math.fabs(cv2.contourArea(c) < 100 or not (cv2.isContourConvex(approx))):
            return shape

        if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            area = cv2.contourArea(c);
            # x , y top left
            e = 0.10;
            b1 = b2 = 0;
            if (abs(x - w) < 0.10):
                b1 = x;
                b2 = w;

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        return shape
