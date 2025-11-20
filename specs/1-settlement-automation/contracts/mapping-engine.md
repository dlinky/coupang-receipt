# Mapping Engine Contract

**Service**: Mapping Engine  
**Purpose**: 엑셀 파일 간 데이터 매핑을 수행하는 핵심 서비스

## Interface

### `execute_mapping(mapping_config: MappingConfiguration, head_office_file: FileInformation, branch_file_path: str, week: int) -> MappingResult`

매핑 규칙에 따라 본사 파일에서 지점 파일로 데이터를 매핑합니다.

**Parameters**:
- `mapping_config` (MappingConfiguration): 매핑 설정
- `head_office_file` (FileInformation): 본사 파일 정보
- `branch_file_path` (str): 지점 파일 경로
- `week` (int): 주차 (1-5)

**Returns**:
- `MappingResult`: 매핑 결과
  - `success` (bool): 성공 여부
  - `rows_processed` (int): 처리된 행 수
  - `error_message` (str, optional): 에러 메시지

**Preconditions**:
- 본사 파일이 존재하고 열 수 있어야 함
- 지점 파일이 존재하고 쓰기 가능해야 함
- `week`는 1-5 범위여야 함
- `mapping_config`가 유효해야 함

**Postconditions**:
- 성공 시: 지점 파일에 데이터가 입력됨
- 실패 시: 지점 파일은 변경되지 않음

**Exceptions**:
- `FileNotFoundError`: 파일이 존재하지 않음
- `PermissionError`: 파일 접근 권한 없음
- `ValueError`: 매핑 설정이 유효하지 않음
- `KeyError`: 시트가 존재하지 않음

## Calculation Methods

### 1. `simple_copy`

단순 복사: 본사 파일의 셀 범위에서 지점 파일의 셀 범위로 데이터를 복사합니다.

**Input**: 
- 본사 파일 셀 범위 (주차별 오프셋 적용)
- 지점 파일 셀 범위 (주차별 오프셋 적용)

**Output**: 
- 지점 파일에 데이터 입력

**Behavior**:
- 병합 셀 자동 감지 및 첫 번째 셀에 입력
- 빈 셀은 건너뜀

### 2. `conditional_copy`

조건부 복사: 조건을 만족하는 경우만 데이터를 복사합니다.

**Input**:
- 본사 파일 시트 및 셀 범위
- 조건 정보 (이름 열, 값 열, 확인 열, 확인 값)

**Output**:
- 조건을 만족하는 라이더의 데이터만 지점 파일에 입력

**Behavior**:
- 지점 파일의 라이더 목록(B열)을 기준으로 매칭
- 본사 파일에서 해당 라이더의 조건 확인
- 조건 만족 시에만 값 입력

### 3. `date_calculation`

날짜 계산: 주차 정보를 기반으로 날짜를 계산하여 입력합니다.

**Input**:
- 주차 정보 (week)
- 날짜 계산 유형 (title, payment_date, date_range)

**Output**:
- 계산된 날짜 문자열

**Behavior**:
- `title`: "MM월 W주차" 형식
- `payment_date`: "YY.MM.DD" 형식 (해당 주차 금요일)
- `date_range`: "MM.DD ~ MM.DD" 형식 (전주 수요일 ~ 해당주 화요일)

### 4. `unique_extraction`

고유값 추출: 여러 주차의 데이터에서 중복을 제거하여 고유값만 추출합니다.

**Input**:
- 지점 파일의 주간정산 시트
- 모든 주차의 라이더 목록

**Output**:
- 중복 제거된 고유 라이더 목록

**Behavior**:
- 주간정산 시트의 모든 주차 라이더 목록 수집
- 중복 제거
- 월간정산 시트에 입력

### 5. `simple_sum`

단순 합산: 여러 열(붙어있거나 떨어져 있는)의 값을 행별로 합산하여 입력합니다.

**Input**:
- 본사 파일 셀 범위 (쉼표로 구분된 여러 범위, 예: "G17:I46" 또는 "K17:K46, M17:M46, O17:O46")
- 지점 파일 셀 범위 (주차별 오프셋 적용)

**Output**:
- 각 행별로 합산된 값이 지점 파일에 입력

**Behavior**:
- 여러 범위를 파싱 (쉼표로 구분)
- 각 범위에서 같은 행의 값들을 합산
- 숫자가 아닌 값(None, 빈 문자열 등)은 합산에서 제외
- 모든 범위는 동일한 행 수를 가져야 함
- 지점 파일에만 주차별 오프셋 적용

**Examples**:
- 붙어있는 열: `head_office_range="G17:I46"` → G, H, I 열의 값을 행별로 합산
- 떨어져 있는 열: `head_office_range="K17:K46, M17:M46, O17:O46"` → K, M, O 열의 값을 행별로 합산

### 6. `conditional_sum`

조건부 합산: 조건을 만족하는 모든 행의 value_column 값을 합산하여 입력합니다.

**Input**:
- 본사 파일 조건 시트 및 조건 정보 (conditional_copy와 동일)
  - `source_sheet`: 조건 확인 시트
  - `name_column`: 이름 확인 열 (예: "G")
  - `value_column`: 값 확인 열 (예: "F")
  - `check_column`: 달성 여부 확인 열 (예: "J")
  - `check_value`: 달성 여부 값 (예: "달성")
- 지점 파일 셀 범위 (주차별 오프셋 적용)

**Output**:
- 각 라이더별로 조건을 만족하는 모든 행의 value_column 값이 합산되어 지점 파일에 입력

**Behavior**:
- 지점 파일의 라이더 목록(C열)을 기준으로 매칭
- 본사 파일에서 해당 라이더의 조건 확인
- 조건을 만족하는 모든 행의 value_column 값을 합산
- 같은 라이더가 여러 행에 조건을 만족하는 경우 모두 합산
- 숫자가 아닌 값(None, 문자열 등)은 합산에서 제외
- 매칭되는 행이 없는 경우 0 입력
- 지점 파일에만 주차별 오프셋 적용

**Difference from conditional_copy**:
- `conditional_copy`: 조건을 만족하는 첫 번째 행의 값만 가져옴
- `conditional_sum`: 조건을 만족하는 모든 행의 값을 합산

**Example**:
```json
{
  "data_name": "지점 프로모션 합계",
  "branch_sheet": "주간정산",
  "branch_range": "H6:H35",
  "head_office_sheet": "협력사 자체 미션",
  "head_office_range": "",
  "calculation_method": "conditional_sum",
  "condition": {
    "source_sheet": "협력사 자체 미션",
    "name_column": "G",
    "value_column": "F",
    "check_column": "J",
    "check_value": "달성"
  }
}
```

## Error Handling

### 매핑 오류
- 시트가 존재하지 않음 → `KeyError` 발생, 매핑 파일 열기 안내
- 셀 범위가 유효하지 않음 → `ValueError` 발생, 매핑 파일 열기 안내
- 데이터 형식 불일치 → `TypeError` 발생, 사용자에게 알림

### 파일 오류
- 파일이 존재하지 않음 → `FileNotFoundError` 발생
- 파일이 열 수 없음 → `PermissionError` 발생
- 비밀번호 오류 → `ValueError` 발생, 재입력 요청

## Performance Requirements

- 단일 매핑 항목 처리: 1초 이내
- 전체 주차(5주차) 처리: 3분 이내
- 월간정산 생성: 10초 이내

## Testing Contract

### Unit Tests
- 각 계산 방식별 독립 테스트
- 오프셋 적용 테스트
- 병합 셀 처리 테스트
- 에러 케이스 테스트

### Integration Tests
- 전체 매핑 워크플로우 테스트
- 실제 엑셀 파일을 사용한 테스트
- 여러 주차 처리 테스트

