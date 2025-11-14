# Research: 본사 정산서 자동화 프로그램

**Date**: 2025-11-14  
**Feature**: 본사 정산서 자동화 프로그램

## 기술 선택 및 의사결정

### 1. 엑셀 파일 처리 라이브러리 선택

**Decision**: openpyxl 사용

**Rationale**:
- 비밀번호 보호된 엑셀 파일 지원 (xlwings는 Windows COM에 의존)
- 크로스 플랫폼 지원 (Windows, macOS, Linux)
- 병합 셀 처리 기능 제공
- 순수 Python 라이브러리로 의존성 최소화
- 활발한 커뮤니티 및 문서화

**Alternatives considered**:
- **xlwings**: Windows에서만 완전히 작동하며 COM 의존성으로 크로스 플랫폼 지원 제한
- **pandas**: 엑셀 읽기/쓰기는 가능하나 비밀번호 보호 파일 지원 제한적
- **xlsxwriter**: 쓰기 전용으로 읽기 기능 없음

### 2. GUI 프레임워크 선택

**Decision**: PySide6 사용

**Rationale**:
- Qt 기반으로 크로스 플랫폼 네이티브 UI 제공
- Python 표준 GUI 라이브러리 (tkinter)보다 현대적이고 기능이 풍부
- 비동기 작업 처리 지원 (QThread, QTimer)
- 테이블 뷰, 파일 다이얼로그 등 필요한 위젯 제공
- LGPL 라이선스로 상업적 사용 가능

**Alternatives considered**:
- **tkinter**: Python 표준 라이브러리이지만 UI가 구식이고 기능 제한적
- **PyQt6**: PySide6과 유사하나 GPL 라이선스로 상업적 사용 시 라이선스 비용 발생
- **Kivy**: 모바일 중심으로 데스크톱 UI가 네이티브하지 않음

### 3. 매핑 설정 저장 형식

**Decision**: JSON 형식 사용

**Rationale**:
- Python 표준 라이브러리(json)로 추가 의존성 불필요
- 사람이 읽고 수정하기 쉬운 형식
- 구조화된 데이터 표현에 적합
- YAML보다 파싱이 빠르고 표준 라이브러리 지원

**Alternatives considered**:
- **YAML**: 가독성은 좋으나 추가 의존성(pyyaml) 필요
- **XML**: 과도하게 복잡하고 가독성 낮음
- **INI**: 중첩 구조 표현에 부적합

### 4. 테스트 프레임워크

**Decision**: pytest 사용

**Rationale**:
- Python 표준 테스트 프레임워크
- 풍부한 fixture 지원
- 커버리지 측정 도구(coverage.py)와 통합 용이
- 명확한 테스트 구조 및 어설션

**Alternatives considered**:
- **unittest**: 표준 라이브러리이지만 pytest보다 기능 제한적
- **nose2**: 유지보수가 중단된 상태

### 5. 비동기 처리 전략

**Decision**: QThread를 사용한 백그라운드 작업 처리

**Rationale**:
- PySide6의 QThread는 GUI 응답성을 유지하면서 장시간 작업 처리 가능
- 진행 상태 업데이트를 위한 시그널/슬롯 메커니즘 제공
- 파일 처리 작업이 30초~3분 소요되므로 UI 블로킹 방지 필수

**Alternatives considered**:
- **asyncio**: GUI 이벤트 루프와 충돌 가능성
- **threading**: QThread가 Qt 통합에 더 적합

### 6. 병합 셀 처리 전략

**Decision**: openpyxl의 merged_cells 속성 활용

**Rationale**:
- openpyxl이 병합 셀 정보를 자동으로 제공
- 병합 영역의 첫 번째 셀 좌표를 쉽게 얻을 수 있음
- 셀 범위 문자열 파싱 후 병합 여부 확인

**Implementation approach**:
1. 대상 셀 범위 파싱 (예: "C6")
2. 워크시트의 merged_cells 속성 확인
3. 병합 영역에 포함된 경우 첫 번째 셀 좌표 반환
4. 해당 셀에 값 입력

### 7. 날짜 계산 로직

**Decision**: Python의 datetime 모듈 사용

**Rationale**:
- 표준 라이브러리로 추가 의존성 불필요
- 주차 기반 날짜 계산에 충분한 기능 제공
- relativedelta (dateutil)는 과도한 의존성

**Implementation approach**:
- 주차 정보(1-5)를 기반으로 해당 월의 첫 번째 주차 시작일 계산
- 전주 수요일 ~ 해당주 화요일 범위 계산
- 해당 주차의 금요일 날짜 계산
- YY.MM.DD 형식으로 포맷팅

### 8. 에러 처리 전략

**Decision**: 사용자 친화적 메시지 + 로그 파일

**Rationale**:
- 비기술 사용자를 위한 명확한 에러 메시지
- 디버깅을 위한 상세 로그 파일
- 매핑 오류 시 매핑 파일을 메모장으로 자동 열기

**Error categories**:
1. 파일 오류: 비밀번호 오류, 파일 없음, 형식 오류
2. 매핑 오류: 시트 없음, 셀 범위 오류 → 매핑 파일 열기
3. 데이터 오류: 형식 불일치, 파싱 실패
4. 시스템 오류: 메모리 부족, 권한 오류

### 9. 설정 파일 관리

**Decision**: config.json과 mapping.json 분리

**Rationale**:
- config.json: 애플리케이션 설정 (비밀번호, 오프셋 등)
- mapping.json: 매핑 규칙 (사용자가 자주 수정)
- 분리로 인한 명확한 책임 분리

**Config structure**:
```json
{
  "default_password": "4880403942",
  "week_offsets": {
    "1": 0,
    "2": 36,
    "3": 72,
    "4": 108,
    "5": 144
  }
}
```

### 10. 확장 가능한 계산 방식 설계

**Decision**: Strategy 패턴 사용

**Rationale**:
- 새로운 계산 방식을 코드 수정 없이 추가 가능
- 각 계산 방식이 독립적으로 테스트 가능
- 매핑 설정에서 계산 방식 이름으로 선택

**Calculation types**:
- simple_copy: 단순 복사
- conditional_copy: 조건부 복사 (프로모션)
- date_calculation: 날짜 계산
- unique_extraction: 고유값 추출 (월간정산)

## 성능 고려사항

### 파일 처리 최적화
- 엑셀 파일을 메모리에 한 번만 로드
- 필요한 시트만 열기
- 대량 데이터 처리 시 청크 단위 처리 고려 (현재는 50행 이하로 불필요)

### GUI 응답성
- 파일 처리 작업을 QThread에서 실행
- 진행 상태를 시그널로 전달하여 UI 업데이트
- 취소 기능 제공 (필요 시)

## 보안 고려사항

### 비밀번호 처리
- 비밀번호를 평문으로 저장하지 않음 (사용자 입력 또는 기본값)
- 메모리에서 비밀번호 제거 (가능한 경우)
- 설정 파일에 비밀번호 저장 시 경고 표시

## 호환성 고려사항

### 엑셀 파일 형식
- .xlsx 형식 지원 (openpyxl 기본)
- .xls 형식은 지원하지 않음 (xlrd 의존성 추가 필요하나 사용 빈도 낮음)

### Python 버전
- Python 3.11+ 요구 (타입 힌팅 및 최신 기능 활용)
- 하위 호환성은 필요 시 고려

## 미래 확장 가능성

### 추가 기능 고려
- 매핑 규칙 버전 관리
- 매핑 규칙 템플릿 저장/로드
- 배치 처리 (여러 파일 일괄 처리)
- 로그 파일 뷰어

### 기술적 개선
- 매핑 규칙 검증 도구
- 자동 테스트 생성
- 성능 프로파일링 도구

