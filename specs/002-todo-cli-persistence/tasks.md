# Tasks: Todo CLI with File-Based Persistence

**Input**: Design documents from `/specs/002-todo-cli-persistence/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-contract.md

**Tests**: Following TDD approach per constitution Principle III - tests written BEFORE implementation

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/, tests/, specs/)
- [ ] T002 Initialize Python project with pyproject.toml and dependencies (click>=8.0, pytest>=8.0, pytest-cov>=4.0, ruff>=0.8, black>=24.0)
- [ ] T003 [P] Configure ruff for linting in pyproject.toml
- [ ] T004 [P] Configure black for formatting in pyproject.toml
- [ ] T005 [P] Configure pytest in pyproject.toml with coverage settings
- [ ] T006 Create all __init__.py files for src/ and tests/ modules

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Create TaskStatus enum in src/models/task.py (INCOMPLETE, COMPLETE values)
- [ ] T008 [P] Create validation constants in src/lib/validators.py (MAX_TITLE_LENGTH=500, MAX_DESCRIPTION_LENGTH=2000)
- [ ] T009 Create pytest fixtures in tests/conftest.py (temp_storage_path, task_service)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks Across Sessions (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks and view them across CLI sessions with JSON persistence

**Independent Test**: Add a task in one CLI invocation, close terminal, verify task appears when listing in new invocation

### Tests for User Story 1 (TDD: Write FIRST, ensure they FAIL)

- [ ] T010 [P] [US1] Write failing unit test for Task dataclass creation in tests/unit/test_task.py
- [ ] T011 [P] [US1] Write failing unit test for Task.to_dict() serialization in tests/unit/test_task.py
- [ ] T012 [P] [US1] Write failing unit test for Task.from_dict() deserialization in tests/unit/test_task.py
- [ ] T013 [P] [US1] Write failing unit test for validate_title() with valid input in tests/unit/test_validators.py
- [ ] T014 [P] [US1] Write failing unit test for validate_title() with empty/whitespace in tests/unit/test_validators.py
- [ ] T015 [P] [US1] Write failing unit test for validate_title() with >500 chars in tests/unit/test_validators.py
- [ ] T016 [P] [US1] Write failing unit test for validate_description() in tests/unit/test_validators.py
- [ ] T017 [P] [US1] Write failing unit test for storage.save() in tests/unit/test_storage.py
- [ ] T018 [P] [US1] Write failing unit test for storage.load() with missing file in tests/unit/test_storage.py
- [ ] T019 [P] [US1] Write failing unit test for storage.load() with corrupted JSON in tests/unit/test_storage.py
- [ ] T020 [P] [US1] Write failing unit test for TaskService.add() in tests/unit/test_task_service.py
- [ ] T021 [P] [US1] Write failing unit test for TaskService.list_all() in tests/unit/test_task_service.py
- [ ] T022 [P] [US1] Write failing integration test for `todo add` command in tests/integration/test_cli.py
- [ ] T023 [P] [US1] Write failing integration test for `todo list` command in tests/integration/test_cli.py
- [ ] T024 [P] [US1] Write failing integration test for cross-session persistence in tests/integration/test_cli.py

### Implementation for User Story 1

- [ ] T025 [P] [US1] Implement Task dataclass with fields (id, title, description, status) in src/models/task.py
- [ ] T026 [P] [US1] Implement Task.to_dict() method in src/models/task.py
- [ ] T027 [P] [US1] Implement Task.from_dict() classmethod in src/models/task.py
- [ ] T028 [P] [US1] Implement validate_title() function in src/lib/validators.py (strip, length, whitespace checks)
- [ ] T029 [P] [US1] Implement validate_description() function in src/lib/validators.py (length check)
- [ ] T030 [P] [US1] Implement get_storage_path() helper in src/lib/storage.py (handle TODO_FILE env var, default ~/.todo/tasks.json)
- [ ] T031 [P] [US1] Implement save() function in src/lib/storage.py (atomic write, create directory if needed)
- [ ] T032 [P] [US1] Implement load() function in src/lib/storage.py (handle missing file, corrupted JSON gracefully)
- [ ] T033 [US1] Implement TaskService.__init__() with storage path and load in src/services/task_service.py (depends on T030-T032)
- [ ] T034 [US1] Implement TaskService.add() method in src/services/task_service.py (validate, generate ID, save)
- [ ] T035 [US1] Implement TaskService.list_all() method in src/services/task_service.py (return sorted by ID)
- [ ] T036 [US1] Create Click CLI group in src/cli/main.py with version and help text
- [ ] T037 [US1] Implement `todo add` command in src/cli/main.py (use TaskService, handle errors, exit codes)
- [ ] T038 [US1] Implement `todo list` command in src/cli/main.py (format output, handle empty list)
- [ ] T039 [US1] Verify all T010-T024 tests now PASS

**Checkpoint**: User Story 1 complete - users can add/view tasks with persistence ✅

---

## Phase 4: User Story 2 - Mark Tasks Complete Persistently (Priority: P1)

**Goal**: Users can mark tasks complete/incomplete with status persisting across sessions

**Independent Test**: Add task, mark complete in one session, verify status persists in new session

### Tests for User Story 2 (TDD: Write FIRST, ensure they FAIL)

- [ ] T040 [P] [US2] Write failing unit test for TaskService.get() in tests/unit/test_task_service.py
- [ ] T041 [P] [US2] Write failing unit test for TaskService.mark_complete() in tests/unit/test_task_service.py
- [ ] T042 [P] [US2] Write failing unit test for TaskService.mark_incomplete() in tests/unit/test_task_service.py
- [ ] T043 [P] [US2] Write failing unit test for mark_complete() with non-existent ID in tests/unit/test_task_service.py
- [ ] T044 [P] [US2] Write failing integration test for `todo complete` command in tests/integration/test_cli.py
- [ ] T045 [P] [US2] Write failing integration test for `todo incomplete` command in tests/integration/test_cli.py
- [ ] T046 [P] [US2] Write failing integration test for status persistence across sessions in tests/integration/test_cli.py

### Implementation for User Story 2

- [ ] T047 [P] [US2] Implement TaskService.get() method in src/services/task_service.py
- [ ] T048 [P] [US2] Implement TaskService.mark_complete() method in src/services/task_service.py (validate ID exists, update status, save)
- [ ] T049 [P] [US2] Implement TaskService.mark_incomplete() method in src/services/task_service.py (validate ID exists, update status, save)
- [ ] T050 [US2] Implement `todo complete` command in src/cli/main.py (use mark_complete, handle errors)
- [ ] T051 [US2] Implement `todo incomplete` command in src/cli/main.py (use mark_incomplete, handle errors)
- [ ] T052 [US2] Verify all T040-T046 tests now PASS

**Checkpoint**: User Story 2 complete - status management with persistence ✅

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Users can update task title/description with changes persisting across sessions

**Independent Test**: Add task, update details in one session, verify updates persist in new session

### Tests for User Story 3 (TDD: Write FIRST, ensure they FAIL)

- [ ] T053 [P] [US3] Write failing unit test for TaskService.update() with title only in tests/unit/test_task_service.py
- [ ] T054 [P] [US3] Write failing unit test for TaskService.update() with description only in tests/unit/test_task_service.py
- [ ] T055 [P] [US3] Write failing unit test for TaskService.update() with both title and description in tests/unit/test_task_service.py
- [ ] T056 [P] [US3] Write failing unit test for update() with empty title validation in tests/unit/test_task_service.py
- [ ] T057 [P] [US3] Write failing unit test for update() with non-existent ID in tests/unit/test_task_service.py
- [ ] T058 [P] [US3] Write failing integration test for `todo update` command in tests/integration/test_cli.py
- [ ] T059 [P] [US3] Write failing integration test for update persistence across sessions in tests/integration/test_cli.py

### Implementation for User Story 3

- [ ] T060 [P] [US3] Implement TaskService.update() method in src/services/task_service.py (validate ID exists, validate new values, update, save)
- [ ] T061 [US3] Implement `todo update` command in src/cli/main.py (require at least one option, handle errors)
- [ ] T062 [US3] Verify all T053-T059 tests now PASS

**Checkpoint**: User Story 3 complete - task update functionality ✅

---

## Phase 6: User Story 4 - Delete Tasks Permanently (Priority: P2)

**Goal**: Users can delete tasks with deletion persisting across sessions

**Independent Test**: Add tasks, delete one in one session, verify it doesn't appear in new session

### Tests for User Story 4 (TDD: Write FIRST, ensure they FAIL)

- [ ] T063 [P] [US4] Write failing unit test for TaskService.delete() in tests/unit/test_task_service.py
- [ ] T064 [P] [US4] Write failing unit test for delete() preserving other task IDs in tests/unit/test_task_service.py
- [ ] T065 [P] [US4] Write failing unit test for delete() with non-existent ID in tests/unit/test_task_service.py
- [ ] T066 [P] [US4] Write failing integration test for `todo delete` command in tests/integration/test_cli.py
- [ ] T067 [P] [US4] Write failing integration test for delete persistence across sessions in tests/integration/test_cli.py

### Implementation for User Story 4

- [ ] T068 [P] [US4] Implement TaskService.delete() method in src/services/task_service.py (validate ID exists, remove from dict, save)
- [ ] T069 [US4] Implement `todo delete` command in src/cli/main.py (use delete, handle errors)
- [ ] T070 [US4] Verify all T063-T067 tests now PASS

**Checkpoint**: User Story 4 complete - task deletion functionality ✅

---

## Phase 7: User Story 5 - Configure Storage Location (Priority: P3)

**Goal**: Users can configure custom storage location via TODO_FILE environment variable

**Independent Test**: Set TODO_FILE to custom path, add tasks, verify they're stored at custom location

### Tests for User Story 5 (TDD: Write FIRST, ensure they FAIL)

- [ ] T071 [P] [US5] Write failing unit test for get_storage_path() with no env var in tests/unit/test_storage.py
- [ ] T072 [P] [US5] Write failing unit test for get_storage_path() with TODO_FILE set in tests/unit/test_storage.py
- [ ] T073 [P] [US5] Write failing unit test for storage path with tilde expansion in tests/unit/test_storage.py
- [ ] T074 [P] [US5] Write failing integration test for custom storage location in tests/integration/test_cli.py
- [ ] T075 [P] [US5] Write failing integration test for auto-creating custom storage directory in tests/integration/test_cli.py

### Implementation for User Story 5

- [ ] T076 [US5] Enhance get_storage_path() in src/lib/storage.py to check TODO_FILE env var (if not already complete from T030)
- [ ] T077 [US5] Verify all T071-T075 tests now PASS
- [ ] T078 [US5] Update CLI --help text in src/cli/main.py to document TODO_FILE environment variable

**Checkpoint**: User Story 5 complete - configurable storage location ✅

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements and edge case handling

- [ ] T079 [P] Add unit tests for edge cases (max length titles/descriptions, unicode characters, special chars in paths)
- [ ] T080 [P] Add integration tests for error scenarios (permission denied, disk full simulation)
- [ ] T081 [P] Add performance test for 1000 tasks (verify <2s list time per SC-003)
- [ ] T082 [P] Enhance error messages to include actionable guidance per FR-033
- [ ] T083 [P] Add logging for corrupted JSON file warnings per FR-034
- [ ] T084 Run full test suite with coverage (target 100% per constitution)
- [ ] T085 Run linting (ruff) and formatting (black) checks
- [ ] T086 Verify all 38 functional requirements from spec.md are met
- [ ] T087 Test cross-session workflow: add → close terminal → list → complete → close → list
- [ ] T088 Verify CLI help text for all commands per FR-036
- [ ] T089 Create entry point script and verify `todo --version` works

**Final Checkpoint**: All user stories complete, polish done, ready for production ✅

---

## Implementation Strategy

### MVP Scope (Deliver First)
**Phase 3 ONLY** - User Story 1: Add and View Tasks
- Provides immediate value: users can create and track tasks
- Foundation for all other features
- Independently testable and deliverable

### Incremental Delivery Order
1. **MVP**: Phase 3 (US1) - Add/View ← Deploy this first!
2. **Core Features**: Phase 4 (US2) - Mark Complete
3. **Enhanced Features**: Phase 5 (US3) - Update, Phase 6 (US4) - Delete
4. **Advanced Features**: Phase 7 (US5) - Configure Storage
5. **Polish**: Phase 8 - Quality improvements

### Dependencies Between Stories
```
Phase 1 (Setup)
    ↓
Phase 2 (Foundation)
    ↓
    ├─→ Phase 3 (US1: Add/View) [MVP] ← No dependencies, deliver first
    ├─→ Phase 4 (US2: Complete)        ← Requires US1 (needs tasks to mark)
    ├─→ Phase 5 (US3: Update)          ← Requires US1 (needs tasks to update)
    ├─→ Phase 6 (US4: Delete)          ← Requires US1 (needs tasks to delete)
    └─→ Phase 7 (US5: Configure)       ← Requires US1 (needs basic ops for testing)
    ↓
Phase 8 (Polish)
```

### Parallel Execution Opportunities

**Within Phase 3 (US1)**:
- Tests T010-T024 can all be written in parallel
- Implementation tasks marked [P] can be done in parallel:
  - T025-T029 (models + validators)
  - T030-T032 (storage layer)
- Once T033 done, T034-T035 can proceed
- Once T036 done, T037-T038 can proceed

**Across Phases**:
- After Phase 2 complete and Phase 3 implementation starts:
  - Phase 4 tests can be written in parallel
  - Phase 5 tests can be written in parallel
  - Phase 6 tests can be written in parallel

**Within Each Story Phase**:
- All unit tests for that story can be written in parallel
- Implementation tasks marked [P] are parallelizable
- Integration tests can be written after unit tests done

### Example Parallel Work for US1
```
Developer A: T010-T016 (Task model + validation tests)
Developer B: T017-T019 (Storage layer tests)
Developer C: T020-T021 (TaskService tests)
Developer D: T022-T024 (CLI integration tests)

Then in parallel:
Developer A: T025-T029 (Task model + validators implementation)
Developer B: T030-T032 (Storage layer implementation)

Then:
Developer A: T033-T035 (TaskService implementation)
Developer B: T036-T038 (CLI commands)
```

---

## Task Summary

**Total Tasks**: 89
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundation): 3 tasks
- Phase 3 (US1 - Add/View): 30 tasks (15 tests + 15 implementation)
- Phase 4 (US2 - Complete): 13 tasks (7 tests + 6 implementation)
- Phase 5 (US3 - Update): 10 tasks (7 tests + 3 implementation)
- Phase 6 (US4 - Delete): 8 tasks (5 tests + 3 implementation)
- Phase 7 (US5 - Configure): 8 tasks (5 tests + 3 implementation)
- Phase 8 (Polish): 11 tasks

**Parallelizable Tasks**: 68 tasks marked [P] (76%)

**User Story Distribution**:
- US1 (P1): 30 tasks - Add and view with persistence
- US2 (P1): 13 tasks - Mark complete/incomplete
- US3 (P2): 10 tasks - Update task details
- US4 (P2): 8 tasks - Delete tasks
- US5 (P3): 8 tasks - Configure storage location

**Estimated MVP Effort**: Phases 1-3 (39 tasks) delivers working add/view functionality

**Independent Test Validation**:
- ✅ US1: Cross-session add/list tested in T024
- ✅ US2: Cross-session status persistence tested in T046
- ✅ US3: Cross-session update persistence tested in T059
- ✅ US4: Cross-session delete persistence tested in T067
- ✅ US5: Custom storage location tested in T074-T075
