# Implementation Plan: Todo CLI Core Features

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Implement a command-line Todo application with five core operations: Add, List, Update, Delete, and Mark Complete/Incomplete. The application uses in-memory storage (session-based), follows CLI conventions with subcommands, and targets Python 3.13+ with pytest for testing. All 26 functional requirements from the spec will be implemented following TDD principles.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: `click` (CLI framework), `dataclasses` (built-in)
**Storage**: In-memory (Python dict/list) - session-based per constitution
**Testing**: `pytest` with `pytest-cov` for coverage
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project
**Performance Goals**: <5s task add, <2s list (up to 1000 tasks) per SC-001/SC-002
**Constraints**: No external databases, no network, no file persistence
**Scale/Scope**: Single user, ~1000 tasks max, 5 CLI commands

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-First Development | PASS | Spec complete at `spec.md` with 26 FRs, 5 user stories |
| II. CLI-First Interface | PASS | All operations via CLI subcommands, stdout/stderr separation |
| III. Test-Driven Development | PLANNED | Tests will be written before implementation per tasks |
| IV. In-Memory Storage | PASS | No external deps, session-based storage designed |
| V. Clean Code & Simplicity | PLANNED | Single project structure, minimal dependencies |
| VI. Auditability & Traceability | PASS | PHRs created, spec traceability maintained |

**Gate Result**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI contract)
│   └── cli-contract.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass
├── services/
│   ├── __init__.py
│   └── task_service.py  # Business logic (CRUD operations)
├── cli/
│   ├── __init__.py
│   └── main.py          # Click CLI entry point
└── lib/
    ├── __init__.py
    └── id_generator.py  # ID generation utility

tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_task.py
│   └── test_task_service.py
└── integration/
    ├── __init__.py
    └── test_cli.py      # End-to-end CLI tests
```

**Structure Decision**: Single project structure selected per constitution (V. Clean Code & Simplicity). CLI application with clear separation: models (data), services (logic), cli (interface).

## Complexity Tracking

> No violations - structure follows constitution principles.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| CLI Framework | `click` over `argparse` | Better subcommand support, auto-help, less boilerplate |
| Storage | `dict[int, Task]` | O(1) lookup by ID, simple iteration for list |
| ID Generation | Sequential counter | Simple, unique, meets FR-003 |

## Key Design Decisions

### CLI Command Structure

Using subcommand pattern (industry standard, per clarification):

```bash
todo add "Buy groceries" --description "From the farmers market"
todo list
todo complete 1
todo incomplete 1
todo update 1 --title "Buy organic groceries"
todo delete 1
```

### Task Storage Architecture

```
TaskService (singleton per session)
    └── _tasks: dict[int, Task]  # ID → Task mapping
    └── _next_id: int            # Auto-incrementing counter
```

### Error Handling Strategy

- Invalid ID → stderr message + exit code 1
- Empty title → stderr message + exit code 1
- Success → stdout message + exit code 0

## Dependencies

### Runtime Dependencies

| Package | Version | Purpose | Constitution Justification |
|---------|---------|---------|---------------------------|
| click | ^8.0 | CLI framework | Cleaner than argparse for subcommands |
| Python | 3.13+ | Runtime | Per constitution Technology Stack |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | ^8.0 | Testing framework |
| pytest-cov | ^4.0 | Coverage reporting |
| ruff | ^0.8 | Linting |
| black | ^24.0 | Formatting |

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Session data loss | Medium | Documented in spec; future persistence layer ready |
| Click learning curve | Low | Well-documented, simple API |
| ID gaps after deletion | None | By design per FR-018 |
