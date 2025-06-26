from tensorflow.keras.models import load_model # type: ignore
import cv2
import numpy as np

# Load your trained model
model = load_model("Model/your_model.h5")  # update filename if needed

# Define your gesture labels
labels = ["A", "B", "C", "D", "E"]  # replace with your actual labels

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize and preprocess
    img = cv2.resize(frame, (224, 224))  # change size if needed
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Make prediction
    prediction = model.predict(img)
    index = np.argmax(prediction)
    class_name = labels[index]
    confidence = prediction[0][index]

    # Display result
    cv2.putText(frame, f"{class_name} ({confidence:.2f})", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()