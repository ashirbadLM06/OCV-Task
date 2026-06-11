import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

PINCH_THRESHOLD = 40

print("--- Instant Response Hand Gestures LED System ---")
print("Pinch fingers to turn LED ON (Green). Release to turn LED OFF (Red).")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h,w,c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    led_on = False
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_px = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_px = (int(index_tip.x * w), int(index_tip.y * h))

            distance_px = math.hypot(thumb_px[0] - index_px[0], thumb_px[1] - index_px[1])

            cv2.circle(frame, thumb_px, 6, (255, 255, 0), -1)
            cv2.circle(frame, index_px, 6, (255, 255, 0), -1)
            cv2.line(frame, thumb_px, index_px, (255, 255, 255), 1)

            mid_point = ((thumb_px[0] + index_px[0]) // 2, (thumb_px[1] + index_px[1]) // 2 - 10)
            cv2.putText(frame, f"{int(distance_px)} px", mid_point,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1,cv2.LINE_AA )

            if distance_px < PINCH_THRESHOLD:
                led_on = True
    led_center = (w - 60, 60)
    led_radius = 25

    if led_on:
        led_color = (0, 255, 0)
        status_text = "LED: ON"
    else:
        led_color = (0, 0, 255)
        status_text = "LED: OFF"

    cv2.circle(frame, led_center, led_radius, led_color, -1)
    cv2.circle(frame, led_center, led_radius + 2, (255, 255, 255), 2)
    cv2.putText(frame, status_text, (w - 110, 110), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Gesture Controlled LED", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
