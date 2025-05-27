import cv2
from ultralytics import YOLO  # YOLOv8

model = YOLO('yolov8n.pt')  # 초경량 모델 (YOLOv8n)

cap = cv2.VideoCapture(10)  # Pi 카메라

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if model.names[cls] == "person":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, "person", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    cv2.imshow("YOLO Person Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
