# CLI Contract: Todo CLI with File-Based Persistence

**Feature**: 002-todo-cli-persistence
**Date**: 2025-12-29
**Purpose**: Define command-line interface contracts for all CLI commands

## General CLI Behavior

**Entry Point**: `todo` command

**Exit Codes**:
- `0`: Success
- `1`: Error (validation failure, file I/O error, task not found, etc.)

**Output Streams**:
- **stdout**: Success messages, task listings, help text
- **stderr**: Error messages, warnings (corrupted file, etc.)

**Help Support**: All commands and the root command support `--help` flag

**Storage Configuration**:
- Default: `~/.todo/tasks.json`
- Override: Set `TODO_FILE` environment variable to custom path

---

## Root Command

### `todo`

Display help and list available commands.

**Usage**:
```bash
todo
todo --help
```

**Output**:
```
Todo CLI - A simple command-line task manager.

Manage your tasks from the command line. Tasks are stored in a JSON file
and persist across CLI sessions.

Commands:
  add         Add a new task
  list        List all tasks
  complete    Mark a task as complete
  incomplete  Mark a task as incomplete
  update      Update a task's title or description
  delete      Delete a task

Use 'todo COMMAND --help' for more information on a command.
```

**Exit Code**: `0`

---

## Command: add

Add a new task with title and optional description.

**Usage**:
```bash
todo add TITLE [--description DESCRIPTION]
todo add TITLE [-d DESCRIPTION]
```

**Arguments**:
- `TITLE` (required): Task title as a single string (use quotes if contains spaces)

**Options**:
- `--description TEXT`, `-d TEXT`: Optional task description (max 2000 characters)

**Examples**:
```bash
todo add "Buy groceries"
todo add "Call dentist" --description "Schedule annual checkup"
todo add "Review PR" -d "Check for security issues"
```

**Success Output** (stdout):
```
Task 1 added: "Buy groceries"
```

**Error Cases**:

| Error | Condition | stderr Message | Exit Code |
|-------|-----------|----------------|-----------|
| Empty title | Title is empty or whitespace-only | `Error: Title cannot be empty` | 1 |
| Title too long | Title exceeds 500 characters | `Error: Title must be 500 characters or less` | 1 |
| Description too long | Description exceeds 2000 characters | `Error: Description must be 2000 characters or less` | 1 |
| File write error | Cannot write to storage file | `Error: Cannot write to {path}. Check file permissions.` | 1 |

**Functional Requirements**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-009, FR-010, FR-031

---

## Command: list

Display all tasks with ID, status, title, and description.

**Usage**:
```bash
todo list
```

**Arguments**: None

**Options**: None

**Success Output** (stdout):

**When tasks exist**:
```
ID   Status       Title                          Description
──   ──────────   ────────────────────────────── ──────────────────────────────
1    incomplete   Buy groceries                  From farmers market
2    complete     Call dentist
3    incomplete   Review pull request            Check for security issues...
```

**When no tasks exist**:
```
No tasks found. Add a task with: todo add "Your task title"
```

**Formatting**:
- Tasks ordered by ID ascending (FR-016)
- Description truncated to 30 chars with "..." if longer
- Status clearly labeled as "complete" or "incomplete" (FR-015)
- Fixed-width columns for readability

**Error Cases**:

| Error | Condition | stderr Message | Exit Code |
|-------|-----------|----------------|-----------|
| File read error | Cannot read storage file | `Error: Cannot read from {path}. Check file permissions.` | 1 |
| Corrupted file | Invalid JSON in storage | Warning: `Storage file corrupted. Starting with empty task list.` (then show empty list) | 0 |

**Functional Requirements**: FR-014, FR-015, FR-016, FR-017, FR-008, FR-012

---

## Command: complete

Mark a task as complete by its ID.

**Usage**:
```bash
todo complete TASK_ID
```

**Arguments**:
- `TASK_ID` (required): Integer ID of the task to mark complete

**Options**: None

**Examples**:
```bash
todo complete 1
todo complete 42
```

**Success Output** (stdout):
```
Task 1 marked as complete
```

**Error Cases**:

| Error | Condition | stderr Message | Exit Code |
|-------|-----------|----------------|-----------|
| Task not found | No task with given ID | `Error: Task with ID {id} not found` | 1 |
| Invalid ID format | ID is not an integer | `Error: Invalid task ID. Must be a positive integer.` | 1 |
| File write error | Cannot save after update | `Error: Cannot write to {path}. Check file permissions.` | 1 |

**Functional Requirements**: FR-018, FR-020, FR-021, FR-030, FR-031

---

## Command: incomplete

Mark a task as incomplete by its ID.

**Usage**:
```bash
todo incomplete TASK_ID
```

**Arguments**:
- `TASK_ID` (required): Integer ID of the task to mark incomplete

**Options**: None

**Examples**:
```bash
todo incomplete 1
todo incomplete 42
```

**Success Output** (stdout):
```
Task 1 marked as incomplete
```

**Error Cases**:

| Error | Condition | stderr Message | Exit Code |
|-------|-----------|----------------|-----------|
| Task not found | No task with given ID | `Error: Task with ID {id} not found` | 1 |
| Invalid ID format | ID is not an integer | `Error: Invalid task ID. Must be a positive integer.` | 1 |
| File write error | Cannot save after update | `Error: Cannot write to {path}. Check file permissions.` | 1 |

**Functional Requirements**: FR-019, FR-020, FR-021, FR-030, FR-031

---

## Command: update

Update a task's title and/or description by its ID.

**Usage**:
```bash
todo update TASK_ID [--title TITLE] [--description DESCRIPTION]
todo update TASK_ID [-t TITLE] [-d DESCRIPTION]
```

**Arguments**:
- `TASK_ID` (required): Integer ID of the task to update

**Options**:
- `--title TEXT`, `-t TEXT`: New title for the task (1-500 characters)
- `--description TEXT`, `-d TEXT`: New description for the task (max 2000 characters)

**Constraints**: At least one of `--title` or `--description` must be provided

**Examples**:
```bash
todo update 1 --title "Buy organic groceries"
todo update 1 -d "From the farmers market"
todo update 1 -t "New title" -d "New description"
```

**Success Output** (stdout):
```
Task 1 updated
```

**Error Cases**:

| Error | Condition | stderr Message | Exit Code |
|-------|-----------|----------------|-----------|
| Task not found | No task with given ID | `Error: Task with ID {id} not found` | 1 |
| No options provided | Neither title nor description given | `Error: Provide --title and/or --description to update` | 1 |
| Empty title | New title is empty/whitespace-only | `Error: Title cannot be empty` | 1 |
| Title too long | New title exceeds 500 characters | `Error: Title must be 500 characters or less` | 1 |
| Description too long | New description exceeds 2000 characters | `Error: Description must be 2000 characters or less` | 1 |
| File write error | Cannot save after update | `Error: Cannot write to {path}. Check file permissions.` | 1 |

**Functional Requirements**: FR-022, FR-023, FR-024, FR-025, FR-026, FR-030, FR-031, FR-032

---

## Command: delete

Delete a task permanently by its ID.

**Usage**:
```bash
todo delete TASK_ID
```

**Arguments**:
- `TASK_ID` (required): Integer ID of the task to delete

**Options**: None

**Examples**:
```bash
todo delete 1
todo delete 42
```

**Success Output** (stdout):
```
Task 1 deleted
```

**Error Cases**:

| Error | Condition | stderr Message | Exit Code |
|-------|-----------|----------------|-----------|
| Task not found | No task with given ID | `Error: Task with ID {id} not found` | 1 |
| Invalid ID format | ID is not an integer | `Error: Invalid task ID. Must be a positive integer.` | 1 |
| File write error | Cannot save after deletion | `Error: Cannot write to {path}. Check file permissions.` | 1 |

**Functional Requirements**: FR-027, FR-028, FR-029, FR-030, FR-031, FR-032

---

## Implementation Notes

### Click Framework Patterns

**Command Group**:
```python
@click.group()
@click.version_option(version="1.0.0", prog_name="todo")
def cli():
    """Todo CLI - A simple command-line task manager."""
    pass
```

**Command with Required Argument**:
```python
@cli.command()
@click.argument("title")
def add(title: str):
    """Add a new task with the given TITLE."""
    pass
```

**Command with Options**:
```python
@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", "-t", default=None)
@click.option("--description", "-d", default=None)
def update(task_id: int, title: str | None, description: str | None):
    """Update a task's title and/or description."""
    pass
```

**Error Handling Pattern**:
```python
try:
    service.mark_complete(task_id)
    click.echo(f"Task {task_id} marked as complete")
except ValueError as e:
    click.echo(f"Error: {e}", err=True)
    sys.exit(1)
```

### Global Service Instance

```python
# Initialize TaskService once at module level
# Storage path determined from environment or default
_service = TaskService()
```

All commands operate on the same `_service` instance, which loads from and saves to the JSON file.

---

## Acceptance Test Scenarios

Based on spec acceptance scenarios, CLI integration tests must verify:

**Cross-Session Persistence** (User Story 1):
1. Run `todo add "Buy groceries"` → verify success
2. Run `todo list` in new CLI invocation → verify task appears
3. Run `todo add "Call dentist"` → verify both tasks in subsequent list

**Status Persistence** (User Story 2):
1. Run `todo add "Task 1"` → get ID
2. Run `todo complete <ID>` → verify success
3. Run `todo list` in new CLI invocation → verify status shows "complete"

**Update Persistence** (User Story 3):
1. Run `todo add "Original title"` → get ID
2. Run `todo update <ID> -t "Updated title"` → verify success
3. Run `todo list` in new CLI invocation → verify updated title appears

**Delete Persistence** (User Story 4):
1. Run `todo add "Task 1"` and `todo add "Task 2"` → get IDs
2. Run `todo delete <ID1>` → verify success
3. Run `todo list` in new CLI invocation → verify only Task 2 appears

**Custom Storage Location** (User Story 5):
1. Set `TODO_FILE=/tmp/custom.json`
2. Run `todo add "Task 1"` → verify file created at custom path
3. Run `todo list` with same env var → verify task loaded from custom path

---

## Contract Validation

All commands comply with:
- **FR-035**: CLI interface for all operations
- **FR-036**: `--help` documentation
- **FR-037**: Exit codes (0 success, 1 error)
- **FR-038**: stdout for results, stderr for errors

Contract is ready for implementation and testing.
