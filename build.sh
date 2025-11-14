#!/bin/bash
# macOS/Linux 배포용 실행 파일 빌드 스크립트 (테스트용)

echo "===================================="
echo "본사 정산서 자동화 프로그램 빌드"
echo "===================================="
echo ""

# 가상 환경 확인
if [ ! -d ".venv" ]; then
    echo "가상 환경이 없습니다. 생성 중..."
    python3 -m venv .venv
fi

# 가상 환경 활성화
source .venv/bin/activate

# 의존성 설치
echo "의존성 설치 중..."
pip install -r requirements.txt

# 이전 빌드 결과물 삭제
rm -rf dist build

# PyInstaller로 빌드
echo ""
echo "실행 파일 빌드 중..."
pyinstaller build_exe.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "===================================="
    echo "빌드 완료!"
    echo "===================================="
    echo "실행 파일 위치: dist/쿠팡 정산서 프로그램(v1.0)"
    echo ""
    echo "배포 시 다음 파일들을 함께 배포하세요:"
    echo "- dist/쿠팡 정산서 프로그램(v1.0)"
    echo "- config 폴더 (config.json, mapping.json 포함)"
    echo ""
else
    echo ""
    echo "===================================="
    echo "빌드 실패!"
    echo "===================================="
    exit 1
fi

