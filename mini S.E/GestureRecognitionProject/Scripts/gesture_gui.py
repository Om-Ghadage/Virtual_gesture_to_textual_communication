# import tkinter as tk
# from tkinter import messagebox
# import cv2
# import numpy as np
# import math
# import os
# from cvzone.HandTrackingModule import HandDetector
# from cvzone.ClassificationModule import Classifier

# def start_recognition():
#     try:
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             raise Exception("Webcam not accessible. Check camera permissions or availability.")

#         detector = HandDetector(maxHands=1)
#         classifier = Classifier(
#             "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/Models/keras_model.h5",
#             "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/Models/labels.txt"
#         )

#         offset = 20
#         imgSize = 300

#         # Dynamically load labels from the "data" folder
#         data_path = "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/data"
#         labels = sorted(os.listdir(data_path))

#         while True:
#             success, img = cap.read()
#             if not success:
#                 raise Exception("Failed to read from webcam.")

#             imgOutput = img.copy()
#             hands, img = detector.findHands(img)

#             if hands:
#                 hand = hands[0]
#                 x, y, w, h = hand['bbox']
#                 imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
#                 imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

#                 if imgCrop.size == 0:
#                     continue

#                 aspectRatio = h / w
#                 if aspectRatio > 1:
#                     k = imgSize / h
#                     wCal = math.ceil(k * w)
#                     imgResize = cv2.resize(imgCrop, (wCal, imgSize))
#                     wGap = math.ceil((imgSize - wCal) / 2)
#                     imgWhite[:, wGap: wCal + wGap] = imgResize
#                 else:
#                     k = imgSize / w
#                     hCal = math.ceil(k * h)
#                     imgResize = cv2.resize(imgCrop, (imgSize, hCal))
#                     hGap = math.ceil((imgSize - hCal) / 2)
#                     imgWhite[hGap: hCal + hGap, :] = imgResize

#                 prediction, index = classifier.getPrediction(imgWhite, draw=False)

#                 # Ensure index doesn't go out of range
#                 label_text = labels[index] if index < len(labels) else "Unknown"

#                 cv2.rectangle(imgOutput, (x - offset, y - offset - 70), (x + 250, y - offset), (0, 255, 0), cv2.FILLED)
#                 cv2.putText(imgOutput, label_text, (x, y - 30),
#                             cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
#                 cv2.rectangle(imgOutput, (x - offset, y - offset),
#                               (x + w + offset, y + h + offset), (0, 255, 0), 4)

#             cv2.imshow("Gesture Recognition", imgOutput)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cap.release()
#         cv2.destroyAllWindows()

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # GUI Window
# root = tk.Tk()
# root.title("Gesture Recognition GUI")
# root.geometry("350x200")

# start_btn = tk.Button(root, text="Start Gesture Recognition", command=start_recognition,
#                       font=("Arial", 12), bg="green", fg="white", width=25)
# start_btn.pack(pady=20)

# exit_btn = tk.Button(root, text="Quit", command=root.destroy,
#                      font=("Arial", 12), bg="red", fg="white", width=25)
# exit_btn.pack(pady=10)

# root.mainloop()




import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import math
import os
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import time

def start_recognition():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Webcam not accessible. Check camera permissions or availability.")

        detector = HandDetector(maxHands=1)
        classifier = Classifier(
            "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/Models/keras_model.h5",
            "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/Models/labels.txt"
        )

        offset = 20
        imgSize = 300

        data_path = "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/data"
        labels = sorted(os.listdir(data_path))

        # Output directory setup
        output_path = "C:/Users/OM Ghadage/OneDrive/Desktop/mini S.E (1)/mini S.E/GestureRecognitionProject/output"
        os.makedirs(output_path, exist_ok=True)
        img_counter = 0

        while True:
            success, img = cap.read()
            if not success:
                raise Exception("Failed to read from webcam.")

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
                    imgWhite[:, wGap: wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap: hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                label_text = labels[index] if index < len(labels) else "Unknown"

                cv2.rectangle(imgOutput, (x - offset, y - offset - 70), (x + 250, y - offset), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgOutput, label_text, (x, y - 30),
                            cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                cv2.rectangle(imgOutput, (x - offset, y - offset),
                              (x + w + offset, y + h + offset), (0, 255, 0), 4)

            cv2.imshow("Gesture Recognition", imgOutput)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('s'):
                img_counter += 1
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                save_path = os.path.join(output_path, f"gesture_gui_output_{timestamp}.jpg")
                cv2.imwrite(save_path, imgOutput)
                print(f"Saved: {save_path}")
                messagebox.showinfo("Image Saved", f"GUI output saved:\n{save_path}")

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Window
root = tk.Tk()
root.title("Gesture Recognition GUI")
root.geometry("350x200")

start_btn = tk.Button(root, text="Start Gesture Recognition", command=start_recognition,
                      font=("Arial", 12), bg="green", fg="white", width=25)
start_btn.pack(pady=20)

exit_btn = tk.Button(root, text="Quit", command=root.destroy,
                     font=("Arial", 12), bg="red", fg="white", width=25)
exit_btn.pack(pady=10)

root.mainloop()
