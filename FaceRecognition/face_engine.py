import cv2
import numpy as np
import os
from pathlib import Path, WindowsPath, PureWindowsPath

def drawBoundary(image, classifier, scaleFactor, minNeighbors, colour, text):
    #convert video stream to gray
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(grayImage, scaleFactor, minNeighbors)
    #coordinates of the binding box
    coordinates = []

    # (x,y) represents top left corner of binding box
    # h is the max height & w is the max width
    # therefore (h,w) represents bottom right corner of binding box
    for (x, y, h, w) in features:
        cv2.rectangle(image, (x, y), (x+w, y+h), colour, 2)
        cv2.putText(image, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 1, cv2.LINE_AA)
        coordinates = [x, y, w, h]
    
    return coordinates

def detect(image, faceClassifier, eyeClassifier):
    colour = {
        "blue" : (255,0,0),
        "red" : (0,0,255),
        "green" : (0,255,0),
        "white" : (255, 255, 255)
    }

    coordinates = drawBoundary(image, faceClassifier, 1.1, 10, colour['blue'], "Face")
    
    if len(coordinates) == 4:
        croppedFaceImage = image[coordinates[1]:coordinates[1] + coordinates[3], coordinates[0]: coordinates[0] + coordinates[2]]
        coordinates = drawBoundary(croppedFaceImage, eyeClassifier, 1.1, 14, colour['red'], "Eyes")

    return image



faceClassifier = cv2.CascadeClassifier('FaceRecognition/Classifiers/face.xml')
eyeClassifier = cv2.CascadeClassifier('FaceRecognition/Classifiers/eye.xml')



#webcam footage feed
videoStream = cv2.VideoCapture(0)

while True:
    #Setup of and stream and window creation
    _, image = videoStream.read()
    image = detect(image, faceClassifier, eyeClassifier)
    cv2.imshow("face detection", image)

    #How to terminate video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#releases webcam and closes video stream window
videoStream.release()
cv2.destroyAllWindows()