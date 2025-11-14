# Implementation Plan: 본사 정산서 자동화 프로그램

**Branch**: `1-settlement-automation` | **Date**: 2025-11-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-settlement-automation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

본사 정산서 엑셀 파일의 데이터를 지점 정산서 양식에 자동으로 매핑하여 입력하는 데스크톱 애플리케이션을 개발합니다. Python과 PySide6을 사용하여 GUI 애플리케이션을 구현하고, openpyxl을 사용하여 엑셀 파일을 처리합니다. 매핑 규칙은 JSON 파일로 관리하여 코드 수정 없이 확장 가능하도록 설계합니다.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: 
- PySide6 (GUI 프레임워크)
- openpyxl (엑셀 파일 처리)
- json (표준 라이브러리, 매핑 설정 저장)

**Storage**: JSON 파일 (매핑 설정 및 config.json)  
**Testing**: pytest (단위 테스트, 통합 테스트)  
**Target Platform**: Windows, macOS, Linux (데스크톱 애플리케이션)  
**Project Type**: single (단일 데스크톱 애플리케이션)  
**Performance Goals**: 
- 단일 주차 처리: 30초 이내
- 전체 주차(5주차) 처리: 3분 이내
- 월간정산 생성: 10초 이내
- GUI 응답 시간: 1초 이내

**Constraints**: 
- 비밀번호 보호된 엑셀 파일 지원 필수
- 병합 셀 자동 감지 및 처리
- 최대 50행 데이터 처리 성능 유지
- 오프라인 동작 (인터넷 연결 불필요)

**Scale/Scope**: 
- 단일 사용자 데스크톱 애플리케이션
- 주당 1회 사용 (월 4-5회)
- 최대 50명 라이더 데이터 처리
- 5주차까지 주차별 데이터 처리

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Code Quality
- [x] 코드가 간결하고 읽기 쉬운가? - Python의 명확한 문법과 함수 분리를 통해 달성
- [x] 주석이 최소화되고 코드가 자체 설명적인가? - 의미 있는 변수명과 함수명 사용
- [x] 변수명과 함수명이 의미를 명확히 전달하는가? - 도메인 용어 사용 (mapping, settlement, rider 등)

### Testing
- [x] 핵심 로직에 대한 테스트 계획이 수립되었는가? - 매핑 엔진, 날짜 계산, 파일 파싱 등 핵심 로직 테스트 계획
- [x] 70% 코드 커버리지 목표를 달성할 수 있는가? - pytest와 coverage.py를 사용하여 달성 가능
- [x] 테스트 전략(단위/통합/계약)이 정의되었는가? - 단위 테스트(매핑 로직), 통합 테스트(파일 처리), 계약 테스트(매핑 규칙)

### User Experience
- [x] 인터페이스가 직관적인가? - 파일 선택, 주차 선택, 실행 버튼 등 명확한 UI 흐름
- [x] 1초 이내 응답 목표를 달성할 수 있는 설계인가? - 비동기 처리 및 백그라운드 작업으로 UI 응답성 유지
- [x] 사용자 작업 흐름이 최적화되었는가? - 3단계 작업 흐름: 파일 선택 → 주차 선택 → 실행

### Performance
- [x] 새로운 의존성 추가가 필요한가? (필요 시 정당화 필요) - PySide6 (GUI 필수), openpyxl (엑셀 처리 필수) - 두 라이브러리 모두 필수 기능 제공
- [x] 기존 라이브러리나 표준 라이브러리로 구현 가능한가? - 엑셀 처리는 표준 라이브러리로 불가능하므로 openpyxl 필요. GUI는 PySide6이 최소 의존성
- [x] 의존성 추가의 비용-편익 분석이 완료되었는가? - PySide6: 크로스 플랫폼 GUI 필수, openpyxl: 비밀번호 보호 파일 지원 및 병합 셀 처리 필수

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── mapping_config.py      # 매핑 설정 데이터 모델
│   ├── file_info.py           # 파일 정보 데이터 모델
│   └── processing_context.py  # 처리 컨텍스트 데이터 모델
├── services/
│   ├── excel_processor.py    # 엑셀 파일 처리 서비스
│   ├── mapping_engine.py     # 매핑 엔진 (핵심 로직)
│   ├── date_calculator.py    # 날짜 계산 서비스
│   └── config_manager.py     # 설정 파일 관리 서비스
├── gui/
│   ├── main_window.py        # 메인 윈도우
│   ├── mapping_editor.py     # 매핑 설정 편집 창
│   └── widgets/              # 재사용 가능한 위젯
└── utils/
    ├── file_parser.py        # 파일명 파싱 유틸리티
    └── cell_utils.py         # 셀 처리 유틸리티

tests/
├── unit/
│   ├── test_mapping_engine.py
│   ├── test_date_calculator.py
│   ├── test_file_parser.py
│   └── test_cell_utils.py
├── integration/
│   ├── test_excel_processor.py
│   └── test_mapping_workflow.py
└── contract/
    └── test_mapping_rules.py

config/
├── mapping.json              # 기본 매핑 설정
└── config.json               # 애플리케이션 설정 (비밀번호 등)
```

**Structure Decision**: 단일 프로젝트 구조를 선택했습니다. 데스크톱 애플리케이션이므로 프론트엔드/백엔드 분리가 필요 없으며, 모델-서비스-GUI 계층 구조로 명확하게 분리합니다. 테스트는 단위/통합/계약 테스트로 구성하여 70% 커버리지 목표를 달성합니다.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

Constitution Check를 통과했으며 추가 정당화가 필요한 위반 사항이 없습니다.

## Phase 0: Research 완료

**Output**: [research.md](./research.md)

주요 기술 선택 및 의사결정:
- 엑셀 처리: openpyxl (비밀번호 보호 파일 지원, 크로스 플랫폼)
- GUI: PySide6 (크로스 플랫폼, 비동기 처리 지원)
- 설정 저장: JSON (표준 라이브러리, 가독성)
- 테스트: pytest (표준 프레임워크, 커버리지 측정)

## Phase 1: Design 완료

**Outputs**:
- [data-model.md](./data-model.md): 엔티티 및 데이터 모델 정의
- [contracts/](./contracts/): 서비스 인터페이스 계약 정의
  - mapping-engine.md: 매핑 엔진 계약
  - excel-processor.md: 엑셀 처리 서비스 계약
  - date-calculator.md: 날짜 계산 서비스 계약
- [quickstart.md](./quickstart.md): 빠른 시작 가이드

### Constitution Check 재검증 (Phase 1 후)

모든 원칙을 준수하며 설계가 완료되었습니다:
- ✅ Code Quality: 명확한 계층 구조 및 인터페이스 정의
- ✅ Testing: 각 서비스별 테스트 계약 정의
- ✅ User Experience: 직관적인 3단계 워크플로우
- ✅ Performance: 최소 의존성 (PySide6, openpyxl만 사용)
