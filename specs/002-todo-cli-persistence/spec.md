# Feature Specification: Todo CLI with File-Based Persistence

**Feature Branch**: `002-todo-cli-persistence`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Todo CLI with file-based persistence - tasks stored in JSON file, configurable location, add/list/update/delete/complete operations on persisted data"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks Across Sessions (Priority: P1)

As a user, I want to add tasks that persist across CLI sessions so that I can track my todos over time without losing data when I close the terminal.

**Why this priority**: This is the foundational capability that enables the core workflow. Without persistent storage across sessions, the application cannot function as a task management tool. This story delivers immediate value by allowing users to build and maintain a task list.

**Independent Test**: Can be fully tested by adding a task in one CLI invocation, closing the terminal, and verifying the task appears when listing tasks in a new CLI invocation.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user runs `todo add "Buy groceries"`, **Then** the task is saved to the JSON file and assigned a unique ID
2. **Given** a task was added in a previous session, **When** user runs `todo list` in a new session, **Then** the previously added task appears in the list
3. **Given** multiple tasks exist from previous sessions, **When** user adds a new task, **Then** the new task receives a unique ID and all tasks persist
4. **Given** tasks exist in the JSON file, **When** user opens a new terminal and runs `todo list`, **Then** all tasks from the file are displayed

---

### User Story 2 - Mark Tasks Complete Persistently (Priority: P1)

As a user, I want to mark tasks as complete or incomplete and have that status persist across sessions so that I can track my progress over time.

**Why this priority**: Status management is core to task tracking functionality. Users need to record completion and have that state persist. This is essential for the primary workflow: add → work on task → mark complete.

**Independent Test**: Can be tested by adding a task, marking it complete in one session, then verifying the completion status persists in a new session.

**Acceptance Scenarios**:

1. **Given** an incomplete task exists, **When** user marks it complete, **Then** the status changes to complete and is saved to the JSON file
2. **Given** a task was marked complete in a previous session, **When** user lists tasks in a new session, **Then** the task still shows as complete
3. **Given** a complete task exists, **When** user marks it incomplete, **Then** the status changes to incomplete and persists
4. **Given** multiple tasks with different statuses exist, **When** user changes one task's status, **Then** only that task's status changes while others remain unchanged

---

### User Story 3 - Update Task Details (Priority: P2)

As a user, I want to update the title or description of existing tasks so that I can correct mistakes or add more information as tasks evolve.

**Why this priority**: Updating tasks is important for maintaining accurate information but is secondary to the core add/list/complete workflow. Users can work around missing update functionality by deleting and re-adding tasks.

**Independent Test**: Can be tested by adding a task, updating its details in one session, then verifying the updates persist in a new session.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Buy groceries", **When** user updates the title to "Buy organic groceries", **Then** the new title is saved and persists across sessions
2. **Given** a task exists, **When** user adds or updates the description, **Then** the description is saved and persists
3. **Given** a task was updated in a previous session, **When** user lists tasks in a new session, **Then** the updated details are displayed
4. **Given** user attempts to update with an empty title, **Then** the system rejects the update and the task remains unchanged

---

### User Story 4 - Delete Tasks Permanently (Priority: P2)

As a user, I want to delete tasks I no longer need so that my task list stays focused and uncluttered.

**Why this priority**: Deletion helps maintain list hygiene but is not essential for core task tracking. Users can ignore completed or irrelevant tasks without deleting them.

**Independent Test**: Can be tested by adding tasks, deleting one, and verifying it no longer appears in subsequent sessions.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 1, **When** user deletes task 1, **Then** the task is removed from the JSON file permanently
2. **Given** a task was deleted in a previous session, **When** user lists tasks in a new session, **Then** the deleted task does not appear
3. **Given** multiple tasks exist, **When** user deletes one task, **Then** remaining tasks keep their original IDs
4. **Given** user attempts to delete a non-existent task ID, **When** the delete command runs, **Then** an error message is displayed and no data is changed

---

### User Story 5 - Configure Storage Location (Priority: P3)

As a user, I want to configure where my tasks are stored so that I can organize my task lists by project or keep them in a specific location.

**Why this priority**: Custom storage location provides flexibility for advanced users but is not required for basic functionality. The default location works for most use cases.

**Independent Test**: Can be tested by setting the `TODO_FILE` environment variable, adding tasks, and verifying they are stored in the custom location.

**Acceptance Scenarios**:

1. **Given** no `TODO_FILE` environment variable is set, **When** user adds a task, **Then** it is stored in `~/.todo/tasks.json`
2. **Given** `TODO_FILE` is set to a custom path, **When** user adds a task, **Then** it is stored at the custom path
3. **Given** the custom storage directory does not exist, **When** user adds a task, **Then** the directory is created automatically
4. **Given** tasks exist in a custom location, **When** user lists tasks, **Then** tasks are loaded from the custom location

---

### Edge Cases

- **Missing storage file**: When the JSON file doesn't exist, system creates it with an empty task list
- **Corrupted JSON file**: When the JSON file contains invalid JSON, system logs a warning and starts with an empty task list
- **Storage directory doesn't exist**: System creates the directory (e.g., `~/.todo/`) automatically before saving
- **File permission errors**: When system cannot read or write the file, display clear error message with guidance
- **Empty title**: System rejects add/update operations with empty or whitespace-only titles
- **Invalid task ID**: All operations on non-existent IDs show clear error messages
- **Concurrent modifications**: When multiple CLI instances run simultaneously, last write wins (documented limitation)
- **Large task lists**: System handles up to 1000 tasks with acceptable performance
- **Special characters in paths**: Storage path handles spaces, unicode, and special characters correctly
- **ID uniqueness after deletion**: New tasks always receive unique IDs, even after deletions
- **Maximum field lengths**: Titles limited to 500 characters, descriptions to 2000 characters

## Requirements *(mandatory)*

### Functional Requirements

#### Task Management Core

- **FR-001**: System MUST allow users to add a task with a required title (1-500 characters, non-whitespace-only)
- **FR-002**: System MUST allow users to add an optional description (0-2000 characters) when creating a task
- **FR-003**: System MUST automatically assign a unique positive integer ID to each new task
- **FR-004**: System MUST set the initial status of all new tasks to "incomplete"

#### Data Persistence

- **FR-005**: System MUST persist all tasks to a JSON file that survives across CLI command executions
- **FR-006**: System MUST store tasks at `~/.todo/tasks.json` by default
- **FR-007**: System MUST support `TODO_FILE` environment variable to override the default storage location
- **FR-008**: System MUST load existing tasks from the JSON file when any CLI command starts
- **FR-009**: System MUST save tasks to the JSON file immediately after each mutation operation (add, update, delete, mark complete/incomplete)
- **FR-010**: System MUST create the storage directory if it does not exist
- **FR-011**: System MUST handle missing JSON file gracefully by starting with an empty task list
- **FR-012**: System MUST handle corrupted JSON file gracefully by logging a warning and starting with an empty task list
- **FR-013**: System MUST maintain ID counter state in the JSON file to ensure unique IDs across sessions

#### Task Viewing

- **FR-014**: System MUST display all tasks when user requests the task list
- **FR-015**: System MUST display task ID, title, description (if present), and status for each task
- **FR-016**: System MUST order task list by ID in ascending order
- **FR-017**: System MUST display a clear message when no tasks exist

#### Task Status Management

- **FR-018**: System MUST allow users to mark a task as "complete" by specifying its ID
- **FR-019**: System MUST allow users to mark a task as "incomplete" by specifying its ID
- **FR-020**: System MUST preserve all other task fields when changing status
- **FR-021**: System MUST persist status changes immediately to the JSON file

#### Task Modification

- **FR-022**: System MUST allow users to update the title of an existing task by ID
- **FR-023**: System MUST allow users to update the description of an existing task by ID
- **FR-024**: System MUST NOT allow modification of task ID
- **FR-025**: System MUST validate updated title is non-empty and within length limits
- **FR-026**: System MUST persist updates immediately to the JSON file

#### Task Deletion

- **FR-027**: System MUST allow users to delete a task by specifying its ID
- **FR-028**: System MUST NOT modify IDs of remaining tasks after deletion
- **FR-029**: System MUST remove deleted tasks permanently from the JSON file

#### Error Handling

- **FR-030**: System MUST display a clear error message when user references a non-existent task ID
- **FR-031**: System MUST display a clear error message when user provides invalid input (empty title, invalid ID format)
- **FR-032**: System MUST NOT modify the JSON file when an operation fails due to validation errors
- **FR-033**: System MUST display a clear error message with guidance when file permissions prevent reading or writing
- **FR-034**: System MUST log a warning to stderr when encountering a corrupted JSON file

#### CLI Interface

- **FR-035**: System MUST provide command-line interface for all operations
- **FR-036**: System MUST provide `--help` documentation for all commands
- **FR-037**: System MUST return appropriate exit codes (0 for success, non-zero for errors)
- **FR-038**: System MUST output results to stdout and errors to stderr

### Key Entities

- **Task**: Represents a single todo item
  - **ID**: Unique positive integer identifier (system-assigned, immutable, persists across sessions)
  - **Title**: Short description of the task (required, 1-500 characters, non-whitespace-only)
  - **Description**: Detailed information about the task (optional, 0-2000 characters)
  - **Status**: Current state of the task ("complete" or "incomplete")

- **Storage File**: JSON file containing all tasks and metadata
  - **Location**: Configurable path (default `~/.todo/tasks.json`)
  - **Format**: Human-readable JSON structure
  - **Content**: Task list array and next ID counter

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 5 seconds from command entry to confirmation
- **SC-002**: Tasks added in one CLI session are immediately visible in subsequent sessions
- **SC-003**: Users can view their complete task list in under 2 seconds regardless of task count (up to 1000 tasks)
- **SC-004**: Status changes (mark complete/incomplete) persist across CLI sessions without data loss
- **SC-005**: Users can identify task status at a glance when viewing the task list
- **SC-006**: 100% of invalid operations (empty title, non-existent ID, file errors) result in clear, actionable error messages
- **SC-007**: All five core operations (add, list, update, delete, mark complete) work on the same persisted data
- **SC-008**: New users can successfully add and view their first task within 1 minute of starting the application
- **SC-009**: Zero data loss occurs during normal operation across CLI executions
- **SC-010**: Users can configure custom storage location via environment variable without system modification
- **SC-011**: System recovers gracefully from corrupted files without losing ability to create new tasks
- **SC-012**: Users can complete the full workflow (add → list → complete → list) across multiple terminal sessions

## Assumptions

- Tasks persist across CLI command executions via JSON file storage (per constitution v1.1.0)
- Task IDs are simple incrementing integers starting from 1
- A single user interacts with the application at a time (no concurrent access coordination)
- Multiple CLI instances may run simultaneously, with last-write-wins behavior (documented limitation)
- The CLI operates in a terminal environment with standard input/output capabilities
- Unicode text is supported for titles and descriptions
- File system has write permissions for the storage directory (`~/.todo/` by default)
- JSON file is human-readable and can be manually inspected or edited if needed
- User's home directory path (`~`) can be reliably resolved
- File I/O operations complete within reasonable time (< 100ms for typical file sizes)
- Storage file size remains manageable (< 1MB for ~1000 tasks)
