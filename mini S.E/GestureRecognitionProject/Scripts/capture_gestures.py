import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import os  # To handle folder creation



cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300
counter = 0

# New folder path for saving images
folder = "output"

# Check if the folder exists, if not, create it
if not os.path.exists(folder):
    os.makedirs(folder)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Ensure the crop stays within image bounds
        y1, y2 = max(0, y - offset), min(img.shape[0], y + h + offset)
        x1, x2 = max(0, x - offset), min(img.shape[1], x + w + offset)

        imgCrop = img[y1:y2, x1:x2]

        # Check if the cropped image is valid
        if imgCrop.size == 0:
            print("Warning: Empty image crop, skipping frame.")
            continue

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap: wCal + wGap] = imgResize

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap: hCal + hGap, :] = imgResize

        cv2.imshow('ImageCrop', imgCrop)
        cv2.imshow('ImageWhite', imgWhite)

    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        # Save the image with the current timestamp
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(f"Image {counter} saved!")
    elif key == ord("q"):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
