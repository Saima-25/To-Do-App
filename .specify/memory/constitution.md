<!--
  Sync Impact Report
  ==================
  Version change: 1.0.0 → 1.1.0

  Modified principles:
  - IV. In-Memory Storage → IV. JSON File Persistence (BREAKING CHANGE)

  Reason for change:
  - CLI commands run in separate processes, making per-process memory insufficient
  - Tasks must persist across command invocations (add → list → update → delete workflow)
  - JSON file storage required while maintaining "no external database" constraint

  Impact on existing artifacts:
  - specs/001-todo-cli-core/spec.md: MUST be updated (FR-005 and related requirements)
  - specs/001-todo-cli-core/plan.md: MUST be updated (storage architecture)
  - src/services/task_service.py: MUST add JSON load/save functionality
  - tests/: MUST add persistence tests and update fixtures

  Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ No updates needed (Constitution Check section generic)
  - .specify/templates/spec-template.md: ✅ No updates needed (compatible structure)
  - .specify/templates/tasks-template.md: ✅ No updates needed (compatible structure)

  Follow-up TODOs:
  - Update spec.md to reflect JSON persistence requirements
  - Update plan.md with new storage architecture
  - Implement TaskService JSON load/save methods
  - Add tests for file persistence
-->

# Todo CLI Constitution

## Core Principles

### I. Spec-First Development (NON-NEGOTIABLE)

All features MUST be fully specified before any planning, coding, or implementation begins.

- **Requirement → Specification → Plan → Tasks → Code**: This sequence is mandatory and irreversible
- No agent may write, suggest, or implement code during the specification phase
- All specifications MUST be versioned and stored in `/specs/<feature>/spec.md`
- Changes to approved specs MUST go through formal change control via the Spec Manager Agent
- Implementation is BLOCKED until specifications are approved by the spec-manager agent

**Rationale**: Spec-first ensures alignment between stakeholders, prevents scope creep, and maintains auditability for hackathon evaluation.

### II. CLI-First Interface

The Todo application MUST expose all functionality through a command-line interface.

- **Text I/O Protocol**: Commands accept arguments via stdin/args, output to stdout, errors to stderr
- **Human-Readable Output**: Default output MUST be human-readable and formatted for terminal display
- **Predictable Commands**: Follow standard CLI conventions (verb-noun patterns, `--help` flags, exit codes)
- **Error Messages**: MUST be actionable and include guidance on how to resolve the issue

**Rationale**: CLI-first ensures the application is scriptable, testable, and demonstrable for hackathon judges.

### III. Test-Driven Development

Tests MUST be written before implementation code.

- **Red-Green-Refactor**: Write failing test → Implement to pass → Refactor without breaking tests
- **Acceptance Tests**: Each user story MUST have corresponding acceptance tests derived from spec scenarios
- **Test Independence**: Each test MUST be independently runnable without side effects
- **Coverage**: All public functions and CLI commands MUST have test coverage

**Rationale**: TDD ensures code correctness, enables confident refactoring, and demonstrates engineering discipline.

### IV. JSON File Persistence

Task data MUST persist across CLI command executions using local JSON file storage.

- **No External Databases**: The application MUST NOT require external databases or network connections
- **JSON File Storage**: Tasks MUST be stored in a local JSON file (default: `~/.todo/tasks.json`)
- **Cross-Command Persistence**: Tasks MUST survive between CLI invocations to support workflow (add → list → update → delete)
- **Data Structure**: Use Python dictionaries/lists internally, serialize to JSON for persistence
- **Auto-Save**: Changes MUST be persisted immediately after each mutation operation
- **File Location**: Default to `~/.todo/tasks.json`, support `TODO_FILE` environment variable for custom paths

**Rationale**: CLI commands run in separate processes. JSON file persistence is required to maintain state across commands while keeping the implementation simple and avoiding external database dependencies.

### V. Clean Code & Simplicity

Code MUST be readable, maintainable, and minimal.

- **YAGNI**: Do not implement features not explicitly required by specifications
- **Single Responsibility**: Each module, class, and function MUST have one clear purpose
- **Meaningful Names**: Variables, functions, and modules MUST have descriptive, self-documenting names
- **No Premature Optimization**: Optimize only when specifications require specific performance targets
- **Minimal Dependencies**: Use Python standard library where possible; external packages MUST be justified

**Rationale**: Clean code reduces bugs, speeds up development, and impresses hackathon judges.

### VI. Auditability & Traceability

All work MUST be traceable from requirement to implementation.

- **PHR (Prompt History Records)**: Every significant interaction MUST be recorded in `history/prompts/`
- **ADR (Architecture Decision Records)**: Significant design decisions MUST be documented in `history/adr/`
- **Spec Traceability**: Each task MUST reference its parent spec requirement
- **Git History**: Commits MUST reference the spec/task being implemented

**Rationale**: Full traceability demonstrates engineering rigor and enables hackathon judges to follow the development process.

## Technology Stack

- **Language**: Python 3.13+
- **CLI Framework**: Standard `argparse` or `click` (to be decided during planning)
- **Testing**: `pytest` for unit and integration tests
- **Code Quality**: `ruff` for linting, `black` for formatting
- **Type Hints**: Required for all public interfaces
- **Documentation**: Docstrings for all public modules and functions

## Development Workflow

### Phase Progression

1. **Requirement Analysis**: Domain Agent clarifies user intent and business rules
2. **Specification**: Spec Manager creates versioned spec with acceptance criteria
3. **Planning**: Architecture and implementation approach documented
4. **Task Generation**: Actionable, testable tasks derived from plan
5. **Implementation**: TDD cycle (Red → Green → Refactor) for each task

### Agent Responsibilities

| Agent | Gate | Responsibility |
|-------|------|----------------|
| todo-domain-agent | Requirements | Clarify domain rules, user expectations, edge cases |
| todo-spec-manager | Specifications | Create, version, and enforce specs; block non-compliant work |
| python-cli-expert | Planning | Validate CLI design patterns and user experience |
| hackathon-judge-reviewer | All Phases | Audit compliance, traceability, and submission readiness |

### Quality Gates

- **Spec Gate**: No planning until spec is approved
- **Plan Gate**: No task generation until plan is reviewed
- **Implementation Gate**: No coding until tasks are defined
- **Merge Gate**: All tests pass, code reviewed, spec requirements met

## Governance

### Amendment Process

1. Propose change with rationale
2. Impact analysis on existing specs, plans, and code
3. Approval required from spec-manager agent
4. Version increment following semantic versioning
5. Update all dependent artifacts

### Versioning Policy

- **MAJOR**: Breaking changes to principles or workflow that invalidate existing artifacts
- **MINOR**: New principles, sections, or expanded guidance
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance

- This constitution supersedes all other development practices
- All PRs and reviews MUST verify compliance with these principles
- Violations MUST be documented and remediated before merge
- Complexity beyond these principles MUST be explicitly justified

**Version**: 1.1.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-29
