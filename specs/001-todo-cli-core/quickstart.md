# Quickstart: Todo CLI

**Feature**: 001-todo-cli-core
**Date**: 2025-12-28
**Purpose**: Get started with the Todo CLI in under 1 minute (per SC-007)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd todo-phase1

# Install with pip (Python 3.13+ required)
pip install -e .

# Verify installation
todo --help
```

## Basic Usage

### Add Your First Task

```bash
# Add a simple task
todo add "Buy groceries"
# Output: Task 1 added: "Buy groceries"

# Add a task with description
todo add "Call dentist" -d "Schedule annual checkup"
# Output: Task 2 added: "Call dentist"
```

### View Your Tasks

```bash
todo list
# Output:
# ID  Status      Title           Description
# ──  ──────────  ──────────────  ───────────────────────
# 1   incomplete  Buy groceries
# 2   incomplete  Call dentist    Schedule annual checkup
```

### Mark Tasks Complete

```bash
todo complete 1
# Output: Task 1 marked as complete

todo list
# Output:
# ID  Status      Title           Description
# ──  ──────────  ──────────────  ───────────────────────
# 1   complete    Buy groceries
# 2   incomplete  Call dentist    Schedule annual checkup
```

### Update a Task

```bash
todo update 1 --title "Buy organic groceries"
# Output: Task 1 updated

todo update 2 -d "Schedule for next Monday"
# Output: Task 2 updated
```

### Delete a Task

```bash
todo delete 1
# Output: Task 1 deleted

todo list
# Output:
# ID  Status      Title           Description
# ──  ──────────  ──────────────  ───────────────────────
# 2   incomplete  Call dentist    Schedule for next Monday
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `todo add TITLE [-d DESC]` | Add new task | `todo add "Task" -d "Details"` |
| `todo list` | Show all tasks | `todo list` |
| `todo complete ID` | Mark complete | `todo complete 1` |
| `todo incomplete ID` | Mark incomplete | `todo incomplete 1` |
| `todo update ID [-t TITLE] [-d DESC]` | Update task | `todo update 1 -t "New title"` |
| `todo delete ID` | Remove task | `todo delete 1` |

## Getting Help

```bash
# General help
todo --help

# Command-specific help
todo add --help
todo list --help
```

## Important Notes

- **Session-based storage**: Tasks are stored in memory only. When you exit, all tasks are lost.
- **Task IDs**: IDs are assigned automatically and never reused within a session.
- **Title required**: Every task must have a non-empty title.
