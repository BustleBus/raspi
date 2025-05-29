# 🎯 Raspberry Pi 5 → YOLO 실시간 객체 감지 프로젝트

라즈베리파이5와 Pi Camera를 이용해 YOLO 모델로 실시간 객체(예: 사람) 감지를 수행하는 프로젝트입니다.  
이 문서는 설치, 가상환경 실행, Pi Camera 설정 및 YOLO 실행 방법을 정리한 실행 가이드입니다.

---

## ✅ 1. Python 가상환경 실행

```bash
source yolo-env/bin/activate
# yolo-env: 너가 만든 Python 가상환경 디렉터리 이름 (예: YOLO 설치할 때 만든 환경)
# bin/activate: 가상환경을 활성화시키는 스크립트
#source: 그 스크립트를 현재 셸에서 실행하라는 명령어 (bash/zsh 등에서 사용)
