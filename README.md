# 🎯 Raspberry Pi 5 → YOLO 실시간 객체 감지 프로젝트

라즈베리파이 5와 Pi Camera를 이용해 **YOLO**로 실시간 객체(예: 사람) 감지를 수행하는 프로젝트입니다.  
이 문서는 **설치 → 가상환경 → 카메라 설정 → YOLO 실행** 순서로 필요한 모든 절차를 안내합니다.

---

## 1. Python 가상환경 실행

```bash
# 가상환경 생성(한 번만)
python3 -m venv yolo-env

# 가상환경 활성화(매번)
source yolo-env/bin/activate
```

| 용어             | 설명                               |
| -------------- | -------------------------------- |
| `yolo-env`     | YOLO 전용 Python 가상환경 디렉터리         |
| `bin/activate` | 가상환경을 현재 셸에 적용하는 스크립트            |
| `source`       | 스크립트를 현재 셸에서 실행하는 Linux/Bash 명령어 |

## 2. 터미널 2개로 실행하기

#### 3-1️⃣ Pi Camera 영상 녹화 (터미널 #1)
```bash
libcamera-vid -t 0 --width 1280 --height 720 --framerate 60 -o test.h264
```

| 옵션                 | 의미                 |
| ------------------ | ------------------ |
| `-t 0`             | 무한 시간 녹화           |
| `--width --height` | 1280×720 해상도       |
| `--framerate 60`   | 60 fps             |
| `-o test.h264`     | `test.h264` 파일로 저장 |

📹 실시간으로 Pi Camera 영상을 H.264 포맷으로 저장합니다.

#### 3-2️⃣ YOLO 실행 (터미널 #2)

```bash
# 같은 디렉터리에 CameraYolo.py가 있어야 합니다
python CameraYolo.py
```

CameraYolo.py 는 실시간 카메라 영상에서 person 클래스를 감지-표시하는 YOLO 코드입니다.
⚠️ 반드시 가상환경이 활성화된 상태에서 실행하세요.
