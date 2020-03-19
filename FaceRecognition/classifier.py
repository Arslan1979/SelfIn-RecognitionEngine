import numpy as np
import os
import cv2
from PIL import Image

def trainClassifier(dataDir):
    path = [os.path.join(dataDir, f) for f in os.listdir(dataDir)]
    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)

    
    classifier = cv2.face_LBPHFaceRecognizer.create()
    classifier.train(faces, ids)
    classifier.write("classifier.yml")

trainClassifier('FaceRecognition/Data')


