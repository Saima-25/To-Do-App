# Research: Todo CLI Core Features

**Feature**: 001-todo-cli-core
**Date**: 2025-12-28
**Purpose**: Resolve technical decisions and document best practices

## Research Topics

### 1. CLI Framework Selection

**Decision**: `click` over `argparse`

**Rationale**:
- Native subcommand support with `@click.group()` decorator
- Automatic `--help` generation for commands and subcommands
- Built-in parameter validation and type conversion
- Cleaner syntax with decorators vs ArgumentParser setup
- Better error messages out of the box
- Active maintenance and wide adoption

**Alternatives Considered**:

| Framework | Pros | Cons | Decision |
|-----------|------|------|----------|
| argparse | Standard library, no deps | Verbose subcommand setup, manual help | Rejected |
| click | Clean decorators, auto-help | External dep (justified) | Selected |
| typer | Type hints driven | Extra abstraction layer | Rejected |
| fire | Auto-generates CLI | Less control over UX | Rejected |

### 2. Data Storage Pattern

**Decision**: `dict[int, Task]` with sequential ID counter

**Rationale**:
- O(1) lookup by ID (required for update, delete, complete operations)
- O(n) iteration for list (acceptable for <1000 tasks)
- Simple implementation, easy to test
- Natural fit for Python's built-in types
- Easily replaceable with persistence layer later

**Alternatives Considered**:

| Pattern | Pros | Cons | Decision |
|---------|------|------|----------|
| `list[Task]` | Simple | O(n) lookup by ID | Rejected |
| `dict[int, Task]` | O(1) lookup | Slightly more memory | Selected |
| SQLite in-memory | SQL queries | Over-engineered for scope | Rejected |

### 3. Task Model Design

**Decision**: Python `dataclass` with frozen=False

**Rationale**:
- Built-in to Python 3.7+, no external dependency
- Auto-generates `__init__`, `__repr__`, `__eq__`
- Type hints for all fields
- Mutable (frozen=False) to allow status updates
- Clean, declarative syntax

**Alternatives Considered**:

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Plain dict | Flexible | No type safety, error-prone | Rejected |
| NamedTuple | Immutable, light | Can't update fields | Rejected |
| dataclass | Type-safe, mutable | Slightly more code | Selected |
| Pydantic | Validation built-in | Heavy dependency | Rejected |

### 4. ID Generation Strategy

**Decision**: Sequential integer counter starting at 1

**Rationale**:
- Simple to implement and understand
- Human-readable IDs (users reference "task 1", not UUID)
- Meets FR-003 (unique positive integer)
- Counter survives deletions (IDs never reused within session)
- Gaps after deletion are acceptable per FR-018

**Implementation**:
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        task_id = self._next_id
        self._next_id += 1
        return task_id
```

### 5. Error Handling Pattern

**Decision**: Click exceptions with stderr output

**Rationale**:
- Click's `click.echo()` with `err=True` for stderr
- `sys.exit(1)` for error conditions
- Consistent error message format: `Error: <message>`
- Per FR-025: exit code 0 success, non-zero error

**Error Categories**:

| Error Type | Exit Code | Example Message |
|------------|-----------|-----------------|
| Task not found | 1 | `Error: Task with ID 99 not found` |
| Empty title | 1 | `Error: Title cannot be empty` |
| Invalid ID format | 1 | `Error: ID must be a positive integer` |
| Success | 0 | (no error message) |

### 6. Output Formatting

**Decision**: Human-readable table format for list, simple messages for mutations

**Rationale**:
- Per constitution II: "Human-Readable Output"
- Per FR-007: display ID, title, description, status
- Per SC-004: "identify task status at a glance"

**Format Examples**:

```
# List output (with tasks)
ID  Status      Title                Description
──  ──────────  ───────────────────  ─────────────────────
1   incomplete  Buy groceries        From the farmers market
2   complete    Call dentist         Schedule annual checkup
3   incomplete  Write report

# List output (empty)
No tasks found. Add a task with: todo add "Your task title"

# Add success
Task 1 added: "Buy groceries"

# Complete success
Task 1 marked as complete

# Delete success
Task 1 deleted
```

## Best Practices Applied

### Python CLI Best Practices

1. **Entry point via `pyproject.toml`**: Define `[project.scripts]` for `todo` command
2. **Click groups**: Use `@click.group()` for subcommand organization
3. **Type hints**: All functions annotated for IDE support and documentation
4. **Docstrings**: Click uses docstrings for `--help` text

### Testing Best Practices

1. **Click testing**: Use `CliRunner` for integration tests
2. **Fixtures**: Shared `TaskService` fixtures in `conftest.py`
3. **Isolation**: Each test gets fresh service instance
4. **Coverage**: Target 100% for core logic, 90%+ overall

## Resolved NEEDS CLARIFICATION

| Item | Resolution | Source |
|------|------------|--------|
| CLI Framework | `click` selected | This research |
| Command structure | Subcommands pattern | Clarification session (defaulted) |
| Storage approach | In-memory dict | Constitution + research |
