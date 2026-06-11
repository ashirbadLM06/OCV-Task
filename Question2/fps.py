import cv2
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")

print("Webcam System")
print("Press 's' to save an image.")
print("Press 'q' to quit.")

img_counter = 0
pTime = 0
cTime = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    cTime = time.time()
    timeDiff = cTime - pTime
    fps = 1 / timeDiff
    pTime = cTime
    fps_text = f"FPS: {fps:.0f}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)


    cv2.imshow('Webcam Feed', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        img_name = f"opencv_frame_{img_counter}.png"
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")
        img_counter += 1

    elif key == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()