import cv2
from ultralytics import YOLO

# YOLOv8n 모델 로드 (PyTorch)
model = YOLO('yolov8n.pt')

# 카메라 열기
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 모델 추론
    results = model(frame, verbose=False)[0]

    person_count = 0
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if model.names[cls_id] == "person" and conf > 0.4:
            person_count += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"person {conf:.2f}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    # 혼잡도 출력
    cv2.putText(frame, f"People: {person_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("YOLOv8n Person Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
