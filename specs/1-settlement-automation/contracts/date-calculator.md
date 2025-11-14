# Date Calculator Contract

**Service**: Date Calculator  
**Purpose**: 주차 정보를 기반으로 날짜를 계산하는 서비스

## Interface

### `calculate_title_date(year: int, month: int, week: int) -> str`

타이틀용 날짜 문자열을 생성합니다.

**Parameters**:
- `year` (int): 연도
- `month` (int): 월 (1-12)
- `week` (int): 주차 (1-5)

**Returns**:
- `str`: "MM월 W주차" 형식의 문자열 (예: "11월 1주차")

**Preconditions**:
- `year`는 2000 이상 2100 이하
- `month`는 1-12 범위
- `week`는 1-5 범위

**Postconditions**:
- 형식화된 날짜 문자열 반환

**Exceptions**:
- `ValueError`: 파라미터가 유효 범위를 벗어남

### `calculate_payment_date(year: int, month: int, week: int) -> str`

지급일자 문자열을 생성합니다.

**Parameters**:
- `year` (int): 연도
- `month` (int): 월 (1-12)
- `week` (int): 주차 (1-5)

**Returns**:
- `str`: "YY.MM.DD" 형식의 문자열 (예: "24.11.15")

**Preconditions**:
- `year`는 2000 이상 2100 이하
- `month`는 1-12 범위
- `week`는 1-5 범위

**Postconditions**:
- 해당 주차의 금요일 날짜가 "YY.MM.DD" 형식으로 반환됨

**Exceptions**:
- `ValueError`: 파라미터가 유효 범위를 벗어남

### `calculate_date_range(year: int, month: int, week: int) -> str`

날짜 범위 문자열을 생성합니다.

**Parameters**:
- `year` (int): 연도
- `month` (int): 월 (1-12)
- `week` (int): 주차 (1-5)

**Returns**:
- `str`: "MM.DD ~ MM.DD" 형식의 문자열 (예: "11.06 ~ 11.12")

**Preconditions**:
- `year`는 2000 이상 2100 이하
- `month`는 1-12 범위
- `week`는 1-5 범위

**Postconditions**:
- 전주 수요일부터 해당주 화요일까지의 날짜 범위가 "MM.DD ~ MM.DD" 형식으로 반환됨

**Exceptions**:
- `ValueError`: 파라미터가 유효 범위를 벗어남

### `get_week_friday(year: int, month: int, week: int) -> datetime.date`

해당 주차의 금요일 날짜를 반환합니다.

**Parameters**:
- `year` (int): 연도
- `month` (int): 월 (1-12)
- `week` (int): 주차 (1-5)

**Returns**:
- `datetime.date`: 금요일 날짜 객체

**Preconditions**:
- `year`는 2000 이상 2100 이하
- `month`는 1-12 범위
- `week`는 1-5 범위

**Postconditions**:
- 해당 주차의 금요일 날짜 반환

**Exceptions**:
- `ValueError`: 파라미터가 유효 범위를 벗어남

### `get_week_range(year: int, month: int, week: int) -> Tuple[datetime.date, datetime.date]`

해당 주차의 날짜 범위를 반환합니다 (전주 수요일 ~ 해당주 화요일).

**Parameters**:
- `year` (int): 연도
- `month` (int): 월 (1-12)
- `week` (int): 주차 (1-5)

**Returns**:
- `Tuple[datetime.date, datetime.date]`: (시작일, 종료일)

**Preconditions**:
- `year`는 2000 이상 2100 이하
- `month`는 1-12 범위
- `week`는 1-5 범위

**Postconditions**:
- 전주 수요일과 해당주 화요일 날짜 튜플 반환

**Exceptions**:
- `ValueError`: 파라미터가 유효 범위를 벗어남

## 날짜 계산 로직

### 주차 계산 규칙
1. 해당 월의 첫 번째 주차 시작일 계산
2. 주차 번호에 따라 시작일에서 (week - 1) * 7일 추가
3. 해당 주의 금요일 계산
4. 전주 수요일 계산 (금요일 - 5일)
5. 해당주 화요일 계산 (금요일 - 3일)

### 예시
- 2024년 11월 1주차:
  - 금요일: 2024-11-08
  - 범위: 2024-11-06 (수) ~ 2024-11-12 (화)

## Error Handling

### 입력 검증 오류
- 파라미터가 유효 범위를 벗어남 → `ValueError` with message "Invalid parameter: {param_name}"

### 날짜 계산 오류
- 잘못된 날짜 계산 → `ValueError` with message "Date calculation failed"

## Performance Requirements

- 단일 날짜 계산: 1ms 이내
- 모든 날짜 계산 (타이틀, 지급일자, 범위): 10ms 이내

## Testing Contract

### Unit Tests
- 각 날짜 계산 함수별 테스트
- 경계값 테스트 (1주차, 5주차, 월 초/말)
- 잘못된 입력값 테스트
- 다양한 연도/월 조합 테스트

### Edge Cases
- 월의 첫 주차와 마지막 주차
- 월 경계를 넘는 주차 (예: 11월 마지막 주차가 12월로 넘어가는 경우)
- 윤년 처리

