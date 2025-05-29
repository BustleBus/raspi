# raspi

라즈베리파이5 -> Yolo 

1. 가상 환경 실행
    source yolo-env/bin/activate // Python 가상환경(virtual environment)을 활성화
    
    yolo-env: 너가 만든 Python 가상환경 디렉터리 이름 (예: YOLO 설치할 때 만든 환경)
    
    bin/activate: 가상환경을 활성화시키는 스크립트
    
    source: 그 스크립트를 현재 셸에서 실행하라는 명령어 (bash/zsh 등에서 사용)

2. 터미널 2개 활성화
    2-1) 라즈베리파이의 카메라 영상을 실시간으로 녹화하는 명령어
         libcamera-vid -t 0 --width 1280 --height 720 --framerate 60 -o test.h264
    2-2) Yolo 활성화
         python (프로그램명)

