import os
import logging
import cv2
import math
import numpy as np
import tensorflow as tf
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import absl.logging

# Suppress TensorFlow and absl warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
absl.logging.set_verbosity(absl.logging.ERROR)
absl.logging.set_stderrthreshold('error')

# Initialize webcam and model
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

classifier = Classifier(
    "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/Models/keras_model.h5",
    "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/Models/labels.txt"
)

offset = 20
imgSize = 300
labels = ["Hello", "I Love You", "Perfect", "Thank you", "Yes"]

while True:
    success, img = cap.read()
    if not success:
        break

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        if imgCrop.size == 0:
            continue

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap: wGap + wCal] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap: hGap + hCal, :] = imgResize

        prediction, index = classifier.getPrediction(imgWhite, draw=False)
        print(prediction, index)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 70), (x - offset + 400, y - offset - 10), (0, 255, 0), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

    cv2.imshow("Live Feed", imgOutput)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()