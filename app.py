import cv2
from ultralytics import YOLO
import time
from collections import Counter

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

prev_time = 0

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera frame not received")
        break

    # Object detection
    results = model(frame, conf=0.5, verbose=False)

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    # Count detected objects
    detected_objects = []

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        object_name = model.names[class_id]
        detected_objects.append(object_name)

    # Count each object category
    object_counts = Counter(detected_objects)

    # Total object count
    total_objects = len(detected_objects)

    # Calculate FPS
    current_time = time.time()

    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0

    prev_time = current_time

    # Display FPS
    cv2.putText(
        annotated_frame,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Display total objects
    cv2.putText(
        annotated_frame,
        f"Total Objects: {total_objects}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Display individual object counts
    y_position = 110

    for name, count in object_counts.items():

        text = f"{name}: {count}"

        cv2.putText(
            annotated_frame,
            text,
            (20, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        y_position += 30

    # Show final output
    cv2.imshow(
        "YOLOv8 Real-Time Object Detection",
        annotated_frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()