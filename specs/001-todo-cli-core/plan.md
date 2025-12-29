# Implementation Plan: Todo CLI Core Features

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Implement a command-line Todo application with five core operations: Add, List, Update, Delete, and Mark Complete/Incomplete. The application uses JSON file persistence to maintain tasks across CLI executions, follows CLI conventions with subcommands, and targets Python 3.13+ with pytest for testing. All 33 functional requirements from the spec will be implemented following TDD principles.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: `click` (CLI framework), `dataclasses` (built-in), `json` (built-in), `pathlib` (built-in)
**Storage**: JSON file at `~/.todo/tasks.json` (configurable via `TODO_FILE` env var) - per constitution v1.1.0
**Testing**: `pytest` with `pytest-cov` for coverage, `tempfile` for persistence tests
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project
**Performance Goals**: <5s task add, <2s list (up to 1000 tasks) per SC-001/SC-002
**Constraints**: No external databases, no network connections, JSON file only
**Scale/Scope**: Single user, ~1000 tasks max, 5 CLI commands

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-First Development | PASS | Spec complete at `spec.md` with 33 FRs, 5 user stories |
| II. CLI-First Interface | PASS | All operations via CLI subcommands, stdout/stderr separation |
| III. Test-Driven Development | PLANNED | Tests will be written before implementation per tasks |
| IV. JSON File Persistence | PASS | JSON storage at ~/.todo/tasks.json, no external databases |
| V. Clean Code & Simplicity | PLANNED | Single project structure, stdlib-only for persistence |
| VI. Auditability & Traceability | PASS | PHRs created, spec traceability maintained, constitution updated |

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
│   └── task.py          # Task dataclass with JSON serialization
├── services/
│   ├── __init__.py
│   └── task_service.py  # Business logic (CRUD + persistence)
├── cli/
│   ├── __init__.py
│   └── main.py          # Click CLI entry point
└── lib/
    ├── __init__.py
    ├── validators.py    # Input validation utilities
    └── storage.py       # JSON file I/O operations

tests/
├── __init__.py
├── conftest.py          # Shared fixtures (incl. temp storage)
├── unit/
│   ├── __init__.py
│   ├── test_task.py
│   ├── test_task_service.py
│   └── test_storage.py  # JSON persistence unit tests
└── integration/
    ├── __init__.py
    └── test_cli.py      # End-to-end CLI tests with persistence
```

**Structure Decision**: Single project structure selected per constitution (V. Clean Code & Simplicity). CLI application with clear separation: models (data), services (logic), cli (interface).

## Complexity Tracking

> No violations - structure follows constitution principles.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| CLI Framework | `click` over `argparse` | Better subcommand support, auto-help, less boilerplate |
| In-Memory Storage | `dict[int, Task]` | O(1) lookup by ID, simple iteration for list |
| File Storage | JSON at `~/.todo/tasks.json` | Human-readable, stdlib support, no external deps |
| ID Generation | Sequential counter (persisted) | Simple, unique, survives restarts, meets FR-003 & FR-033 |
| Save Strategy | Auto-save on mutations | Immediate persistence ensures FR-030, no explicit save needed |

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
TaskService
    ├── _tasks: dict[int, Task]      # ID → Task mapping (in-memory cache)
    ├── _next_id: int                # Auto-incrementing counter
    ├── _storage_path: Path          # JSON file location
    └── Methods:
        ├── __init__()               # Load from JSON on startup
        ├── _load()                  # Read tasks from JSON file
        ├── _save()                  # Write tasks to JSON file (auto-called on mutations)
        ├── add/update/delete/mark   # CRUD operations (auto-save after each)
        └── list_all/get             # Read-only operations (no save)
```

**JSON File Format**:
```json
{
  "next_id": 4,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "From farmers market",
      "status": "incomplete"
    },
    {
      "id": 2,
      "title": "Call dentist",
      "description": "",
      "status": "complete"
    }
  ]
}
```

**Storage Flow**:
1. CLI startup → TaskService.__init__() → _load() reads JSON
2. User command (e.g., `todo add`) → TaskService method → mutation + _save()
3. CLI exit → File already saved, no cleanup needed

### Error Handling Strategy

- Invalid ID → stderr message + exit code 1
- Empty title → stderr message + exit code 1
- Corrupted JSON → Log warning to stderr, start with empty task list
- File permission errors → stderr message + exit code 1
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
| Corrupted JSON file | Medium | Graceful fallback to empty task list, log warning to user |
| File permission errors | Medium | Clear error messages, validate permissions on init |
| Concurrent CLI instances | Low | Single-user assumption, last-write-wins documented |
| Click learning curve | Low | Well-documented, simple API |
| ID gaps after deletion | None | By design per FR-018 |
| Large JSON file (>1000 tasks) | Low | Performance goal handles up to 1000 tasks per SC-002 |
