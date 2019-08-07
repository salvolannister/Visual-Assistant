import imutils
import cv2
import json
import threading
import numpy as np

from pyimagesearch.shapedetector import ShapeDetector
from SimpleWebSocketServer import SimpleExampleServer, WebSocket
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

capture = cv2.VideoCapture(0)
clients = []
server = None

class SimpleWSServer(WebSocket):
    def handleConnected(self):
        clients.append(self)

    def handleClose(self):
        clients.remove(self)

def run_server():
    global server
    server = SimpleWebSocketServer('', 9000, SimpleWSServer,
                                   selectInterval=(1000.0 / 15) / 1000)
    server.serveforever()

t = threading.Thread(target=run_server)
t.start()

while True:
    ret, image = capture.read()



    # Apply filters
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.medianBlur(grey, 15)


    cv2.imshow('Image previews', image)

    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    #thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    canny = cv2.Canny(blurred, 80, 180, 3)

    cv2.imshow("canny", canny)

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
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)

        shape = sd.detect(c)
        print(shape)
        if shape == "rectangle":
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)

        # show the output image
        cv2.imshow("Image", image)
    #questo non credo funzioni
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


