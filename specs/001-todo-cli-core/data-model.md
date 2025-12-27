# Data Model: Todo CLI Core Features

**Feature**: 001-todo-cli-core
**Date**: 2025-12-28
**Source**: [spec.md](./spec.md) Key Entities section

## Entities

### Task

The primary entity representing a single todo item.

**Attributes**:

| Field | Type | Constraints | Source |
|-------|------|-------------|--------|
| id | `int` | Positive integer, unique, immutable, system-assigned | FR-003, FR-015 |
| title | `str` | Required, 1-500 chars, non-whitespace-only | FR-001, FR-016 |
| description | `str` | Optional, 0-2000 chars | FR-002 |
| status | `TaskStatus` | Enum: "complete" \| "incomplete", default "incomplete" | FR-004, FR-010, FR-011 |

**Relationships**: None (standalone entity)

**State Transitions**:

```
                    ┌─────────────┐
     create()       │             │
  ─────────────────▶│  incomplete │
                    │             │
                    └──────┬──────┘
                           │
              complete()   │   incomplete()
                    ┌──────┴──────┐
                    ▼             ▲
              ┌─────────────┐     │
              │             │     │
              │  complete   │─────┘
              │             │
              └─────────────┘
```

**Validation Rules**:

| Rule | Field | Condition | Error |
|------|-------|-----------|-------|
| V001 | title | `len(title.strip()) >= 1` | "Title cannot be empty" |
| V002 | title | `len(title) <= 500` | "Title exceeds 500 characters" |
| V003 | description | `len(description) <= 2000` | "Description exceeds 2000 characters" |
| V004 | id | `id > 0` | "ID must be positive integer" |

## Data Structures

### TaskService (In-Memory Storage)

```
TaskService
├── _tasks: dict[int, Task]    # Primary storage: ID → Task mapping
├── _next_id: int              # Counter for ID generation (starts at 1)
└── Methods:
    ├── add(title, description?) → Task
    ├── get(id) → Task | None
    ├── list() → list[Task]
    ├── update(id, title?, description?) → Task
    ├── delete(id) → bool
    ├── mark_complete(id) → Task
    └── mark_incomplete(id) → Task
```

**Storage Characteristics**:

| Property | Value | Rationale |
|----------|-------|-----------|
| Lookup by ID | O(1) | Dict hash lookup |
| List all | O(n) | Dict values iteration |
| Add | O(1) | Dict insertion |
| Delete | O(1) | Dict removal |
| Memory | ~1KB per task | Title + description + overhead |
| Max tasks | ~1000 | Per SC-002 performance target |

## Type Definitions

### TaskStatus (Enum)

```
TaskStatus
├── INCOMPLETE = "incomplete"    # Default state on creation
└── COMPLETE = "complete"        # After marking complete
```

### Task (Dataclass)

```
Task
├── id: int                      # Unique identifier
├── title: str                   # Task title (required)
├── description: str             # Task description (optional, default "")
└── status: TaskStatus           # Current status (default INCOMPLETE)
```

## Invariants

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| INV-001 | Task IDs are unique within a session | TaskService._generate_id() |
| INV-002 | Task IDs are never reused after deletion | Counter never decrements |
| INV-003 | Task IDs are always positive integers | Counter starts at 1 |
| INV-004 | New tasks always start as incomplete | Task default status |
| INV-005 | Title cannot be empty or whitespace-only | Validation on add/update |

## Data Lifecycle

```
Session Start
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  TaskService initialized with empty _tasks dict          │
│  _next_id = 1                                           │
└─────────────────────────────────────────────────────────┘
     │
     ▼ (user operations)
┌─────────────────────────────────────────────────────────┐
│  add() → creates Task, stores in _tasks, increments ID  │
│  list() → returns all tasks from _tasks.values()        │
│  get() → returns task by ID or None                     │
│  update() → modifies task in place                      │
│  delete() → removes task from _tasks                    │
│  complete/incomplete() → updates task status            │
└─────────────────────────────────────────────────────────┘
     │
     ▼
Session End
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  All data lost (in-memory only per constitution)        │
└─────────────────────────────────────────────────────────┘
```
