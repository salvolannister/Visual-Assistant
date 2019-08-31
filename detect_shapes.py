import imutils
import cv2
import json
import threading
import numpy as np

from pyimagesearch.shapedetector import ShapeDetector
from SimpleWebSocketServer import  SimpleWebSocketServer,WebSocket

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better


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
                                   selectInterval=(1000.0 / 30) / 1000)
    server.serveforever()


t=threading.Thread(target=run_server)
t.start()

capture = cv2.VideoCapture(0)
print(capture.get(cv2.CAP_PROP_FPS))
kernel1 = np.ones((8, 8), np.uint8)
kernel2 = np.ones((2, 2), np.uint8)


while True:
    ret, image = capture.read()



    # Apply filters
    hls_img = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.medianBlur(hls_img, 15)
    lower_red = np.array([170, 70, 50])
    upper_red = np.array( [180, 255, 255])
    mask_0 = cv2.inRange(hls_img, lower_red, upper_red)

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hls_img, lower_red1, upper_red1)
    mask_red = mask_0 + mask_1
    res = cv2.bitwise_and(image, image, mask=mask_red)

    '''  
    cv2.imshow('Image previews', image)
    cv2.imshow('bit_wise', res)
    '''
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])


    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    r_hls_img = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    #blurred = cv2.GaussianBlur(resized, (3, 3), 0)
    mask_0 = cv2.inRange(r_hls_img, lower_red, upper_red)
    mask_1 = cv2.inRange(r_hls_img, lower_red1, upper_red1)
    mask_red = mask_0 + mask_1

    erosion = cv2.erode(mask_red, kernel2, iterations=1)
    dilatation =  cv2.dilate(erosion, kernel1,iterations = 1)
   # res = cv2.bitwise_and(dilatation, resized, mask=mask_red)
    #thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    canny = cv2.Canny(dilatation , 80, 180, 3)
    '''
    cv2.imshow('red mask', mask_red)
    cv2.imshow('erosion', erosion)
    cv2.imshow('dilatation', dilatation)
    cv2.imshow("canny", canny)
    cv2.imshow("bit wise", res) 
    '''
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
        #print(shape)
        if shape == "rectangle":

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            for client in clients:

                msg = json.dumps({'x': cX, 'y': cY})
                client.sendMessage(str(msg))
                print(str(msg) + " sent")

            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)

        # show the output image
        #cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

server.close()
