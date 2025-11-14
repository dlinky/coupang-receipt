# Excel Processor Contract

**Service**: Excel Processor  
**Purpose**: 엑셀 파일의 읽기/쓰기 작업을 처리하는 서비스

## Interface

### `load_workbook(file_path: str, password: str = None) -> Workbook`

엑셀 파일을 로드합니다.

**Parameters**:
- `file_path` (str): 파일 경로
- `password` (str, optional): 비밀번호 (보호된 파일인 경우)

**Returns**:
- `Workbook`: openpyxl Workbook 객체

**Preconditions**:
- 파일이 존재해야 함
- 비밀번호 보호된 파일인 경우 올바른 비밀번호 필요

**Postconditions**:
- Workbook 객체가 메모리에 로드됨

**Exceptions**:
- `FileNotFoundError`: 파일이 존재하지 않음
- `ValueError`: 비밀번호가 올바르지 않음
- `PermissionError`: 파일 접근 권한 없음

### `get_sheet(workbook: Workbook, sheet_name: str) -> Worksheet`

워크북에서 시트를 가져옵니다.

**Parameters**:
- `workbook` (Workbook): 워크북 객체
- `sheet_name` (str): 시트명

**Returns**:
- `Worksheet`: openpyxl Worksheet 객체

**Preconditions**:
- 워크북이 유효해야 함
- 시트명이 존재해야 함

**Postconditions**:
- 시트 객체 반환

**Exceptions**:
- `KeyError`: 시트가 존재하지 않음

### `read_cell_range(worksheet: Worksheet, cell_range: str) -> List[Any]`

셀 범위에서 데이터를 읽습니다.

**Parameters**:
- `worksheet` (Worksheet): 워크시트 객체
- `cell_range` (str): 셀 범위 (예: "A1:B10")

**Returns**:
- `List[Any]`: 셀 값 리스트

**Preconditions**:
- 워크시트가 유효해야 함
- 셀 범위 형식이 올바르야 함

**Postconditions**:
- 셀 범위의 모든 값이 리스트로 반환됨

**Exceptions**:
- `ValueError`: 셀 범위 형식이 올바르지 않음

### `write_cell_range(worksheet: Worksheet, cell_range: str, values: List[Any]) -> None`

셀 범위에 데이터를 씁니다.

**Parameters**:
- `worksheet` (Worksheet): 워크시트 객체
- `cell_range` (str): 셀 범위 (예: "A1:B10")
- `values` (List[Any]): 쓸 값 리스트

**Preconditions**:
- 워크시트가 유효해야 함
- 셀 범위 형식이 올바르야 함
- 값 리스트가 셀 범위 크기와 일치해야 함

**Postconditions**:
- 셀 범위에 값이 입력됨
- 병합 셀인 경우 첫 번째 셀에 입력

**Exceptions**:
- `ValueError`: 셀 범위 형식이 올바르지 않음
- `IndexError`: 값 리스트 크기가 셀 범위와 일치하지 않음

### `is_merged_cell(worksheet: Worksheet, cell_address: str) -> bool`

셀이 병합된 셀인지 확인합니다.

**Parameters**:
- `worksheet` (Worksheet): 워크시트 객체
- `cell_address` (str): 셀 주소 (예: "A1")

**Returns**:
- `bool`: 병합된 셀 여부

**Preconditions**:
- 워크시트가 유효해야 함
- 셀 주소 형식이 올바르야 함

**Postconditions**:
- 병합 여부 반환

### `get_merged_cell_top_left(worksheet: Worksheet, cell_address: str) -> str`

병합된 셀의 좌상단 셀 주소를 반환합니다.

**Parameters**:
- `worksheet` (Worksheet): 워크시트 객체
- `cell_address` (str): 셀 주소

**Returns**:
- `str`: 좌상단 셀 주소

**Preconditions**:
- 워크시트가 유효해야 함
- 셀이 병합된 셀 범위에 포함되어야 함

**Postconditions**:
- 좌상단 셀 주소 반환

### `save_workbook(workbook: Workbook, file_path: str) -> None`

워크북을 파일로 저장합니다.

**Parameters**:
- `workbook` (Workbook): 워크북 객체
- `file_path` (str): 저장할 파일 경로

**Preconditions**:
- 워크북이 유효해야 함
- 파일 경로가 쓰기 가능해야 함

**Postconditions**:
- 워크북이 파일로 저장됨

**Exceptions**:
- `PermissionError`: 파일 쓰기 권한 없음
- `IOError`: 파일 저장 실패

## Error Handling

### 파일 오류
- 파일이 존재하지 않음 → `FileNotFoundError`
- 비밀번호 오류 → `ValueError` with message "Invalid password"
- 파일 접근 권한 없음 → `PermissionError`

### 데이터 오류
- 시트가 존재하지 않음 → `KeyError` with sheet name
- 셀 범위 형식 오류 → `ValueError` with message "Invalid cell range format"
- 값 타입 불일치 → `TypeError` (자동 변환 시도)

## Performance Requirements

- 파일 로드: 5초 이내 (50행 이하)
- 셀 범위 읽기: 1초 이내 (50행 이하)
- 셀 범위 쓰기: 1초 이내 (50행 이하)
- 파일 저장: 3초 이내

## Testing Contract

### Unit Tests
- 파일 로드 테스트 (일반 파일, 보호된 파일)
- 셀 읽기/쓰기 테스트
- 병합 셀 처리 테스트
- 에러 케이스 테스트

### Integration Tests
- 실제 엑셀 파일을 사용한 전체 워크플로우 테스트
- 비밀번호 보호 파일 테스트
- 대용량 파일 테스트 (50행)

