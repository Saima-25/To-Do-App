# Quick Start: Todo CLI with File-Based Persistence

**Feature**: 002-todo-cli-persistence
**Date**: 2025-12-29
**Purpose**: User-friendly guide to get started with the Todo CLI application

## Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd todo-phase1

# Install dependencies
pip install -e .

# Verify installation
todo --help
```

## Basic Usage

### Add Your First Task

```bash
todo add "Buy groceries"
```

Output:
```
Task 1 added: "Buy groceries"
```

### View Your Tasks

```bash
todo list
```

Output:
```
ID   Status       Title                          Description
──   ──────────   ────────────────────────────── ──────────────────────────────
1    incomplete   Buy groceries
```

### Mark a Task Complete

```bash
todo complete 1
```

Output:
```
Task 1 marked as complete
```

### View Updated Tasks

```bash
todo list
```

Output:
```
ID   Status       Title                          Description
──   ──────────   ────────────────────────────── ──────────────────────────────
1    complete     Buy groceries
```

## Common Workflows

### Add Task with Description

```bash
todo add "Call dentist" --description "Schedule annual checkup"
```

Or use the short form:
```bash
todo add "Call dentist" -d "Schedule annual checkup"
```

### Update Task Details

Change the title:
```bash
todo update 1 --title "Buy organic groceries"
```

Change the description:
```bash
todo update 1 --description "From the farmers market"
```

Change both at once:
```bash
todo update 1 -t "Buy organic groceries" -d "From the farmers market"
```

### Delete a Task

```bash
todo delete 1
```

Output:
```
Task 1 deleted
```

### Mark Task as Incomplete

If you accidentally marked a task as complete:
```bash
todo incomplete 1
```

## Data Persistence

### Where Are Tasks Stored?

By default, tasks are saved to:
```
~/.todo/tasks.json
```

This file persists across CLI sessions. You can:
- View it: `cat ~/.todo/tasks.json`
- Edit it manually (be careful!)
- Back it up: `cp ~/.todo/tasks.json ~/.todo/tasks.backup.json`

### Custom Storage Location

Set the `TODO_FILE` environment variable to use a custom location:

**For a single command:**
```bash
TODO_FILE=/tmp/work-tasks.json todo add "Finish report"
```

**For the current session:**
```bash
export TODO_FILE=/tmp/work-tasks.json
todo add "Finish report"
todo list
```

**Permanently (add to ~/.bashrc or ~/.zshrc):**
```bash
export TODO_FILE=~/Documents/my-tasks.json
```

## Tips and Tricks

### Use Quotes for Multi-Word Titles

```bash
# ✅ Correct
todo add "Review pull request #42"

# ❌ Incorrect (will only use "Review" as title)
todo add Review pull request #42
```

### View All Available Commands

```bash
todo --help
```

### Get Help for a Specific Command

```bash
todo add --help
todo list --help
todo update --help
```

### Check Task IDs Before Operating

Always run `todo list` first to see current task IDs, especially before updating or deleting:

```bash
# 1. List tasks to see IDs
todo list

# 2. Use the correct ID
todo complete 3
```

### Quickly Add Multiple Tasks

```bash
todo add "Task 1"
todo add "Task 2"
todo add "Task 3"
todo list
```

## Troubleshooting

### Error: "Title cannot be empty"

Make sure your title has actual text content:

```bash
# ❌ Fails
todo add ""
todo add "   "

# ✅ Works
todo add "Valid task"
```

### Error: "Task with ID X not found"

The task doesn't exist. Run `todo list` to see available task IDs.

### Error: "Cannot write to /path/to/file"

Check file permissions:

```bash
# Check if directory exists
ls -la ~/.todo/

# Check file permissions
ls -la ~/.todo/tasks.json

# Fix permissions if needed
chmod 644 ~/.todo/tasks.json
```

### Storage File Corrupted

If you see a warning about corrupted storage, the CLI will start with an empty task list. Your old file is preserved at `~/.todo/tasks.json` - you can manually inspect or restore it.

## Example Session

Here's a complete workflow demonstrating the Todo CLI:

```bash
# Start a new terminal session
$ todo list
No tasks found. Add a task with: todo add "Your task title"

# Add some tasks
$ todo add "Buy groceries"
Task 1 added: "Buy groceries"

$ todo add "Call dentist" -d "Schedule annual checkup"
Task 2 added: "Call dentist"

$ todo add "Review PR #42" -d "Check for security issues and code style"
Task 3 added: "Review PR #42"

# View all tasks
$ todo list
ID   Status       Title                          Description
──   ──────────   ────────────────────────────── ──────────────────────────────
1    incomplete   Buy groceries
2    incomplete   Call dentist                   Schedule annual checkup
3    incomplete   Review PR #42                  Check for security issues...

# Mark one complete
$ todo complete 1
Task 1 marked as complete

# Update another
$ todo update 2 -t "Call dentist ASAP"
Task 2 updated

# View updated list
$ todo list
ID   Status       Title                          Description
──   ──────────   ────────────────────────────── ──────────────────────────────
1    complete     Buy groceries
2    incomplete   Call dentist ASAP              Schedule annual checkup
3    incomplete   Review PR #42                  Check for security issues...

# Close terminal and reopen
$ todo list
ID   Status       Title                          Description
──   ──────────   ────────────────────────────── ──────────────────────────────
1    complete     Buy groceries
2    incomplete   Call dentist ASAP              Schedule annual checkup
3    incomplete   Review PR #42                  Check for security issues...

# Tasks persisted! ✅
```

## Next Steps

- Read the full [specification](./spec.md) for detailed requirements
- Review [CLI contracts](./contracts/cli-contract.md) for complete command reference
- Check [data model](./data-model.md) to understand JSON storage format
- Run tests: `pytest` (for developers)

## Getting Help

```bash
# Show all commands
todo --help

# Get help for a specific command
todo add --help
todo list --help
todo update --help
todo delete --help
todo complete --help
todo incomplete --help
```

Happy task tracking! 🎯
