# PowerShell 배포용 실행 파일 빌드 스크립트

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "본사 정산서 자동화 프로그램 빌드" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 가상 환경 확인
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "가상 환경이 없습니다. 생성 중..." -ForegroundColor Yellow
    python -m venv .venv
}

# PowerShell 실행 정책 확인 및 설정
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Host "PowerShell 실행 정책이 Restricted입니다. 현재 세션에만 Bypass로 설정합니다..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
}

# 가상 환경 활성화
Write-Host "가상 환경 활성화 중..." -ForegroundColor Green
& ".venv\Scripts\Activate.ps1"

# 의존성 설치
Write-Host "의존성 설치 중..." -ForegroundColor Green
pip install -r requirements.txt

# 이전 빌드 결과물 삭제
if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force
}
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force
}

# PyInstaller로 빌드
Write-Host ""
Write-Host "실행 파일 빌드 중..." -ForegroundColor Green
pyinstaller build_exe.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Green
    Write-Host "빌드 완료!" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Green
    Write-Host "실행 파일 위치: dist\쿠팡 정산서 프로그램(v1.0).exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "배포 시 다음 파일들을 함께 배포하세요:" -ForegroundColor Yellow
    Write-Host "- dist\쿠팡 정산서 프로그램(v1.0).exe" -ForegroundColor Yellow
    Write-Host "- config 폴더 (config.json, mapping.json 포함)" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Red
    Write-Host "빌드 실패!" -ForegroundColor Red
    Write-Host "====================================" -ForegroundColor Red
    exit 1
}

Read-Host "Press Enter to continue"

