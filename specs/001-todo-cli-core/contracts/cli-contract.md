# CLI Contract: Todo CLI Core Features

**Feature**: 001-todo-cli-core
**Date**: 2025-12-28
**Purpose**: Define the CLI interface contract for all todo operations

## Command Overview

| Command | Description | FR Reference |
|---------|-------------|--------------|
| `todo add` | Add a new task | FR-001, FR-002, FR-003, FR-004 |
| `todo list` | List all tasks | FR-006, FR-007, FR-008, FR-009 |
| `todo complete` | Mark task complete | FR-010, FR-012 |
| `todo incomplete` | Mark task incomplete | FR-011, FR-012 |
| `todo update` | Update task fields | FR-013, FR-014, FR-015, FR-016 |
| `todo delete` | Delete a task | FR-017, FR-018, FR-019 |

## Command Specifications

### `todo` (Root Command)

```
Usage: todo [OPTIONS] COMMAND [ARGS]...

  Todo CLI - A simple command-line task manager.

Options:
  --help  Show this message and exit.

Commands:
  add         Add a new task
  complete    Mark a task as complete
  delete      Delete a task
  incomplete  Mark a task as incomplete
  list        List all tasks
  update      Update a task
```

---

### `todo add`

**Purpose**: Create a new task (FR-001, FR-002, FR-003, FR-004)

**Usage**:
```
todo add TITLE [OPTIONS]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| TITLE | string | Yes | Task title (1-500 chars) |

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --description | -d | string | "" | Optional task description (0-2000 chars) |
| --help | | | | Show help |

**Output (stdout)**:
```
Task {id} added: "{title}"
```

**Errors (stderr)**:

| Condition | Exit Code | Message |
|-----------|-----------|---------|
| Empty title | 1 | `Error: Title cannot be empty` |
| Title > 500 chars | 1 | `Error: Title exceeds 500 characters` |
| Description > 2000 chars | 1 | `Error: Description exceeds 2000 characters` |

**Examples**:
```bash
$ todo add "Buy groceries"
Task 1 added: "Buy groceries"

$ todo add "Call dentist" -d "Schedule annual checkup"
Task 2 added: "Call dentist"

$ todo add ""
Error: Title cannot be empty
```

---

### `todo list`

**Purpose**: Display all tasks (FR-006, FR-007, FR-008, FR-009)

**Usage**:
```
todo list [OPTIONS]
```

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --help | | | | Show help |

**Output (stdout)** - With tasks:
```
ID  Status      Title                Description
──  ──────────  ───────────────────  ─────────────────────────
1   incomplete  Buy groceries        From the farmers market
2   complete    Call dentist         Schedule annual checkup
3   incomplete  Write report
```

**Output (stdout)** - Empty:
```
No tasks found. Add a task with: todo add "Your task title"
```

**Errors**: None (empty list is valid state)

**Examples**:
```bash
$ todo list
ID  Status      Title           Description
──  ──────────  ──────────────  ───────────
1   incomplete  Buy groceries

$ todo list  # when empty
No tasks found. Add a task with: todo add "Your task title"
```

---

### `todo complete`

**Purpose**: Mark a task as complete (FR-010, FR-012)

**Usage**:
```
todo complete ID [OPTIONS]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| ID | integer | Yes | Task ID to mark complete |

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --help | | | | Show help |

**Output (stdout)**:
```
Task {id} marked as complete
```

**Errors (stderr)**:

| Condition | Exit Code | Message |
|-----------|-----------|---------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| Invalid ID format | 1 | `Error: ID must be a positive integer` |

**Examples**:
```bash
$ todo complete 1
Task 1 marked as complete

$ todo complete 99
Error: Task with ID 99 not found
```

---

### `todo incomplete`

**Purpose**: Mark a task as incomplete (FR-011, FR-012)

**Usage**:
```
todo incomplete ID [OPTIONS]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| ID | integer | Yes | Task ID to mark incomplete |

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --help | | | | Show help |

**Output (stdout)**:
```
Task {id} marked as incomplete
```

**Errors (stderr)**:

| Condition | Exit Code | Message |
|-----------|-----------|---------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| Invalid ID format | 1 | `Error: ID must be a positive integer` |

**Examples**:
```bash
$ todo incomplete 1
Task 1 marked as incomplete

$ todo incomplete 99
Error: Task with ID 99 not found
```

---

### `todo update`

**Purpose**: Update task title or description (FR-013, FR-014, FR-015, FR-016)

**Usage**:
```
todo update ID [OPTIONS]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| ID | integer | Yes | Task ID to update |

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --title | -t | string | None | New title (1-500 chars) |
| --description | -d | string | None | New description (0-2000 chars) |
| --help | | | | Show help |

**Note**: At least one of --title or --description must be provided.

**Output (stdout)**:
```
Task {id} updated
```

**Errors (stderr)**:

| Condition | Exit Code | Message |
|-----------|-----------|---------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| No options provided | 1 | `Error: Provide --title and/or --description to update` |
| Empty title | 1 | `Error: Title cannot be empty` |
| Title > 500 chars | 1 | `Error: Title exceeds 500 characters` |
| Description > 2000 chars | 1 | `Error: Description exceeds 2000 characters` |
| Invalid ID format | 1 | `Error: ID must be a positive integer` |

**Examples**:
```bash
$ todo update 1 --title "Buy organic groceries"
Task 1 updated

$ todo update 1 -d "From the farmers market on Saturday"
Task 1 updated

$ todo update 1 --title "New title" --description "New description"
Task 1 updated

$ todo update 99 --title "Test"
Error: Task with ID 99 not found
```

---

### `todo delete`

**Purpose**: Delete a task (FR-017, FR-018, FR-019)

**Usage**:
```
todo delete ID [OPTIONS]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| ID | integer | Yes | Task ID to delete |

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --help | | | | Show help |

**Output (stdout)**:
```
Task {id} deleted
```

**Errors (stderr)**:

| Condition | Exit Code | Message |
|-----------|-----------|---------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| Invalid ID format | 1 | `Error: ID must be a positive integer` |

**Examples**:
```bash
$ todo delete 1
Task 1 deleted

$ todo delete 99
Error: Task with ID 99 not found
```

---

## Exit Codes

| Code | Meaning | Per |
|------|---------|-----|
| 0 | Success | FR-025 |
| 1 | Error (validation, not found, etc.) | FR-025 |

## I/O Streams

| Stream | Content | Per |
|--------|---------|-----|
| stdout | Success messages, list output | FR-026 |
| stderr | Error messages | FR-026 |

## Help Documentation

All commands support `--help` per FR-024:

```bash
$ todo --help
$ todo add --help
$ todo list --help
$ todo complete --help
$ todo incomplete --help
$ todo update --help
$ todo delete --help
```
