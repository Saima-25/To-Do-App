# Tasks: Todo CLI Core Features

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-contract.md

**Tests**: Tests are REQUIRED per constitution (III. Test-Driven Development). Tests MUST be written and FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
  - Create directories: `src/`, `src/models/`, `src/services/`, `src/cli/`, `src/lib/`
  - Create directories: `tests/`, `tests/unit/`, `tests/integration/`
  - Create `__init__.py` files in all Python packages
  - **FR Reference**: N/A (infrastructure)
  - **Acceptance**: All directories exist, Python can import from `src`

- [x] T002 Initialize Python project with pyproject.toml
  - Create `pyproject.toml` with project metadata
  - Add runtime dependency: `click>=8.0`
  - Add dev dependencies: `pytest>=8.0`, `pytest-cov>=4.0`, `ruff>=0.8`, `black>=24.0`
  - Configure `[project.scripts]` for `todo` entry point
  - **FR Reference**: FR-023 (CLI interface)
  - **Acceptance**: `pip install -e .` succeeds, `todo --help` runs

- [x] T003 [P] Configure linting and formatting tools
  - Add `ruff.toml` with Python 3.13 target
  - Add `pyproject.toml` black configuration
  - **FR Reference**: Constitution V (Clean Code)
  - **Acceptance**: `ruff check src/` and `black --check src/` pass

- [x] T004 [P] Create shared test fixtures in tests/conftest.py
  - Create `task_service` fixture returning fresh TaskService instance
  - Create `sample_task` fixture for common test data
  - **FR Reference**: Constitution III (TDD)
  - **Acceptance**: Fixtures importable in unit and integration tests

**Checkpoint**: Project setup complete - can run `pytest` (empty) and `todo --help`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create TaskStatus enum in src/models/task.py
  - Define `TaskStatus` enum with `INCOMPLETE` and `COMPLETE` values
  - Add string representations matching spec ("incomplete", "complete")
  - **FR Reference**: FR-004, FR-010, FR-011
  - **Acceptance**: `TaskStatus.INCOMPLETE.value == "incomplete"`

- [x] T006 Create Task dataclass in src/models/task.py
  - Define `Task` dataclass with fields: `id`, `title`, `description`, `status`
  - Add type hints per constitution
  - Default `description=""`, default `status=TaskStatus.INCOMPLETE`
  - **FR Reference**: FR-001, FR-002, FR-003, FR-004 (Key Entities)
  - **Acceptance**: `Task(id=1, title="Test")` creates valid task with defaults

- [x] T007 Create TaskService class skeleton in src/services/task_service.py
  - Initialize `_tasks: dict[int, Task]` and `_next_id: int = 1`
  - Add method stubs: `add()`, `get()`, `list_all()`, `update()`, `delete()`, `mark_complete()`, `mark_incomplete()`
  - **FR Reference**: FR-005 (in-memory storage)
  - **Acceptance**: TaskService can be instantiated, methods exist

- [x] T008 Create Click CLI group in src/cli/main.py
  - Define `@click.group()` for `todo` command
  - Add subcommand stubs: `add`, `list`, `complete`, `incomplete`, `update`, `delete`
  - Wire entry point to pyproject.toml
  - **FR Reference**: FR-023, FR-024
  - **Acceptance**: `todo --help` shows all subcommands

- [x] T009 Create validation utilities in src/lib/validators.py
  - `validate_title(title: str) -> str`: Strip, check empty, check length <=500
  - `validate_description(description: str) -> str`: Check length <=2000
  - Raise `ValueError` with specific messages per data-model.md V001-V003
  - **FR Reference**: FR-001, FR-016, FR-021
  - **Acceptance**: Validators raise correct errors for invalid input

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Task (Priority: P1)

**Goal**: Users can add tasks with title and optional description

**Independent Test**: Run `todo add "Test"` and verify task creation message

### Tests for User Story 1 (REQUIRED - TDD)

> **Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Unit test for TaskService.add() in tests/unit/test_task_service.py
  - Test: add task with title only → returns Task with ID, status incomplete
  - Test: add task with title and description → both stored
  - Test: add multiple tasks → unique sequential IDs
  - Test: add task with empty title → raises ValueError
  - Test: add task with whitespace-only title → raises ValueError
  - Test: add task with title >500 chars → raises ValueError
  - **FR Reference**: FR-001, FR-002, FR-003, FR-004, FR-021
  - **Acceptance**: Tests written, all FAIL (red phase)

- [x] T011 [P] [US1] Integration test for `todo add` in tests/integration/test_cli.py
  - Test: `todo add "Buy groceries"` → exit 0, stdout contains "Task 1 added"
  - Test: `todo add "Task" -d "Description"` → exit 0, description stored
  - Test: `todo add ""` → exit 1, stderr contains error
  - **FR Reference**: FR-023, FR-025, FR-026
  - **Acceptance**: Tests written, all FAIL (red phase)

### Implementation for User Story 1

- [x] T012 [US1] Implement TaskService.add() in src/services/task_service.py
  - Validate title using validators.validate_title()
  - Validate description using validators.validate_description()
  - Generate ID using `_next_id`, increment counter
  - Create Task instance with defaults
  - Store in `_tasks` dict
  - Return created Task
  - **FR Reference**: FR-001, FR-002, FR-003, FR-004, FR-005
  - **Acceptance**: T010 tests pass (green phase)

- [x] T013 [US1] Implement `todo add` command in src/cli/main.py
  - Accept TITLE as required argument
  - Accept `--description` / `-d` as optional argument
  - Call TaskService.add()
  - Output success to stdout: "Task {id} added: \"{title}\""
  - Handle ValueError → stderr + exit 1
  - **FR Reference**: FR-023, FR-024, FR-025, FR-026
  - **Acceptance**: T011 tests pass (green phase)

**Checkpoint**: User Story 1 complete - `todo add` works end-to-end

---

## Phase 4: User Story 2 - View/List Tasks (Priority: P1)

**Goal**: Users can view all tasks in readable format

**Independent Test**: Add tasks, run `todo list`, verify output format

### Tests for User Story 2 (REQUIRED - TDD)

- [x] T014 [P] [US2] Unit test for TaskService.list_all() in tests/unit/test_task_service.py
  - Test: empty service → returns empty list
  - Test: multiple tasks → returns all tasks
  - Test: tasks returned in ID order (ascending)
  - **FR Reference**: FR-006, FR-008
  - **Acceptance**: Tests written, all FAIL (red phase)

- [x] T015 [P] [US2] Integration test for `todo list` in tests/integration/test_cli.py
  - Test: no tasks → stdout contains "No tasks found"
  - Test: with tasks → shows ID, title, description, status
  - Test: mixed statuses → status clearly displayed
  - Test: output ordered by ID
  - **FR Reference**: FR-006, FR-007, FR-008, FR-009
  - **Acceptance**: Tests written, all FAIL (red phase)

### Implementation for User Story 2

- [x] T016 [US2] Implement TaskService.list_all() in src/services/task_service.py
  - Return `sorted(self._tasks.values(), key=lambda t: t.id)`
  - **FR Reference**: FR-006, FR-008
  - **Acceptance**: T014 tests pass (green phase)

- [x] T017 [US2] Implement `todo list` command in src/cli/main.py
  - Call TaskService.list_all()
  - If empty → output "No tasks found. Add a task with: todo add \"Your task title\""
  - If tasks exist → format as table with columns: ID, Status, Title, Description
  - Use fixed-width columns for readability
  - **FR Reference**: FR-006, FR-007, FR-008, FR-009, FR-023
  - **Acceptance**: T015 tests pass (green phase)

**Checkpoint**: User Stories 1 & 2 complete - add and list work together

---

## Phase 5: User Story 3 - Mark Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task status

**Independent Test**: Add task, run `todo complete 1`, verify status change in list

### Tests for User Story 3 (REQUIRED - TDD)

- [x] T018 [P] [US3] Unit test for TaskService.mark_complete/incomplete() in tests/unit/test_task_service.py
  - Test: mark_complete(id) → status changes to COMPLETE
  - Test: mark_incomplete(id) → status changes to INCOMPLETE
  - Test: mark preserves title and description
  - Test: mark non-existent ID → raises ValueError
  - **FR Reference**: FR-010, FR-011, FR-012, FR-020
  - **Acceptance**: Tests written, all FAIL (red phase)

- [x] T019 [P] [US3] Integration test for `todo complete/incomplete` in tests/integration/test_cli.py
  - Test: `todo complete 1` → exit 0, stdout confirms
  - Test: `todo incomplete 1` → exit 0, stdout confirms
  - Test: `todo complete 99` → exit 1, stderr error
  - Test: list shows updated status after marking
  - **FR Reference**: FR-010, FR-011, FR-020, FR-025, FR-026
  - **Acceptance**: Tests written, all FAIL (red phase)

### Implementation for User Story 3

- [x] T020 [US3] Implement TaskService.get() in src/services/task_service.py
  - Return `self._tasks.get(id)` or None
  - **FR Reference**: FR-020 (needed for lookup)
  - **Acceptance**: Can retrieve task by ID

- [x] T021 [US3] Implement TaskService.mark_complete() and mark_incomplete() in src/services/task_service.py
  - Get task by ID, raise ValueError if not found
  - Update status field only
  - Return updated Task
  - **FR Reference**: FR-010, FR-011, FR-012
  - **Acceptance**: T018 tests pass (green phase)

- [x] T022 [US3] Implement `todo complete` and `todo incomplete` commands in src/cli/main.py
  - Accept ID as required argument (integer)
  - Call appropriate TaskService method
  - Output success: "Task {id} marked as complete/incomplete"
  - Handle ValueError → stderr "Error: Task with ID {id} not found" + exit 1
  - **FR Reference**: FR-010, FR-011, FR-020, FR-025, FR-026
  - **Acceptance**: T019 tests pass (green phase)

**Checkpoint**: User Stories 1, 2, 3 complete - core todo functionality works

---

## Phase 6: User Story 4 - Update Task (Priority: P3)

**Goal**: Users can update task title or description

**Independent Test**: Add task, run `todo update 1 --title "New"`, verify change in list

### Tests for User Story 4 (REQUIRED - TDD)

- [x] T023 [P] [US4] Unit test for TaskService.update() in tests/unit/test_task_service.py
  - Test: update title only → title changes, others preserved
  - Test: update description only → description changes, others preserved
  - Test: update both → both change
  - Test: update with empty title → raises ValueError
  - Test: update non-existent ID → raises ValueError
  - Test: ID cannot be changed
  - **FR Reference**: FR-013, FR-014, FR-015, FR-016, FR-020
  - **Acceptance**: Tests written, all FAIL (red phase)

- [x] T024 [P] [US4] Integration test for `todo update` in tests/integration/test_cli.py
  - Test: `todo update 1 --title "New"` → exit 0, confirms update
  - Test: `todo update 1 -d "New desc"` → exit 0
  - Test: `todo update 1 --title "" ` → exit 1, error
  - Test: `todo update 99 --title "X"` → exit 1, not found error
  - Test: no options provided → exit 1, error message
  - **FR Reference**: FR-013, FR-014, FR-020, FR-021, FR-025
  - **Acceptance**: Tests written, all FAIL (red phase)

### Implementation for User Story 4

- [x] T025 [US4] Implement TaskService.update() in src/services/task_service.py
  - Get task by ID, raise ValueError if not found
  - If title provided, validate and update
  - If description provided, validate and update
  - Return updated Task
  - **FR Reference**: FR-013, FR-014, FR-015, FR-016
  - **Acceptance**: T023 tests pass (green phase)

- [x] T026 [US4] Implement `todo update` command in src/cli/main.py
  - Accept ID as required argument
  - Accept `--title` / `-t` as optional
  - Accept `--description` / `-d` as optional
  - Require at least one option, else error
  - Call TaskService.update()
  - Output: "Task {id} updated"
  - Handle errors → stderr + exit 1
  - **FR Reference**: FR-013, FR-014, FR-020, FR-021, FR-025, FR-026
  - **Acceptance**: T024 tests pass (green phase)

**Checkpoint**: User Stories 1-4 complete - CRUD minus Delete works

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks

**Independent Test**: Add task, run `todo delete 1`, verify task gone from list

### Tests for User Story 5 (REQUIRED - TDD)

- [x] T027 [P] [US5] Unit test for TaskService.delete() in tests/unit/test_task_service.py
  - Test: delete existing task → returns True, task removed
  - Test: delete non-existent ID → raises ValueError
  - Test: other tasks' IDs unchanged after deletion
  - Test: deleted task not in list_all()
  - **FR Reference**: FR-017, FR-018, FR-019, FR-020
  - **Acceptance**: Tests written, all FAIL (red phase)

- [x] T028 [P] [US5] Integration test for `todo delete` in tests/integration/test_cli.py
  - Test: `todo delete 1` → exit 0, confirms deletion
  - Test: `todo delete 99` → exit 1, not found error
  - Test: list after delete → task gone
  - **FR Reference**: FR-017, FR-020, FR-025, FR-026
  - **Acceptance**: Tests written, all FAIL (red phase)

### Implementation for User Story 5

- [x] T029 [US5] Implement TaskService.delete() in src/services/task_service.py
  - Check if ID exists, raise ValueError if not
  - Remove from `_tasks` dict
  - Return True
  - **FR Reference**: FR-017, FR-018, FR-019
  - **Acceptance**: T027 tests pass (green phase)

- [x] T030 [US5] Implement `todo delete` command in src/cli/main.py
  - Accept ID as required argument
  - Call TaskService.delete()
  - Output: "Task {id} deleted"
  - Handle ValueError → stderr + exit 1
  - **FR Reference**: FR-017, FR-020, FR-025, FR-026
  - **Acceptance**: T028 tests pass (green phase)

**Checkpoint**: All 5 user stories complete - full CRUD functionality

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and validation

- [x] T031 [P] Add comprehensive --help text to all commands
  - Add docstrings to all Click commands (used for --help)
  - Ensure consistent formatting
  - **FR Reference**: FR-024
  - **Acceptance**: `todo <cmd> --help` shows useful documentation

- [x] T032 [P] Validate exit codes across all commands
  - Audit all error paths return exit code 1
  - Audit all success paths return exit code 0
  - **FR Reference**: FR-025
  - **Acceptance**: Exit codes consistent per cli-contract.md

- [x] T033 Run full test suite with coverage
  - Execute `pytest --cov=src --cov-report=term-missing`
  - Target: 100% coverage on services, 90%+ overall
  - **FR Reference**: Constitution III (TDD)
  - **Acceptance**: Coverage meets targets, all tests pass

- [x] T034 Run quickstart.md validation
  - Execute all commands from quickstart.md manually
  - Verify output matches documented examples
  - **FR Reference**: SC-007
  - **Acceptance**: Quickstart works as documented

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ──► BLOCKS all user stories
    ↓
Phase 3 (US1: Add)  ←─┐
    ↓                 │
Phase 4 (US2: List)   │ Can run in parallel after Phase 2
    ↓                 │
Phase 5 (US3: Mark)  ←┘
    ↓
Phase 6 (US4: Update) ← Depends on US1
    ↓
Phase 7 (US5: Delete) ← Depends on US1
    ↓
Phase 8 (Polish)
```

### Within Each User Story

1. Tests MUST be written and FAIL before implementation (TDD red phase)
2. Implementation makes tests pass (TDD green phase)
3. Refactor if needed without breaking tests (TDD refactor phase)

### Parallel Opportunities

- T003, T004 can run in parallel (different files)
- T010, T011 can run in parallel (test files)
- T014, T015 can run in parallel
- T018, T019 can run in parallel
- T023, T024 can run in parallel
- T027, T028 can run in parallel
- T031, T032 can run in parallel

---

## Requirement Traceability Matrix

| FR | Task(s) | User Story |
|----|---------|------------|
| FR-001 | T009, T010, T012 | US1 |
| FR-002 | T010, T012 | US1 |
| FR-003 | T006, T010, T012 | US1 |
| FR-004 | T005, T006, T010, T012 | US1 |
| FR-005 | T007, T012 | US1 |
| FR-006 | T014, T016 | US2 |
| FR-007 | T015, T017 | US2 |
| FR-008 | T014, T016, T017 | US2 |
| FR-009 | T015, T017 | US2 |
| FR-010 | T005, T018, T021 | US3 |
| FR-011 | T005, T018, T021 | US3 |
| FR-012 | T018, T021 | US3 |
| FR-013 | T023, T025 | US4 |
| FR-014 | T023, T025 | US4 |
| FR-015 | T023, T025 | US4 |
| FR-016 | T009, T023, T025 | US4 |
| FR-017 | T027, T029 | US5 |
| FR-018 | T027, T029 | US5 |
| FR-019 | T027, T029 | US5 |
| FR-020 | T018, T021, T022, T023, T025, T026, T027, T029, T030 | US3-5 |
| FR-021 | T009, T010, T013, T023, T026 | US1, US4 |
| FR-022 | T010, T012, T023, T025 | US1, US4 |
| FR-023 | T002, T008, T013, T017, T022, T026, T030 | All |
| FR-024 | T008, T031 | All |
| FR-025 | T011, T019, T024, T028, T032 | All |
| FR-026 | T011, T013, T017, T019, T022, T024, T026, T028, T030 | All |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD red phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
