# Tasks: 본사 정산서 자동화 프로그램

**Input**: Design documents from `/specs/1-settlement-automation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the specification, but core logic should be tested to meet 70% coverage goal per Constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (src/, tests/, config/ directories) per implementation plan
- [x] T002 Initialize Python project with requirements.txt (PySide6, openpyxl, pytest, coverage)
- [x] T003 [P] Configure linting and formatting tools (black, flake8 or ruff)
- [x] T004 [P] Create .gitignore file for Python project
- [x] T005 [P] Create README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create base data models in src/models/ (mapping_config.py, file_info.py, processing_context.py)
- [x] T007 [P] Implement config manager service in src/services/config_manager.py (load/save JSON config files)
- [x] T008 [P] Implement file parser utility in src/utils/file_parser.py (parse filename to extract year, month, week)
- [x] T009 [P] Implement cell utilities in src/utils/cell_utils.py (parse cell ranges, apply offsets)
- [x] T010 Setup error handling infrastructure (custom exceptions, error messages)
- [x] T011 Setup logging infrastructure (log to file and console)
- [x] T012 Create default config files (config/config.json, config/mapping.json) with initial values

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 기본 데이터 매핑 실행 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 본사 정산서 파일과 지점 정산서 파일을 선택하고, 기본적인 데이터 매핑을 실행하여 지점 정산서에 데이터를 자동으로 입력합니다.

**Independent Test**: 본사 정산서 파일과 지점 정산서 파일을 준비하고, 단순 복사 항목(라이더 목록, 고용보험, 시간제보험 등)이 올바르게 매핑되어 지점 파일에 입력되는지 확인합니다.

### Implementation for User Story 1

- [x] T013 [US1] Implement Excel processor service in src/services/excel_processor.py (load workbook, read/write cells, handle password-protected files)
- [x] T014 [US1] Implement simple copy calculation method in src/services/mapping_engine.py (copy data from source to target cells)
- [x] T015 [US1] Implement merged cell detection and handling in src/services/excel_processor.py (detect merged cells, write to top-left cell)
- [x] T016 [US1] Implement mapping engine core in src/services/mapping_engine.py (execute_mapping method, load mapping config)
- [x] T017 [US1] Create main window GUI in src/gui/main_window.py (file selection buttons, password input, week selection, execute button)
- [x] T018 [US1] Implement file loading logic in src/gui/main_window.py (load head office file, parse filename, load branch file)
- [x] T019 [US1] Implement mapping execution in src/gui/main_window.py (connect to mapping engine, display progress, handle errors)
- [x] T020 [US1] Implement progress display in src/gui/main_window.py (progress bar, log output)
- [x] T021 [US1] Create main entry point in src/main.py (initialize application, show main window)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can select files, choose a week, and execute basic data mapping.

---

## Phase 4: User Story 2 - 조건부 처리 및 계산 로직 (Priority: P2)

**Goal**: 사용자가 프로모션 같은 조건부 데이터와 날짜 계산이 필요한 항목들을 자동으로 처리합니다.

**Independent Test**: 본사 파일의 "협력사 자제 미션" 시트에서 달성한 라이더만 프로모션 금액을 추출하여 지점 파일에 입력하는지 확인합니다. 또한 날짜 계산 로직이 올바르게 작동하여 타이틀과 지급일자가 정확히 생성되는지 검증합니다.

### Implementation for User Story 2

- [x] T022 [US2] Implement date calculator service in src/services/date_calculator.py (calculate title date, payment date, date range)
- [x] T023 [US2] Implement conditional copy calculation method in src/services/mapping_engine.py (match riders, check conditions, copy only matching data)
- [x] T024 [US2] Implement date calculation method in src/services/mapping_engine.py (calculate dates based on week, format strings)
- [x] T025 [US2] Extend mapping engine to support conditional_copy and date_calculation methods in src/services/mapping_engine.py
- [x] T026 [US2] Update main window to handle date calculation mappings in src/gui/main_window.py
- [x] T027 [US2] Add error handling for conditional copy (rider name mismatch) in src/services/mapping_engine.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can process promotions and date calculations.

---

## Phase 5: User Story 4 - 주차별 오프셋 처리 및 월간정산 (Priority: P2)

**Goal**: 사용자가 여러 주차의 데이터를 한 번에 처리하거나, 월간정산 시트에 전체 주차의 고유 라이더 목록을 자동으로 생성합니다.

**Independent Test**: 2주차 데이터를 매핑할 때 행 오프셋이 +36으로 올바르게 적용되는지 확인합니다. 월간정산 시트에 모든 주차의 라이더 목록을 중복 제거하여 고유값만 추출하는지 검증합니다.

### Implementation for User Story 4

- [x] T028 [US4] Implement week offset calculation in src/utils/cell_utils.py (apply row offset based on week number)
- [x] T029 [US4] Extend mapping engine to apply week offsets to cell ranges in src/services/mapping_engine.py
- [x] T030 [US4] Implement unique extraction calculation method in src/services/mapping_engine.py (extract unique rider names from all weeks)
- [x] T031 [US4] Update main window to support "전체" week selection in src/gui/main_window.py (process all weeks 1-5)
- [x] T032 [US4] Implement monthly settlement sheet processing in src/services/mapping_engine.py (collect riders from all weeks, remove duplicates)
- [x] T033 [US4] Add monthly settlement generation to main window in src/gui/main_window.py

**Checkpoint**: At this point, User Stories 1, 2, AND 4 should all work independently. Users can process multiple weeks and generate monthly settlements.

---

## Phase 6: User Story 3 - 매핑 설정 관리 (Priority: P3)

**Goal**: 사용자가 매핑 정보를 GUI를 통해 수정하고 저장하여, 새로운 매핑 규칙을 추가하거나 기존 규칙을 변경할 수 있습니다.

**Independent Test**: 매핑 설정 수정 창에서 새로운 매핑 항목을 추가하고 저장한 후, 다음 매핑 실행 시 새로운 규칙이 적용되는지 확인합니다.

### Implementation for User Story 3

- [x] T034 [US3] Create mapping editor window GUI in src/gui/mapping_editor.py (table view, add/edit/delete buttons)
- [x] T035 [US3] Implement mapping configuration loading in src/gui/mapping_editor.py (load from JSON, display in table)
- [x] T036 [US3] Implement mapping configuration editing in src/gui/mapping_editor.py (add new mapping, edit existing, delete)
- [x] T037 [US3] Implement mapping configuration validation in src/gui/mapping_editor.py (validate cell ranges, calculation methods)
- [x] T038 [US3] Implement mapping configuration saving in src/gui/mapping_editor.py (save to JSON file)
- [x] T039 [US3] Add "매핑 설정 수정" button to main window in src/gui/main_window.py (open mapping editor)
- [x] T040 [US3] Update mapping engine to reload config after save in src/services/mapping_engine.py

**Checkpoint**: At this point, all user stories should be independently functional. Users can customize mapping rules through GUI.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T041 [P] Add comprehensive error messages for all error scenarios (file errors, mapping errors, data errors)
- [x] T042 [P] Implement error recovery (open mapping file in notepad on mapping errors, show user-friendly messages)
- [x] T043 [P] Add input validation for file selection (check file format, existence, permissions)
- [x] T044 [P] Add input validation for week selection (1-5 range, handle invalid input)
- [x] T045 [P] Implement file name auto-generation for branch files in src/utils/file_parser.py (generate from head office file info)
- [x] T046 [P] Add logging for all operations (file loading, mapping execution, errors)
- [x] T047 [P] Optimize performance (ensure 30s for single week, 3min for all weeks)
- [x] T048 [P] Add unit tests for core logic in tests/unit/ (mapping_engine, date_calculator, file_parser, cell_utils)
- [x] T049 [P] Add integration tests in tests/integration/ (excel_processor, mapping_workflow)
- [x] T050 [P] Add contract tests in tests/contract/ (mapping_rules validation)
- [x] T051 [P] Ensure 70% code coverage (run coverage.py, add tests as needed)
- [x] T052 [P] Code cleanup and refactoring (ensure code is self-documenting, minimal comments)
- [x] T053 [P] Documentation updates (update README.md, add usage examples)
- [x] T054 Run quickstart.md validation (test all scenarios from quickstart guide)

---

## Phase 8: Bug Fixes (Production Issues)

**Purpose**: Fix issues discovered during actual usage

- [x] T055 Fix branch file save to use correct filename format (쿠팡 MM월 W주차 정산표.xlsx) in src/services/mapping_engine.py
- [x] T056 Preserve formulas in branch file when saving in src/services/excel_processor.py (use data_only=False or preserve formulas)
- [x] T057 Fix title format for different title types in src/services/mapping_engine.py:
  - "기사별 정산 내역 타이틀" should be "기사별 정산 내역(MM월 W주차)"
  - "익일정산 신청 내역 타이틀" should be "익일정산 신청 내역(MM월 W주차)"
  - "지점 정산서 타이틀" should be "지점 정산서(MM월 W주차)"
  - "기사별 정산서 타이틀" should be "쿠팡 MM월 W주차 정산서\n(MM.DD ~ MM.DD)"
- [x] T058 Fix date range calculation for AL2 cell (기사별 정산서 타이틀) in src/services/date_calculator.py

---

## Phase 9: Additional Features & Fixes

**Purpose**: Additional features and fixes based on production usage

- [x] T059 Add msoffcrypto library support for password-protected Excel files in src/services/excel_processor.py (handle zip file format)
- [x] T060 Implement sign inversion for insurance fields (고용보험, 산재보험, 시간제보험) in src/services/mapping_engine.py (multiply by -1)
- [x] T061 Add monthly settlement rider name mapping logic in src/services/mapping_engine.py (extract unique riders from all weeks)
- [x] T062 Fix AL2 date range to start from October 29th in src/services/date_calculator.py (adjust week range calculation)

---

## Phase 10: Simple Sum Calculation Method

**Purpose**: Add simple_sum calculation method to sum values from multiple columns (adjacent or non-adjacent)

- [x] T063 [P] Add parse_multiple_ranges utility function in src/utils/cell_utils.py (parse comma-separated cell ranges like "K17:K46, M17:M46")
- [x] T064 Implement _execute_simple_sum method in src/services/mapping_engine.py (read from multiple ranges, sum row by row, write to branch file)
- [x] T065 Add simple_sum case handling in execute_mapping method in src/services/mapping_engine.py
- [x] T066 [P] Add unit tests for parse_multiple_ranges in tests/utils/test_cell_utils.py
- [x] T067 [P] Add unit tests for _execute_simple_sum in tests/services/test_mapping_engine.py (test adjacent columns, non-adjacent columns, empty values, None handling)
- [x] T068 Update mapping engine contract documentation in specs/1-settlement-automation/contracts/mapping-engine.md (add simple_sum method description)

---

## Phase 11: Conditional Sum Calculation Method

**Purpose**: Add conditional_sum calculation method to sum value_column values for rows matching condition

- [x] T069 Implement _execute_conditional_sum method in src/services/mapping_engine.py (sum value_column values for rows matching condition)
- [x] T070 Add conditional_sum case handling in execute_mapping method in src/services/mapping_engine.py
- [x] T071 [P] Add unit tests for _execute_conditional_sum in tests/unit/test_mapping_engine.py (test single match, multiple matches, non-matching condition, non-numeric values, week offset)
- [x] T072 Update mapping engine contract documentation in specs/1-settlement-automation/contracts/mapping-engine.md (add conditional_sum method description)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 mapping engine but independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Extends US1/US2 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent, but enhances all previous stories

### Within Each User Story

- Models before services
- Services before GUI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005)
- Foundational tasks marked [P] can run in parallel (T007, T008, T009)
- Once Foundational phase completes, User Stories 1, 2, 4 can start in parallel (different developers)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# These tasks can run in parallel (different files, no dependencies):
Task: "Implement Excel processor service in src/services/excel_processor.py"
Task: "Implement file loading logic in src/gui/main_window.py"
Task: "Implement progress display in src/gui/main_window.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 4 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP)
   - Developer B: User Story 2 (conditional/date logic)
   - Developer C: User Story 4 (offsets/monthly)
3. After US1, US2, US4 complete:
   - Developer A: User Story 3 (mapping editor)
   - Developer B: Polish tasks
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are included in Polish phase to meet 70% coverage goal per Constitution
- All tasks include exact file paths for clarity

