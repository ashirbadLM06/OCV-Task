import cv2
import mediapipe as mp
import numpy as np

WIDTH, HEIGHT = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# Create canvas directly using the known dimensions
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)
prev_x, prev_y = 0, 0

print(" Hand Tracking Controls ")
print("1 Finger (Index Up)             -> Write (Blue)")
print("3 Fingers (Index, Middle, Ring) -> Erase")
print("Press 'S'                       -> Save Canvas as PNG")
print("Press 'C'                       -> Clear Canvas")
print("Press 'Q'                       -> Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h,w,c = frame.shape
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Check if a hand is detected
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        ix = int(landmarks[8].x * w)
        iy = int(landmarks[8].y * h)

        # Check finger states
        index_up = landmarks[8].y < landmarks[6].y
        middle_up = landmarks[12].y < landmarks[10].y
        ring_up = landmarks[16].y < landmarks[14].y
        pinky_up = landmarks[20].y < landmarks[18].y

        # WRITING (Only Index finger is up)
        if index_up and not middle_up and not ring_up and not pinky_up:
            cv2.circle(frame, (ix, iy), 8, (255, 0, 0), -1)
            cv2.putText(frame,f'Drawing Mode',(15,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy

            cv2.line(canvas, (prev_x, prev_y), (ix, iy), (255, 0, 0), thickness=5)
            prev_x, prev_y = ix, iy

        # ERASING (Three fingers: Index, Middle, and Ring are up)
        elif index_up and middle_up and ring_up:
            cv2.circle(frame, (ix, iy), 20, (255, 255, 255), 2)
            cv2.putText(frame, f'Erasing Mode', (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy
            cv2.line(canvas, (prev_x, prev_y), (ix, iy), (0, 0, 0), thickness=60)
            prev_x, prev_y = ix, iy

        #  HOVERING / NAVIGATING
        else:
            prev_x, prev_y = 0, 0
            cv2.circle(frame, (ix, iy), 5, (0, 255, 0), -1)
            cv2.putText(frame, f'Hovering Mode', (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        prev_x, prev_y = 0, 0

    # Convert canvas to grayscale and threshold it to find where the ink is
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, ink_mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY)

    # Paste the canvas ink directly onto the live camera frame
    frame[ink_mask == 255] = canvas[ink_mask == 255]

    # Display the final application window
    cv2.imshow("Virtual Drawing Board", frame)

    key = cv2.waitKey(1) & 0xFF

    # Save current sketch as a PNG file with a clean white background
    if key == ord("s"):
        white_background = np.ones_like(canvas) * 255
        white_background[ink_mask == 255] = canvas[ink_mask == 255]
        cv2.imwrite("finger_sketch.png", white_background)
        print("Canvas successfully saved as 'finger_sketch.png'!")

    # Clear the entire board
    elif key == ord("c"):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        print("Canvas cleared.")

    # Exit program
    elif key == ord("q") or key == 27:
        break

cap.release()
cv2.destroyAllWindows()