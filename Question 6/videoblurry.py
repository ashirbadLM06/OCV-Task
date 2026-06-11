import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

kernel_size = 5

print("Blur & Canny Edge Detector")
print("Press 'w' to INCREASE blur (softer edges)")
print("Press 's' to DECREASE blur (sharper edges)")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blurred, 50, 150)
    cv2.putText(edges, f"Kernel Size: {kernel_size}x{kernel_size}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


    cv2.imshow("Dynamic Canny Edges", edges)


    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'):
        kernel_size += 2
        print(f"Increased blur kernel to: {kernel_size}")
        if kernel_size >29:
            break

    elif key == ord('s'):
        if kernel_size > 1:
            kernel_size -= 2
            print(f"Decreased blur kernel to: {kernel_size}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()