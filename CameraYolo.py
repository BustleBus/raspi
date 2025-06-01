import cv2
import requests
from ultralytics import YOLO
import time

# YOLOv8n 모델 로드
model = YOLO('yolov8n.pt')

# 1) 카메라 열기 (해상도를 낮춰서 줌인 현상 완화)
cap = cv2.VideoCapture(10)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 2) 성능 측정용 FPS 카운터
prev_time = time.time()
frame_count = 0

# POST 요청을 보낼 서버 주소
POST_URL = 'https://bustlebus.duckdns.org/api/v1/person-count'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # (옵션) 모델 입력용으로 프레임을 더 작게 리사이즈
    small = cv2.resize(frame, (320, 320))
    # YOLO 추론 (imgsz=320으로 내부 리사이즈)
    results = model(small, imgsz=320, conf=0.4, verbose=False)[0]

    person_count = 0
    # small(320×320) 기준 좌표를 원본(640×480)으로 스케일
    h_ratio = frame.shape[0] / 320
    w_ratio = frame.shape[1] / 320

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if model.names[cls_id] == "person" and conf > 0.4:
            x1, y1, x2, y2 = box.xyxy[0]
            x1 = int(x1 * w_ratio)
            y1 = int(y1 * h_ratio)
            x2 = int(x2 * w_ratio)
            y2 = int(y2 * h_ratio)

            person_count += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{conf:.2f}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 혼잡도(인원수) 출력
    cv2.putText(frame, f"People: {person_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # ✅ 서버로 POST 요청 (타임아웃: 1초)
    try:
        payload = {'person_count': person_count}
        headers = {'Content-Type': 'application/json'}
        requests.post(POST_URL, json=payload, headers=headers, timeout=1)
    except requests.exceptions.RequestException as e:
        print(f"[!] POST Error: {e}")

    # 3) 디스플레이용 창 크기 축소 (예: 640×480 → 480×360)
    disp = cv2.resize(frame, (480, 360))
    cv2.imshow("YOLOv8n Person Detection", disp)

    frame_count += 1
    # FPS 계산 (30프레임마다 출력)
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
