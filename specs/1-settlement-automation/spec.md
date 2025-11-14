# Feature Specification: 본사 정산서 자동화 프로그램

**Feature Branch**: `1-settlement-automation`  
**Created**: 2025-11-14  
**Status**: Draft  
**Input**: User description: "본사 정산서 자동화 프로그램 PRD 작성 요청"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 기본 데이터 매핑 실행 (Priority: P1)

사용자가 본사 정산서 파일과 지점 정산서 파일을 선택하고, 기본적인 데이터 매핑을 실행하여 지점 정산서에 데이터를 자동으로 입력합니다.

**Why this priority**: 이 기능이 없으면 프로그램의 핵심 가치인 자동화가 제공되지 않습니다. 수동 입력 시간을 절약하는 주요 기능입니다.

**Independent Test**: 본사 정산서 파일과 지점 정산서 파일을 준비하고, 단순 복사 항목(라이더 목록, 고용보험, 시간제보험 등)이 올바르게 매핑되어 지점 파일에 입력되는지 확인합니다. 이 기능만으로도 사용자는 수동 입력 작업의 대부분을 자동화할 수 있습니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 비밀번호 보호된 본사 정산서 파일을 선택하고 올바른 비밀번호를 입력했을 때, **When** 파일 로드 버튼을 클릭하면, **Then** 파일이 성공적으로 로드되고 파일 정보가 표시됩니다.

2. **Given** 본사 파일과 지점 파일이 모두 로드된 상태에서, **When** 사용자가 주차를 선택하고 "데이터 매핑 실행" 버튼을 클릭하면, **Then** 단순 복사 항목들이 올바른 셀 위치에 입력됩니다.

3. **Given** 병합된 셀에 데이터를 입력해야 할 때, **When** 매핑이 실행되면, **Then** 병합 영역의 첫 번째 셀에 값이 입력됩니다.

4. **Given** 본사 파일명에서 연월주 정보를 파싱하여, **When** 지점 파일명을 자동 생성할 때, **Then** 올바른 형식(`쿠팡 MM월 W주차 정산표.xlsx`)으로 생성됩니다.

---

### User Story 2 - 조건부 처리 및 계산 로직 (Priority: P2)

사용자가 프로모션 같은 조건부 데이터와 날짜 계산이 필요한 항목들을 자동으로 처리합니다.

**Why this priority**: 단순 복사만으로는 완전한 자동화가 불가능합니다. 조건부 처리와 계산 로직이 있어야 모든 데이터 매핑이 완성됩니다.

**Independent Test**: 본사 파일의 "협력사 자제 미션" 시트에서 달성한 라이더만 프로모션 금액을 추출하여 지점 파일에 입력하는지 확인합니다. 또한 날짜 계산 로직이 올바르게 작동하여 타이틀과 지급일자가 정확히 생성되는지 검증합니다.

**Acceptance Scenarios**:

1. **Given** 본사 파일의 "협력사 자제 미션" 시트에 프로모션 정보가 있을 때, **When** 매핑이 실행되면, **Then** 달성한 라이더만 프로모션 금액이 지점 파일에 입력됩니다.

2. **Given** 본사 파일명에서 월과 주차 정보를 추출했을 때, **When** 타이틀을 생성하면, **Then** 올바른 형식(`기사별 정산 내역(MM월 W주차)`)으로 생성됩니다.

3. **Given** 주차 정보가 있을 때, **When** 날짜 계산이 실행되면, **Then** 전주 수요일부터 해당주 화요일까지의 날짜 범위가 올바르게 계산됩니다.

4. **Given** 주차 정보가 있을 때, **When** 지급일자를 계산하면, **Then** 해당 주차의 금요일 날짜가 `YY.MM.DD` 형식으로 생성됩니다.

---

### User Story 3 - 매핑 설정 관리 (Priority: P3)

사용자가 매핑 정보를 GUI를 통해 수정하고 저장하여, 새로운 매핑 규칙을 추가하거나 기존 규칙을 변경할 수 있습니다.

**Why this priority**: 매핑 규칙이 변경되거나 새로운 데이터 항목이 추가될 때 코드 수정 없이 대응할 수 있어야 합니다. 확장성과 유지보수성을 위해 중요합니다.

**Independent Test**: 매핑 설정 수정 창에서 새로운 매핑 항목을 추가하고 저장한 후, 다음 매핑 실행 시 새로운 규칙이 적용되는지 확인합니다. 이 기능만으로도 사용자는 시스템을 자신의 요구사항에 맞게 커스터마이징할 수 있습니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 "매핑 설정 수정" 버튼을 클릭했을 때, **When** 매핑 수정 창이 열리면, **Then** 현재 모든 매핑 항목이 테이블에 표시됩니다.

2. **Given** 매핑 수정 창에서 새로운 매핑 항목을 추가하고 저장했을 때, **When** 다음 매핑 실행 시, **Then** 새로운 매핑 규칙이 적용됩니다.

3. **Given** 기존 매핑 항목을 수정하고 저장했을 때, **When** 다음 매핑 실행 시, **Then** 수정된 규칙이 적용됩니다.

4. **Given** 매핑 항목을 삭제하고 저장했을 때, **When** 다음 매핑 실행 시, **Then** 삭제된 항목은 더 이상 처리되지 않습니다.

---

### User Story 4 - 주차별 오프셋 처리 및 월간정산 (Priority: P2)

사용자가 여러 주차의 데이터를 한 번에 처리하거나, 월간정산 시트에 전체 주차의 고유 라이더 목록을 자동으로 생성합니다.

**Why this priority**: 주차별 오프셋 처리는 1주차 외의 주차를 처리하는 데 필수적입니다. 월간정산은 전체 월 데이터를 요약하는 중요한 기능입니다.

**Independent Test**: 2주차 데이터를 매핑할 때 행 오프셋이 +36으로 올바르게 적용되는지 확인합니다. 월간정산 시트에 모든 주차의 라이더 목록을 중복 제거하여 고유값만 추출하는지 검증합니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 2주차를 선택했을 때, **When** 매핑이 실행되면, **Then** 모든 셀 범위가 행 방향으로 +36 오프셋이 적용됩니다.

2. **Given** 사용자가 5주차를 선택했을 때, **When** 매핑이 실행되면, **Then** 모든 셀 범위가 행 방향으로 +144 오프셋이 적용됩니다.

3. **Given** 주간정산 시트에 여러 주차의 라이더 목록이 있을 때, **When** 월간정산 시트의 라이더 목록을 생성하면, **Then** 중복이 제거된 고유 라이더 목록만 표시됩니다.

4. **Given** 사용자가 "전체" 주차를 선택했을 때, **When** 매핑이 실행되면, **Then** 모든 주차(1~5주차)가 순차적으로 처리됩니다.

---

### Edge Cases

- 본사 파일이 비밀번호로 보호되어 있는데 잘못된 비밀번호를 입력한 경우 어떻게 처리할까? : 본사 파일 비밀번호가 바뀌어 내려오는 경우는 거의 없으므로, 주차별 테이블의 오프셋과 같은 변수들과 함께 config.json에 저장(비밀번호 기본값 : 4880403942)
- 본사 파일에 필요한 시트가 없거나 시트명이 다른 경우 어떻게 처리할까? : 매핑이 잘못된 것이므로 에러 내용을 띄워주고, 매핑 json 파일을 메모장으로 열고 프로그램 종료
- 본사 파일의 셀 범위에 데이터가 없거나 형식이 다른 경우 어떻게 처리할까? : 매핑이 잘못된 것이므로 에러 내용을 띄워주고, 매핑 json 파일을 메모장으로 열고 프로그램 종료
- 지점 파일의 대상 셀이 이미 데이터로 채워져 있는 경우 덮어쓸지, 건너뛸지 어떻게 처리할까? : 덮어쓰기
- 본사 파일명 형식이 예상과 다른 경우(파싱 실패) 어떻게 처리할까? : 파일명 형식이 다를 경우는 없으나, 다를 경우 몇월 몇주차인지 입력하라고 하고 그걸 기준으로 파싱 규칙 변경
- 프로모션 시트에서 라이더 이름이 일치하지 않는 경우 어떻게 처리할까? : 일치하지 않는 경우는 없으나 모든 라이더가 프로모션에 도전하지는 않음. 지점 파일의 주간정산 시트 B열(라이더명) 기준으로 스캔해서 위치를 잡아줘야 함
- 병합 셀의 범위가 예상과 다른 경우 어떻게 처리할까? : 병합 셀의 좌상단 위치를 제공했으므로, 예상과 다를 일은 없음.
- 주차 정보가 1~5 범위를 벗어나는 경우 어떻게 처리할까? : 이건 지점 파일 수정도 필요하므로 에러 내용과 제작자에게 문의하라는 팝업을 띄워주고 프로그램 종료

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load head office settlement Excel files, including password-protected files
- **FR-002**: System MUST load branch settlement Excel files or generate them automatically based on head office file information
- **FR-003**: System MUST parse year, month, and week information from head office file names in the format `빅보스_부산_진구중앙_YYYY_MM-W.xlsx`
- **FR-004**: System MUST generate branch file names in the format `쿠팡 MM월 W주차 정산표.xlsx` based on parsed information
- **FR-005**: System MUST support simple copy operations that map data from source cells to target cells
- **FR-006**: System MUST detect merged cells and write values to the first cell of merged ranges
- **FR-007**: System MUST support conditional copy operations (e.g., only copy promotion amounts for riders who achieved targets)
- **FR-008**: System MUST calculate dates based on week information (previous Wednesday to current Tuesday, Friday payment date)
- **FR-009**: System MUST format date strings as `YY.MM.DD` for payment dates
- **FR-010**: System MUST format title strings with month and week information (e.g., `기사별 정산 내역(MM월 W주차)`)
- **FR-011**: System MUST apply row offsets based on selected week (week 1: base, week 2: +36, week 3: +72, week 4: +108, week 5: +144)
- **FR-012**: System MUST extract unique rider names from all weeks in weekly settlement sheet for monthly settlement sheet
- **FR-013**: System MUST allow users to select specific weeks (1-5) or process all weeks at once
- **FR-014**: System MUST store and load mapping configurations from persistent storage (JSON or YAML format)
- **FR-015**: System MUST provide a GUI for viewing and editing mapping configurations
- **FR-016**: System MUST allow users to add, modify, and delete mapping entries through the GUI
- **FR-017**: System MUST display progress status and logs during mapping operations
- **FR-018**: System MUST handle errors gracefully and display user-friendly error messages
- **FR-019**: System MUST validate file formats and structure before processing
- **FR-020**: System MUST support extensible calculation methods (simple copy, conditional copy, date calculation, unique value extraction, etc.)

### Key Entities *(include if feature involves data)*

- **Mapping Configuration**: Represents a data mapping rule containing:
  - Data name (e.g., "라이더 목록", "프로모션")
  - Branch file sheet name
  - Branch file cell range
  - Head office file sheet name
  - Head office file cell range
  - Calculation/transformation method (simple copy, conditional copy, date calculation, unique value extraction, etc.)

- **File Information**: Represents parsed information from head office file:
  - Year (YYYY)
  - Month (MM)
  - Week (W, 1-5)
  - File path
  - Password (if protected)

- **Processing Context**: Represents the current mapping operation state:
  - Selected week(s)
  - Source file information
  - Target file information
  - Current progress
  - Error state (if any)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete a single-week data mapping operation in under 30 seconds from file selection to completion
- **SC-002**: The system correctly maps at least 95% of simple copy operations without manual intervention
- **SC-003**: Users can process all 5 weeks of data in under 3 minutes
- **SC-004**: The system handles password-protected files with 100% success rate when correct password is provided
- **SC-005**: Users can add or modify mapping configurations without technical knowledge in under 5 minutes
- **SC-006**: Error messages are clear enough that 90% of users can resolve issues without consulting documentation
- **SC-007**: The system processes files with up to 50 rows of data without performance degradation
- **SC-008**: Monthly settlement sheet generation completes in under 10 seconds for a full month of data (5 weeks)

