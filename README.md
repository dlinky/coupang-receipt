# 본사 정산서 자동화 프로그램

본사 정산서 엑셀 파일의 데이터를 지점 정산서 양식에 자동으로 매핑하여 입력하는 데스크톱 애플리케이션입니다.

## 기술 스택

- Python 3.11+
- PySide6 (GUI 프레임워크)
- openpyxl (엑셀 파일 처리)
- pytest (테스트)

## 설치

1. Python 3.11 이상이 설치되어 있어야 합니다.

2. 가상 환경 생성 및 활성화:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 실행

```bash
python src/main.py
```

## 프로젝트 구조

```
src/
├── models/          # 데이터 모델
├── services/        # 비즈니스 로직
├── gui/            # GUI 컴포넌트
└── utils/          # 유틸리티 함수

tests/
├── unit/           # 단위 테스트
├── integration/    # 통합 테스트
└── contract/       # 계약 테스트

config/
├── config.json     # 애플리케이션 설정
└── mapping.json    # 매핑 규칙 설정
```

## 사용 방법

1. 본사 정산서 파일 선택 (비밀번호 입력 필요 시)
2. 지점 정산서 파일 선택 (또는 자동 생성)
3. 주차 선택 (1~5주차 또는 전체)
4. "데이터 매핑 실행" 버튼 클릭

자세한 사용 방법은 `specs/1-settlement-automation/quickstart.md`를 참조하세요.

## 테스트

```bash
pytest
```

코드 커버리지 확인:
```bash
pytest --cov=src --cov-report=html
```

## Windows 실행 파일 빌드

Windows에서 실행 파일(.exe)로 배포하려면:

1. Windows 환경에서 다음 명령어 실행:
```bash
build.bat
```

2. 빌드 완료 후 `dist` 폴더에 `쿠팡 정산서 프로그램(v1.0).exe` 파일이 생성됩니다.

3. 배포 시 다음 파일들을 함께 배포하세요:
   - `dist/쿠팡 정산서 프로그램(v1.0).exe`
   - `config` 폴더 전체 (config.json, mapping.json 포함)

### 수동 빌드

PyInstaller를 직접 사용하려면:
```bash
pip install pyinstaller
pyinstaller build_exe.spec
```

### 빌드 옵션 수정

`build_exe.spec` 파일을 수정하여 빌드 옵션을 변경할 수 있습니다:
- `name`: 실행 파일 이름
- `icon`: 아이콘 파일 경로 (선택사항)
- `console`: 콘솔 창 표시 여부 (False = GUI만 표시)

## 라이선스

이 프로젝트는 내부 사용을 위한 것입니다.

