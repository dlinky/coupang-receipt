@echo off
REM Windows 배포용 실행 파일 빌드 스크립트

echo ====================================
echo 본사 정산서 자동화 프로그램 빌드
echo ====================================
echo.

REM 가상 환경 확인
if not exist ".venv\Scripts\activate.bat" (
    echo 가상 환경이 없습니다. 생성 중...
    python -m venv .venv
)

REM 가상 환경 활성화
call .venv\Scripts\activate.bat

REM 의존성 설치
echo 의존성 설치 중...
pip install -r requirements.txt

REM 이전 빌드 결과물 삭제
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM PyInstaller로 빌드
echo.
echo 실행 파일 빌드 중...
pyinstaller build_exe.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo 빌드 완료!
    echo ====================================
    echo 실행 파일 위치: dist\쿠팡 정산서 프로그램(v1.1).exe
    echo.
    echo 배포 시 다음 파일들을 함께 배포하세요:
    echo - dist\쿠팡 정산서 프로그램(v1.1).exe
    echo - config 폴더 (config.json, mapping.json 포함)
    echo.
) else (
    echo.
    echo ====================================
    echo 빌드 실패!
    echo ====================================
    exit /b 1
)

pause

