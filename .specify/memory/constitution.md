<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial creation)
- Modified principles: N/A (new constitution)
- Added sections:
  - Core Principles (4 principles: Code Quality, Testing, User Experience, Performance)
  - Development Standards
  - Governance
- Removed sections: N/A
- Templates requiring updates:
  - ✅ plan-template.md (Constitution Check section exists, will reference new principles)
  - ✅ spec-template.md (no direct constitution references, compatible)
  - ✅ tasks-template.md (no direct constitution references, compatible)
- Follow-up TODOs: None
-->

# Coupang Receipt Constitution

## Core Principles

### I. Code Quality

코드는 간결하고 읽기 쉬운 형태로 작성되어야 합니다. 주석은 최소화하고, 코드 자체가 의도를 명확히 설명하도록 작성해야 합니다. 변수명과 함수명은 의미를 명확히 전달해야 하며, 복잡한 로직은 작은 함수로 분리하여 가독성을 높여야 합니다.

**Rationale**: 읽기 쉬운 코드는 유지보수성을 높이고 버그 발생 가능성을 줄입니다. 자체 설명적인 코드는 새로운 팀원의 온보딩 시간을 단축하고 코드 리뷰 효율을 향상시킵니다.

### II. Testing (NON-NEGOTIABLE)

핵심 로직은 반드시 테스트를 작성해야 합니다. 프로젝트 전체 코드 커버리지는 최소 70%를 목표로 합니다. 테스트는 단위 테스트, 통합 테스트, 계약 테스트를 포함할 수 있으며, 각 테스트는 독립적으로 실행 가능해야 합니다.

**Rationale**: 테스트는 코드의 신뢰성을 보장하고 리팩토링 시 회귀 버그를 방지합니다. 70% 커버리지 목표는 핵심 로직의 안정성을 보장하면서도 과도한 테스트 작성 부담을 방지합니다.

### III. User Experience

인터페이스는 직관적이고 빠르게 동작해야 합니다. 모든 사용자 상호작용은 1초 이내에 응답해야 합니다. 사용자가 원하는 작업을 최소한의 클릭이나 입력으로 완료할 수 있어야 합니다.

**Rationale**: 빠른 응답 시간은 사용자 만족도를 높이고 이탈률을 줄입니다. 직관적인 인터페이스는 학습 곡선을 낮추고 사용자 생산성을 향상시킵니다.

### IV. Performance

불필요한 라이브러리 사용을 금지합니다. 최소한의 의존성으로 기능을 구현해야 하며, 새로운 라이브러리를 추가하기 전에 기존 도구나 표준 라이브러리로 구현 가능한지 검토해야 합니다. 의존성 추가 시 반드시 명확한 이유와 비용-편익 분석이 필요합니다.

**Rationale**: 최소한의 의존성은 보안 취약점 노출을 줄이고, 번들 크기를 작게 유지하며, 업그레이드 복잡도를 낮춥니다. 또한 프로젝트의 장기적인 유지보수성을 향상시킵니다.

## Development Standards

### Code Review Requirements

- 모든 코드 변경은 PR을 통해 리뷰되어야 합니다
- Constitution 준수 여부를 리뷰에서 확인해야 합니다
- 코드 커버리지 목표(70%) 미달 시 리뷰 승인 불가

### Quality Gates

- 테스트 커버리지 70% 이상 달성 필수
- 모든 테스트 통과 필수
- 성능 목표(1초 이내 응답) 달성 확인 필수
- 새로운 의존성 추가 시 승인 프로세스 필수

## Governance

이 Constitution은 프로젝트의 모든 개발 활동에 우선 적용됩니다. Constitution의 수정은 다음 절차를 따라야 합니다:

1. **수정 제안**: Constitution 수정 사항을 명확히 문서화
2. **영향 분석**: 수정 사항이 기존 원칙과 충돌하지 않는지 검토
3. **템플릿 동기화**: 관련 템플릿 파일들(plan-template.md, spec-template.md, tasks-template.md 등) 업데이트
4. **버전 관리**: Semantic Versioning 규칙에 따라 버전 업데이트
   - MAJOR: 원칙 제거 또는 호환되지 않는 변경
   - MINOR: 새로운 원칙 추가 또는 기존 원칙의 중요한 확장
   - PATCH: 명확화, 문구 수정, 오타 수정 등 비의미적 변경
5. **승인 및 적용**: 팀 승인 후 적용 및 문서화

모든 PR과 코드 리뷰는 Constitution 준수를 확인해야 합니다. 원칙 위반 시 명확한 정당화가 필요하며, Complexity Tracking에 기록되어야 합니다.

**Version**: 1.0.0 | **Ratified**: 2025-11-14 | **Last Amended**: 2025-11-14
