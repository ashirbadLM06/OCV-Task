import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")

print("4-Quadrant Webcam")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break


    height, width,color = frame.shape
    half_width = width // 2
    half_height = height // 2
    small_frame = cv2.resize(frame, (half_width, half_height))

    top_left = small_frame

    top_right = cv2.flip(small_frame, 0)

    bottom_left = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)

    b,g,r= cv2.split(small_frame)
    zeros = np.zeros_like(r)
    bottom_right = cv2.merge([zeros, zeros, r])

    top_row = cv2.hconcat([top_left, top_right])
    bottom_row = cv2.hconcat([bottom_left, bottom_right])
    grid_window = cv2.vconcat([top_row, bottom_row])
    cv2.imshow('4-Quadrant Grid Feed', grid_window)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

