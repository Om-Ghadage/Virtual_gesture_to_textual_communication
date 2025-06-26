import cv2

cap = cv2.VideoCapture(0)  # Try 0, or 1 if needed

while True:
    success, img = cap.read()
    if not success:
        print("Failed to open webcam.")
        break

    cv2.imshow("Webcam Test", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()