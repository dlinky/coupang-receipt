# Data Model: 본사 정산서 자동화 프로그램

**Date**: 2025-11-14  
**Feature**: 본사 정산서 자동화 프로그램

## 엔티티 정의

### 1. MappingConfiguration (매핑 설정)

매핑 규칙을 나타내는 엔티티입니다. JSON 파일로 저장되며 사용자가 GUI를 통해 수정할 수 있습니다.

**Attributes**:
- `data_name` (string, required): 데이터 이름 (예: "라이더 목록", "프로모션")
- `branch_sheet` (string, required): 지점 파일 시트명 (예: "주간정산")
- `branch_range` (string, required): 지점 파일 셀 범위 (예: "C6:C35")
- `head_office_sheet` (string, required): 본사 파일 시트명 (예: "종합")
- `head_office_range` (string, required): 본사 파일 셀 범위 (예: "C17:C46")
- `calculation_method` (string, required): 계산 방식
  - 가능한 값: "simple_copy", "conditional_copy", "date_calculation", "unique_extraction"
- `condition` (object, optional): 조건부 처리 시 조건 정보
  - `source_sheet` (string): 조건 확인 시트
  - `name_column` (string): 이름 확인 열 (예: "G")
  - `value_column` (string): 값 확인 열 (예: "F")
  - `check_column` (string): 달성 여부 확인 열 (예: "J")
  - `check_value` (string): 달성 여부 값 (예: "달성")
- `date_format` (string, optional): 날짜 포맷 (예: "YY.MM.DD")
- `date_type` (string, optional): 날짜 계산 유형
  - 가능한 값: "title", "payment_date", "date_range"

**Validation Rules**:
- `data_name`은 비어있을 수 없음
- `calculation_method`는 유효한 값이어야 함
- `branch_range`와 `head_office_range`는 유효한 셀 범위 형식이어야 함 (예: "A1", "A1:B10")
- `conditional_copy` 방식일 경우 `condition` 필수

**JSON Example**:
```json
{
  "data_name": "라이더 목록",
  "branch_sheet": "주간정산",
  "branch_range": "C6:C35",
  "head_office_sheet": "종합",
  "head_office_range": "C17:C46",
  "calculation_method": "simple_copy"
}
```

```json
{
  "data_name": "프로모션",
  "branch_sheet": "주간정산",
  "branch_range": "E6:E35",
  "head_office_sheet": "협력사 자제 미션",
  "head_office_range": "",
  "calculation_method": "conditional_copy",
  "condition": {
    "source_sheet": "협력사 자제 미션",
    "name_column": "G",
    "value_column": "F",
    "check_column": "J",
    "check_value": "달성"
  }
}
```

### 2. FileInformation (파일 정보)

본사 파일에서 파싱한 정보를 나타내는 엔티티입니다.

**Attributes**:
- `file_path` (string, required): 파일 경로
- `year` (integer, required): 연도 (YYYY)
- `month` (integer, required): 월 (1-12)
- `week` (integer, required): 주차 (1-5)
- `password` (string, optional): 비밀번호 (기본값: config.json에서 로드)
- `is_protected` (boolean, required): 비밀번호 보호 여부

**Validation Rules**:
- `year`는 2000 이상 2100 이하
- `month`는 1-12 범위
- `week`는 1-5 범위
- `is_protected`가 true일 경우 `password` 필수

**State Transitions**:
- 파일 로드 시 파싱 → FileInformation 생성
- 비밀번호 입력 → password 설정
- 파일 열기 시도 → 성공/실패 상태

### 3. ProcessingContext (처리 컨텍스트)

현재 매핑 작업의 상태를 나타내는 엔티티입니다.

**Attributes**:
- `selected_weeks` (array of integers, required): 선택된 주차 목록 (1-5 또는 [1,2,3,4,5])
- `head_office_file` (FileInformation, required): 본사 파일 정보
- `branch_file_path` (string, required): 지점 파일 경로
- `current_week` (integer, optional): 현재 처리 중인 주차
- `current_mapping` (string, optional): 현재 처리 중인 매핑 항목 이름
- `progress` (float, optional): 진행률 (0.0-1.0)
- `status` (string, required): 상태
  - 가능한 값: "idle", "processing", "completed", "error"
- `error_message` (string, optional): 에러 메시지
- `error_type` (string, optional): 에러 유형
  - 가능한 값: "file_error", "mapping_error", "data_error", "system_error"

**Validation Rules**:
- `selected_weeks`는 비어있을 수 없음
- `selected_weeks`의 각 값은 1-5 범위
- `status`가 "error"일 경우 `error_message` 필수

**State Transitions**:
- 초기화: status = "idle"
- 작업 시작: status = "processing", progress = 0.0
- 작업 진행: progress 업데이트 (0.0-1.0)
- 작업 완료: status = "completed", progress = 1.0
- 에러 발생: status = "error", error_message 설정

### 4. ApplicationConfig (애플리케이션 설정)

애플리케이션 전역 설정을 나타내는 엔티티입니다.

**Attributes**:
- `default_password` (string, required): 기본 비밀번호 (기본값: "4880403942")
- `week_offsets` (object, required): 주차별 행 오프셋
  - 키: 주차 번호 (string, "1"-"5")
  - 값: 오프셋 (integer)
- `mapping_file_path` (string, required): 매핑 설정 파일 경로 (기본값: "config/mapping.json")
- `config_file_path` (string, required): 설정 파일 경로 (기본값: "config/config.json")

**Validation Rules**:
- `week_offsets`는 1-5 주차 모두 포함해야 함
- 오프셋 값은 0 이상

**JSON Example**:
```json
{
  "default_password": "4880403942",
  "week_offsets": {
    "1": 0,
    "2": 36,
    "3": 72,
    "4": 108,
    "5": 144
  },
  "mapping_file_path": "config/mapping.json",
  "config_file_path": "config/config.json"
}
```

## 데이터 흐름

### 1. 파일 로드 흐름

```
사용자 파일 선택
  ↓
파일명 파싱 (FileInformation 생성)
  ↓
비밀번호 확인 (필요 시)
  ↓
엑셀 파일 열기
  ↓
시트 및 셀 범위 검증
  ↓
ProcessingContext에 파일 정보 저장
```

### 2. 매핑 실행 흐름

```
ProcessingContext 초기화
  ↓
선택된 주차별 반복:
  ├─ 주차별 오프셋 적용
  ├─ 매핑 규칙별 반복:
  │   ├─ 계산 방식에 따른 데이터 추출
  │   ├─ 데이터 변환/계산
  │   └─ 지점 파일에 데이터 입력
  └─ 진행 상태 업데이트
  ↓
완료 또는 에러 처리
```

### 3. 매핑 설정 수정 흐름

```
매핑 설정 파일 로드
  ↓
MappingConfiguration 리스트 생성
  ↓
GUI에 표시
  ↓
사용자 수정 (추가/수정/삭제)
  ↓
검증
  ↓
매핑 설정 파일 저장
```

## 관계도

```
ApplicationConfig
  ├─ contains → MappingConfiguration (리스트)
  └─ contains → FileInformation (기본값)

ProcessingContext
  ├─ uses → FileInformation (본사 파일)
  ├─ uses → MappingConfiguration (리스트)
  └─ uses → ApplicationConfig (설정)

MappingConfiguration
  └─ references → FileInformation (간접적으로 본사 파일 시트 참조)
```

## 데이터 지속성

### 파일 저장 위치

- `config/config.json`: 애플리케이션 설정 (비밀번호, 오프셋 등)
- `config/mapping.json`: 매핑 규칙 설정
- `logs/`: 로그 파일 (에러 로그, 처리 로그)

### 데이터 백업

- 매핑 설정 파일은 사용자가 직접 백업 가능
- 설정 파일 변경 시 자동 백업 생성 (선택 사항)

## 데이터 검증 전략

### 입력 검증
- 파일명 형식 검증 (정규식)
- 셀 범위 형식 검증 (A1, A1:B10 등)
- 주차 범위 검증 (1-5)
- 날짜 형식 검증

### 런타임 검증
- 시트 존재 여부 확인
- 셀 범위 유효성 확인
- 데이터 타입 일치 확인
- 병합 셀 범위 확인

### 에러 복구
- 매핑 오류 시 매핑 파일 자동 열기
- 파일 오류 시 사용자에게 재시도 옵션 제공
- 부분 실패 시 완료된 작업 롤백 (선택 사항)

