import cv2
from ultralytics import YOLO
import time

# YOLOv8n 모델 로드 (PyTorch)
model = YOLO('yolov8n.pt')  # 이미 yolov8n이라 가볍긴 하지만, 이하로 처리량을 더 줄일 수 있음

# 1) 카메라 열기 (해상도를 낮춰서 줌인 현상 완화)
cap = cv2.VideoCapture(10)  # 문자열로 경로 지정
# 원래 1280×720이었는데 너무 “줌”돼서 보이니 640×480으로 낮춤
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 2) 성능 측정용 FPS 카운터
prev_time = time.time()
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # (옵션) 모델 입력용으로 프레임을 더 작게 리사이즈해도 되고, 원본(640×480) 그대로 넣어도 됨.
    # 아래는 모델 입력을 320×320으로 줄여서 속도 올리는 예시:
    small = cv2.resize(frame, (320, 320))  # 모델 성능을 위해 짧은 사이즈로 줄임
    # 모델 추론 (imgsz=320 으로 지정하면 내부적으로도 320×320으로 리사이즈함)
    results = model(small, imgsz=320, conf=0.4, verbose=False)[0]

    person_count = 0
    # 결과 바운딩박스 좌표는 small(320×320) 기준이므로, 원본 frame(640×480) 크기로 스케일업해야 함
    h_ratio = frame.shape[0] / 320  # 세로 스케일 비율
    w_ratio = frame.shape[1] / 320  # 가로 스케일 비율

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if model.names[cls_id] == "person":
            # 바운딩박스 좌표 가져와서 원본 크기로 스케일
            x1, y1, x2, y2 = box.xyxy[0]
            x1 = int(x1 * w_ratio)
            y1 = int(y1 * h_ratio)
            x2 = int(x2 * w_ratio)
            y2 = int(y2 * h_ratio)

            if conf > 0.4:
                person_count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"person {conf:.2f}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 혼잡도(인원수) 출력
    cv2.putText(frame, f"People: {person_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 3) 디스플레이용 창 크기도 더 작게 축소해서 보여주기 (예: 640×480 → 480×360)
    disp = cv2.resize(frame, (480, 360))
    cv2.imshow("YOLOv8n Person Detection", disp)

    frame_count += 1
    # FPS 계산 (선택)
    if frame_count >= 30:
        now = time.time()
        fps = frame_count / (now - prev_time)
        prev_time = now
        frame_count = 0
        print(f"≈ FPS: {fps:.1f}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
