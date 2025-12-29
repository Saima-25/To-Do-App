# Data Model: Todo CLI with File-Based Persistence

**Feature**: 002-todo-cli-persistence
**Date**: 2025-12-29
**Purpose**: Define entities, relationships, validation rules, and JSON schema for the Todo CLI application

## Entities

### Task

Represents a single todo item that persists across CLI sessions.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | int | Required, Unique, Positive, Immutable | System-assigned unique identifier (starts at 1, auto-increments) |
| `title` | str | Required, 1-500 characters, Non-whitespace-only | Short description of the task |
| `description` | str | Optional, 0-2000 characters | Detailed information about the task (empty string if not provided) |
| `status` | TaskStatus | Required, Enum: {INCOMPLETE, COMPLETE} | Current state of the task (default: INCOMPLETE) |

**Validation Rules** (from spec requirements):

- **FR-001**: Title MUST be 1-500 characters and non-whitespace-only
- **FR-002**: Description MUST be 0-2000 characters
- **FR-003**: ID MUST be unique positive integer, system-assigned
- **FR-004**: Status MUST default to INCOMPLETE on creation
- **FR-015**: ID is immutable (cannot be modified after creation)

**State Transitions**:

```
INCOMPLETE <---> COMPLETE
     ^
     |
   [default]
```

- Task created → status = INCOMPLETE (FR-004)
- mark_complete → status = COMPLETE (FR-018)
- mark_incomplete → status = INCOMPLETE (FR-019)
- All other fields preserved during status change (FR-020)

---

### Storage File

Represents the JSON file containing all tasks and metadata.

**Structure**:

| Field | Type | Description |
|-------|------|-------------|
| `next_id` | int | Counter for next task ID (persists across sessions) |
| `tasks` | list[Task] | Array of all tasks in the system |

**Location**:
- Default: `~/.todo/tasks.json`
- Configurable via `TODO_FILE` environment variable (FR-007)

**Lifecycle**:
- Created automatically if missing (FR-011)
- Loaded on CLI startup (FR-008)
- Saved immediately after each mutation (FR-009)
- Directory created if missing (FR-010)

---

## JSON Schema

### Task Object

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "From farmers market",
  "status": "incomplete"
}
```

**Field Specifications**:
- `id`: Positive integer >= 1
- `title`: Non-empty string, max 500 chars
- `description`: String, max 2000 chars (empty string if not provided)
- `status`: String enum, valid values: `"incomplete"`, `"complete"`

### Storage File Schema

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
    },
    {
      "id": 3,
      "title": "Review pull request",
      "description": "Check for security issues and code style",
      "status": "incomplete"
    }
  ]
}
```

**Root Object**:
- `next_id` (int): Next available ID for new tasks
- `tasks` (array): List of task objects

**Invariants**:
- `next_id` > max(task.id for task in tasks)
- All task IDs are unique within `tasks` array
- Empty file or missing file treated as `{"next_id": 1, "tasks": []}`

---

## Relationships

**Task ↔ Storage File**:
- One-to-many: Storage File contains 0 or more Tasks
- Cascade: Deleting a task removes it from storage file permanently (FR-029)
- Persistence: All task mutations immediately update storage file (FR-009)

**Task ↔ ID Counter**:
- Task creation increments `next_id` counter
- Counter persists in storage file (FR-013)
- Counter never decrements (even after task deletion per FR-018)

---

## Validation Rules

### Input Validation (validators.py)

**Title Validation**:
```python
def validate_title(title: str) -> str:
    """Validate and normalize task title

    Rules:
    - Strip leading/trailing whitespace
    - Must be 1-500 characters after stripping
    - Must not be whitespace-only

    Raises:
        ValueError: If title is empty, whitespace-only, or exceeds 500 chars
    """
```

**Description Validation**:
```python
def validate_description(description: str) -> str:
    """Validate task description

    Rules:
    - Must be 0-2000 characters
    - Empty string is valid

    Raises:
        ValueError: If description exceeds 2000 characters
    """
```

### Storage Validation (storage.py)

**File Format Validation**:
```python
def validate_storage_format(data: dict) -> bool:
    """Validate JSON structure matches expected schema

    Checks:
    - Contains "next_id" key (int > 0)
    - Contains "tasks" key (list)
    - Each task has required fields: id, title, description, status
    - All task IDs are unique
    - All task IDs < next_id

    Returns:
        True if valid, False otherwise (for graceful degradation)
    """
```

**Corrupted File Handling** (FR-012):
- Invalid JSON → Log warning, use empty storage
- Missing keys → Log warning, use empty storage
- Invalid data types → Log warning, use empty storage

---

## Data Flow

### Add Task Flow

```
User → CLI (add command)
  → Validate title/description (validators.py)
  → TaskService.add()
    → Generate ID from next_id
    → Create Task object (status=INCOMPLETE)
    → Add to _tasks dict
    → Increment next_id
    → storage.save() → Write JSON file
  → Return success message
```

### List Tasks Flow

```
User → CLI (list command)
  → TaskService.list_all()
    → Sort _tasks by ID ascending
    → Return list
  → Format and display to stdout
```

### Update/Delete/Mark Complete Flow

```
User → CLI (command with task_id)
  → Validate task_id is integer
  → TaskService.[operation](task_id)
    → Get task from _tasks dict
    → If not found → raise ValueError (FR-030)
    → Perform mutation (update fields, delete, change status)
    → storage.save() → Write JSON file (FR-009, FR-021, FR-026, FR-029)
  → Return success message
```

### Load on Startup Flow

```
CLI starts
  → TaskService.__init__()
    → Get storage path (env var or default)
    → storage.load(path)
      → If file missing → return {"next_id": 1, "tasks": []} (FR-011)
      → If corrupted → log warning, return empty storage (FR-012)
      → Read JSON, validate format
      → Deserialize tasks (Task.from_dict())
    → Populate _tasks dict
    → Set _next_id from storage
  → Ready for commands
```

---

## Performance Considerations

**In-Memory Cache**:
- `_tasks: dict[int, Task]` provides O(1) lookup by ID
- Dictionary allows efficient add, delete, get operations
- List operations require sorting (O(n log n)) but spec limits to 1000 tasks

**File I/O**:
- Read once on startup (amortized across multiple commands in interactive use)
- Write on every mutation (ensures FR-009, acceptable for <1000 tasks)
- Atomic writes (temp file + rename) prevent corruption
- Target: <100ms for save operation (per Technical Context)

**Scalability**:
- JSON file size for 1000 tasks ~200KB (well under 1MB constraint)
- Parse/serialize time for 1000 tasks <50ms on modern hardware
- Memory footprint: ~500KB for 1000 tasks in memory

---

## Edge Cases

**ID Management**:
- After deleting task 5, next task is ID 6 (not reusing deleted IDs per FR-018)
- If storage file manually edited to have gaps, IDs preserved as-is
- `next_id` always >= max(existing IDs) + 1

**Empty States**:
- Empty task list: `{"next_id": 1, "tasks": []}`
- Empty description: stored as `"description": ""`
- No tasks exist → list command shows friendly message (FR-017)

**File System Edge Cases**:
- Storage directory doesn't exist → created automatically (FR-010)
- File permissions denied → clear error message with guidance (FR-033)
- Disk full → save fails, error displayed, in-memory state preserved
- Concurrent writes → last write wins (documented limitation per spec Assumptions)

**Data Integrity**:
- Invalid status value in JSON → graceful degradation (log warning, skip task)
- Missing required field → graceful degradation (log warning, skip task)
- Duplicate IDs in JSON → keep first occurrence, log warning
- Manual edits preserved unless they violate validation rules

---

## Implementation Checklist

**Task Model (src/models/task.py)**:
- [ ] Define `TaskStatus` enum (INCOMPLETE, COMPLETE)
- [ ] Define `Task` dataclass with fields: id, title, description, status
- [ ] Implement `Task.to_dict()` method (serialize to JSON-compatible dict)
- [ ] Implement `Task.from_dict()` classmethod (deserialize from dict)
- [ ] Add `__str__()` method for display

**Validators (src/lib/validators.py)**:
- [ ] Implement `validate_title()` function with length and whitespace checks
- [ ] Implement `validate_description()` function with length check
- [ ] Define validation constants (MAX_TITLE_LENGTH=500, MAX_DESCRIPTION_LENGTH=2000)

**Storage Layer (src/lib/storage.py)**:
- [ ] Implement `load(path: Path) -> dict` function (handle missing/corrupted files)
- [ ] Implement `save(path: Path, data: dict)` function (atomic write)
- [ ] Implement `validate_storage_format(data: dict) -> bool` helper
- [ ] Handle all edge cases: missing file, corrupted JSON, permission errors

**TaskService (src/services/task_service.py)**:
- [ ] Initialize with storage path (from env or default)
- [ ] Load tasks on `__init__()` using storage.load()
- [ ] Implement CRUD methods: add, get, list_all, update, delete
- [ ] Implement status methods: mark_complete, mark_incomplete
- [ ] Call storage.save() after every mutation
- [ ] Maintain in-memory `_tasks` dict and `_next_id` counter

This data model provides the foundation for implementing all 38 functional requirements from the specification.
