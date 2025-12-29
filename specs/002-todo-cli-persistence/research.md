# Research: Todo CLI with File-Based Persistence

**Feature**: 002-todo-cli-persistence
**Date**: 2025-12-29
**Purpose**: Document technology choices, best practices, and design decisions for implementing JSON file persistence in a Python CLI application

## Technology Decisions

### CLI Framework: Click vs Argparse

**Decision**: Use Click framework

**Rationale**:
- **Subcommand Support**: Click provides built-in decorators for subcommands (`@click.group()`, `@command()`), making it trivial to implement `todo add`, `todo list`, etc.
- **Auto-Help Generation**: Click automatically generates `--help` documentation from docstrings and decorators
- **Type Validation**: Built-in parameter types (INT, STRING) with automatic validation
- **User Experience**: Click provides better error messages and handles edge cases (missing required args, invalid types) gracefully
- **Code Clarity**: Decorator-based approach is more readable than argparse's imperative setup
- **Constitution Compliance**: Explicitly mentioned in constitution Technology Stack as an option

**Alternatives Considered**:
- **argparse** (stdlib): More verbose, requires manual subparser setup, but no external dependency
- **typer**: Modern, uses type hints, but adds another dependency beyond Click

**Best Practices**:
- Use `@click.command()` for each CLI command
- Use `@click.option()` for optional flags (--description, --title)
- Use `@click.argument()` for required positional args (task_id, title)
- Output to stdout for success, stderr for errors
- Return exit code 0 for success, 1 for errors
- Provide rich help text via docstrings

---

### JSON File Storage: Structure and Operations

**Decision**: Use stdlib `json` module with custom serialization for Task dataclass

**Rationale**:
- **No External Dependencies**: Meets constitution requirement for minimal dependencies
- **Human-Readable**: JSON files can be inspected/edited manually
- **Cross-Platform**: JSON format works identically on Linux, macOS, Windows
- **Performance**: Adequate for ~1000 tasks (target scope from spec)
- **Simplicity**: Straightforward load/dump operations

**File Format Design**:
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

**Design Decisions**:
- Store `next_id` at root level to persist ID counter across sessions (FR-013)
- Store tasks as array for easy serialization/deserialization
- Use string status values ("complete", "incomplete") instead of booleans for clarity
- Include all fields even if empty (e.g., `"description": ""`) for consistency

**Best Practices**:
- Use `json.dump()` with `indent=2` for readable output
- Use `pathlib.Path` for cross-platform file path handling
- Atomic writes: write to temp file, then rename to avoid corruption
- Validate JSON structure on load (check for required keys)
- Handle `JSONDecodeError` gracefully (corrupted file case per FR-012)
- Create parent directories with `Path.mkdir(parents=True, exist_ok=True)` per FR-010

---

### Error Handling Strategy

**Decision**: Implement three-tier error handling approach

**Rationale**:
- **Validation Errors**: Caught at input (validators.py), raise ValueError with clear messages
- **File I/O Errors**: Caught at storage layer (storage.py), raise custom StorageError
- **CLI Errors**: Caught at CLI layer (main.py), output to stderr with exit code 1

**Error Scenarios**:
1. **Missing File** (FR-011): Start with empty task list, no error
2. **Corrupted JSON** (FR-012): Log warning to stderr, start with empty task list
3. **Permission Denied** (FR-033): Display clear error: "Cannot write to {path}. Check file permissions."
4. **Invalid ID** (FR-030): "Task with ID {id} not found"
5. **Empty Title** (FR-031): "Title cannot be empty"
6. **Validation Failures** (FR-032): Do not modify file, display error, exit 1

**Best Practices**:
- Use specific exception types (FileNotFoundError, PermissionError, JSONDecodeError)
- Always include actionable guidance in error messages
- Log warnings to stderr using Click's `click.echo(..., err=True)`
- Never lose data: if save fails, keep in-memory state intact

---

### Dataclass Serialization

**Decision**: Use dataclasses with custom `to_dict()` / `from_dict()` methods

**Rationale**:
- **Type Safety**: Dataclasses provide clear type hints for Task fields
- **Immutability**: Use `@dataclass` with mutable fields (required for updates)
- **Serialization Control**: Custom methods allow handling of Enum (TaskStatus)
- **Simplicity**: No need for dataclasses-json or pydantic (minimal dependencies)

**Implementation Pattern**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value  # Enum to string
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=TaskStatus(data["status"])  # String to Enum
        )
```

**Best Practices**:
- Always convert Enum to value for JSON serialization
- Use classmethod for deserialization (factory pattern)
- Validate required fields in `from_dict()` method
- Handle missing keys with clear error messages

---

### Testing Strategy

**Decision**: Pytest with temp file fixtures for persistence tests

**Rationale**:
- **Isolation**: Each test uses unique temp file, no side effects
- **Reliability**: Tests don't depend on user's file system state
- **Cross-Session Testing**: Can simulate multiple CLI invocations by reloading service
- **Coverage**: Separate unit tests (storage.py, validators.py) from integration tests (CLI commands)

**Fixture Pattern**:
```python
@pytest.fixture
def temp_storage_path(tmp_path):
    """Provide unique temp file path for each test"""
    return tmp_path / "test_tasks.json"

@pytest.fixture
def task_service(temp_storage_path):
    """Provide TaskService instance with temp storage"""
    return TaskService(storage_path=temp_storage_path)
```

**Best Practices**:
- Use `tmp_path` fixture (pytest built-in) for temp directories
- Test cross-session persistence by creating service, saving, destroying, then recreating
- Mock file I/O errors to test error handling (PermissionError, JSONDecodeError)
- Use `Click.CliRunner` for integration tests (simulates CLI invocations)
- Verify both stdout content AND exit codes in CLI tests

---

### Configuration Management

**Decision**: Use environment variable `TODO_FILE` with fallback to `~/.todo/tasks.json`

**Rationale**:
- **No Config Files**: Simpler than .ini/.yaml/etc. (YAGNI principle)
- **CLI Convention**: Environment variables are standard for CLI tool configuration
- **Testability**: Easy to override in tests
- **User Flexibility**: Power users can set custom paths without code changes

**Implementation**:
```python
def get_storage_path() -> Path:
    """Get storage file path from env or default"""
    env_path = os.environ.get("TODO_FILE")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / ".todo" / "tasks.json"
```

**Best Practices**:
- Always expand `~` in paths with `Path.expanduser()`
- Validate path is writable before first use
- Document environment variable in --help and README

---

## Research Summary

All technical decisions have been made and documented. No outstanding "NEEDS CLARIFICATION" items remain. The implementation approach uses:

1. **Click** for CLI framework (better DX than argparse)
2. **JSON stdlib** for persistence (no external deps)
3. **Dataclasses** with custom serialization (type-safe, simple)
4. **Pytest + temp files** for testing (isolated, reliable)
5. **Environment variables** for configuration (standard CLI practice)

All decisions comply with constitution principles:
- ✅ IV. JSON File Persistence (stdlib only, no external databases)
- ✅ V. Clean Code & Simplicity (minimal dependencies, YAGNI)
- ✅ II. CLI-First Interface (Click conventions, actionable errors)
- ✅ III. Test-Driven Development (pytest strategy defined)

Ready to proceed to Phase 1 (data model and contracts).
