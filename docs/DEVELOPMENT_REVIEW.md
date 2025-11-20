# 개발 회고 및 학습 문서

## 프로젝트 개요

**프로젝트명**: 본사 정산서 자동화 프로그램  
**개발 기간**: 2024년 11월  
**개발 시간**: 
- PRD 작성 및 초기 구현: ~1시간
- 기능 수정 및 디버깅: 추가 시간 소요

## 개발 과정 타임라인

### Phase 1: 기획 및 설계 (빠른 진행)
- ✅ PRD 작성
- ✅ 기술 스택 결정 (Python, PySide6, openpyxl)
- ✅ 데이터 모델 설계
- ✅ 서비스 계약 정의
- ✅ 구현 계획 수립

### Phase 2: 초기 구현 (빠른 진행)
- ✅ 프로젝트 구조 생성
- ✅ 핵심 로직 구현
- ✅ GUI 구현
- ✅ 기본 기능 동작 확인

### Phase 3: 기능 수정 및 디버깅 (시간 소요)
- ⚠️ 실제 사용 중 발견된 문제들
- ⚠️ 반복적인 수정 작업
- ⚠️ 엣지 케이스 처리

## 발생한 주요 문제와 해결 과정

### 1. 오프셋 적용 로직 오류

**문제**: 
- 2주차 파일을 사용해도 1주차 위치에 데이터가 입력됨
- 본사 파일과 지점 파일 모두에 오프셋을 적용하고 있었음

**원인 분석**:
- 초기 설계에서 "주차별 오프셋 적용"이라는 요구사항을 단순히 모든 범위에 적용
- 본사 파일은 이미 해당 주차의 데이터가 있으므로 오프셋 불필요
- 지점 파일만 주차별 위치가 다르므로 오프셋 필요

**해결**:
```python
# 수정 전
source_range = CellUtils.apply_row_offset(
    mapping_config.head_office_range, week_offset  # ❌ 불필요한 오프셋
)
target_range = CellUtils.apply_row_offset(
    mapping_config.branch_range, week_offset
)

# 수정 후
source_range = mapping_config.head_office_range  # ✅ 본사 파일은 오프셋 없음
target_range = CellUtils.apply_row_offset(
    mapping_config.branch_range, week_offset  # ✅ 지점 파일만 오프셋
)
```

**교훈**:
- 요구사항을 구현할 때 "왜" 필요한지 명확히 이해해야 함
- 데이터 소스와 타겟의 특성을 구분하여 처리해야 함

### 2. 날짜 범위 계산 로직 오류

**문제**:
- 2주차 정산기간이 "11.09 ~ 11.11"로 잘못 계산됨
- 실제로는 "11.05 ~ 11.11"이어야 함

**원인 분석**:
- 초기 설계에서 "전주 수요일 ~ 해당주 화요일"로 계산
- 실제 비즈니스 로직은 "전주 화요일 ~ 해당주 월요일"
- 요구사항 문서와 실제 사용 패턴의 불일치

**해결**:
```python
# 수정 전
previous_wednesday = friday - timedelta(days=5)  # 전주 수요일
current_tuesday = friday - timedelta(days=3)     # 해당주 화요일

# 수정 후
previous_tuesday = friday - timedelta(days=10)   # 전주 화요일
current_monday = friday - timedelta(days=4)      # 해당주 월요일
```

**교훈**:
- 비즈니스 로직은 실제 사용 패턴을 확인해야 함
- 문서화된 요구사항과 실제 요구사항이 다를 수 있음
- 프로토타입을 빠르게 만들어 실제 사용자와 검증 필요

### 3. 타이틀 형식 불일치

**문제**:
- 모든 타이틀이 "11월 1주차" 형식으로만 표시됨
- 각 타이틀마다 다른 형식이 필요했음

**원인 분석**:
- 초기 구현에서 `date_type`만으로 구분
- 실제로는 `data_name`에 따라 다른 형식 필요
- 매핑 설정의 세부 요구사항 누락

**해결**:
```python
# 수정 전
if mapping_config.date_type == "title":
    date_str = self.date_calculator.calculate_title_date(...)

# 수정 후
if mapping_config.date_type == "title":
    base_date = self.date_calculator.calculate_title_date(...)
    if mapping_config.data_name == "기사별 정산 내역 타이틀":
        date_str = f"기사별 정산 내역({base_date})"
    elif mapping_config.data_name == "익일정산 신청 내역 타이틀":
        date_str = f"익일정산 신청 내역({base_date})"
    # ...
```

**교훈**:
- 추상화 수준을 적절히 유지해야 함
- 너무 일반화하면 세부 요구사항을 놓칠 수 있음
- 실제 사용 예시를 더 많이 수집해야 함

### 4. 파일 저장 시 수식 손실

**문제**:
- 지점 파일의 수식이 모두 사라짐

**원인 분석**:
- `openpyxl`의 `data_only=True` 옵션 사용
- 이 옵션은 계산된 값만 읽고 수식은 무시

**해결**:
```python
# 수정 전
workbook = load_workbook(path, data_only=True)  # ❌ 수식 손실

# 수정 후
workbook = load_workbook(path, data_only=False)  # ✅ 수식 보존
```

**교훈**:
- 라이브러리 옵션의 의미를 정확히 이해해야 함
- Excel 파일의 구조(수식, 값, 서식)를 고려해야 함

### 5. 비밀번호 보호 파일 처리 실패

**문제**:
- 비밀번호가 걸린 Excel 파일을 zip 파일로 인식

**원인 분석**:
- `openpyxl`은 비밀번호 보호 파일을 직접 처리하지 못함
- `msoffcrypto` 라이브러리 필요

**해결**:
```python
if password:
    decrypted = io.BytesIO()
    with open(path, "rb") as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=password)
        office_file.decrypt(decrypted)
    decrypted.seek(0)
    workbook = load_workbook(decrypted, data_only=False)
```

**교훈**:
- 라이브러리의 한계를 미리 파악해야 함
- 기술 스택 선택 시 엣지 케이스 고려 필요

## 개선할 수 있었던 점들

### 1. 더 상세한 요구사항 수집

**문제점**:
- 초기 요구사항이 추상적이었음
- 실제 사용 패턴을 미리 확인하지 못함

**개선 방안**:
- 실제 Excel 파일 샘플을 미리 받아서 분석
- 각 셀의 의미와 계산 로직을 명확히 문서화
- 사용자와 함께 프로토타입 검증

### 2. 테스트 우선 개발 (TDD)

**문제점**:
- 구현 후 테스트를 진행
- 엣지 케이스를 놓침

**개선 방안**:
- 테스트 케이스를 먼저 작성
- 실제 Excel 파일을 테스트 데이터로 사용
- 각 주차별, 각 데이터 타입별 테스트

### 3. 점진적 통합

**문제점**:
- 모든 기능을 구현한 후 테스트
- 문제 발견 시 수정 범위가 넓음

**개선 방안**:
- 기능별로 단계적 구현 및 테스트
- 각 단계마다 실제 사용자와 검증
- 작은 단위로 반복 배포

### 4. 더 나은 로깅 및 디버깅

**문제점**:
- 문제 발생 시 원인 파악이 어려움
- 어떤 단계에서 문제가 발생했는지 불명확

**개선 방안**:
- 각 단계별 상세 로깅
- 중간 결과를 파일로 저장하여 확인
- 디버그 모드 추가

## 학습 포인트

### 1. 요구사항 분석의 중요성

**배운 점**:
- 문서화된 요구사항과 실제 요구사항이 다를 수 있음
- 실제 사용 패턴을 직접 확인하는 것이 중요
- 추상적인 설명보다 구체적인 예시가 필요

**적용 방법**:
- 실제 데이터 샘플을 먼저 받기
- 사용자와 함께 워크플로우 확인
- 프로토타입을 빠르게 만들어 검증

### 2. 도메인 지식의 중요성

**배운 점**:
- 정산 업무의 특수한 로직을 이해해야 함
- 날짜 계산, 주차 개념 등 비즈니스 규칙 중요
- Excel 파일 구조와 사용 패턴 이해 필요

**적용 방법**:
- 도메인 전문가와 충분한 소통
- 비즈니스 로직을 코드에 주석으로 명확히 기록
- 도메인 용어를 코드에도 반영

### 3. 라이브러리 선택과 이해

**배운 점**:
- 라이브러리의 기능과 한계를 정확히 파악해야 함
- 옵션의 의미를 정확히 이해해야 함
- 엣지 케이스 처리 방법 확인 필요

**적용 방법**:
- 공식 문서를 꼼꼼히 읽기
- 간단한 테스트 코드로 동작 확인
- 엣지 케이스를 미리 테스트

### 4. 점진적 개발과 피드백

**배운 점**:
- 한 번에 완벽하게 만들기보다 빠르게 만들고 개선
- 실제 사용자 피드백이 가장 중요
- 작은 단위로 반복하는 것이 효율적

**적용 방법**:
- MVP를 빠르게 만들기
- 사용자와 함께 테스트
- 피드백을 빠르게 반영

## 향후 유사 프로젝트 체크리스트

### 요구사항 수집 단계
- [ ] 실제 데이터 샘플 수집
- [ ] 사용자 워크플로우 직접 관찰
- [ ] 각 데이터 필드의 의미와 계산 로직 명확화
- [ ] 엣지 케이스 목록 작성
- [ ] 비즈니스 규칙 문서화

### 설계 단계
- [ ] 기술 스택의 한계점 확인
- [ ] 라이브러리 옵션 정확히 이해
- [ ] 데이터 흐름도 작성
- [ ] 에러 케이스 처리 계획
- [ ] 테스트 전략 수립

### 구현 단계
- [ ] 작은 단위로 구현 및 테스트
- [ ] 실제 데이터로 중간 검증
- [ ] 로깅 및 디버깅 도구 준비
- [ ] 사용자와 함께 단계별 검증

### 테스트 단계
- [ ] 실제 Excel 파일로 테스트
- [ ] 모든 주차별 테스트
- [ ] 엣지 케이스 테스트
- [ ] 사용자 수락 테스트

## 코드 품질 개선 아이디어

### 1. 더 명확한 네이밍

```python
# 개선 전
week_offset = self.config_manager.get_week_offset(week)

# 개선 후
branch_file_row_offset = self.config_manager.get_branch_file_row_offset(week)
```

### 2. 상수 분리

```python
# 개선 전
if mapping_config.data_name in ["고용보험", "산재보험", "시간제보험"]:

# 개선 후
INSURANCE_FIELDS_REQUIRING_SIGN_INVERSION = ["고용보험", "산재보험", "시간제보험"]
if mapping_config.data_name in INSURANCE_FIELDS_REQUIRING_SIGN_INVERSION:
```

### 3. 에러 메시지 개선

```python
# 개선 전
raise ValueError(f"Invalid cell range format: {cell_range}")

# 개선 후
raise ValueError(
    f"Invalid cell range format: '{cell_range}'. "
    f"Expected format: 'A1:B10' or 'C6'"
)
```

### 4. 타입 힌팅 강화

```python
# 개선 전
def apply_row_offset(cls, cell_range: str, offset: int) -> str:

# 개선 후
def apply_row_offset(
    cls, 
    cell_range: str, 
    offset: int
) -> str:
    """Apply row offset to cell range.
    
    Args:
        cell_range: Cell range in format 'A1:B10' or 'C6'
        offset: Row offset to apply (can be negative)
    
    Returns:
        Updated cell range with offset applied
        
    Raises:
        ValueError: If cell_range format is invalid
        
    Example:
        >>> CellUtils.apply_row_offset('C6:C35', 36)
        'C42:C71'
    """
```

## 결론

이 프로젝트를 통해 배운 가장 중요한 교훈은 **"완벽한 설계보다 빠른 프로토타입과 지속적인 피드백"**입니다.

초기 설계와 구현은 빠르게 진행했지만, 실제 사용 중 발견된 문제들을 해결하는 과정에서 많은 시간이 소요되었습니다. 이는:

1. **요구사항의 불완전성**: 문서화된 요구사항과 실제 요구사항의 차이
2. **도메인 지식의 부족**: 정산 업무의 특수한 로직 이해 부족
3. **테스트의 부족**: 실제 데이터로 충분한 테스트 미진행

하지만 이러한 과정을 통해:
- 실제 사용 패턴을 이해하게 되었고
- 비즈니스 로직을 정확히 구현할 수 있게 되었으며
- 향후 유사 프로젝트에서 개선할 수 있는 방향을 파악하게 되었습니다.

**핵심 교훈**: 빠른 프로토타입 → 실제 사용자 피드백 → 빠른 개선 사이클이 중요합니다.


