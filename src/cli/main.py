"""Command-line interface for the Todo CLI application."""

import sys

import click

from src.services.task_service import TaskService


def _get_service() -> TaskService:
    """Get a TaskService instance that respects TODO_FILE environment variable.

    This function creates a new service instance on each call to ensure
    the TODO_FILE environment variable is checked at runtime, not at
    module import time.
    """
    return TaskService()


@click.group()
@click.version_option(version="0.1.0", prog_name="todo")
def cli() -> None:
    """Todo CLI - A simple command-line task manager.

    Manage your tasks from the command line. Tasks are stored in a JSON file
    and persist across CLI sessions.

    Storage location:
    - Default: ~/.todo/tasks.json
    - Custom: Set TODO_FILE environment variable
    """
    pass


@cli.command()
@click.argument("title")
@click.option(
    "--description",
    "-d",
    default="",
    help="Optional description for the task (max 2000 characters).",
)
def add(title: str, description: str) -> None:
    """Add a new task with the given TITLE.

    The task will be assigned a unique ID and start with 'incomplete' status.

    Examples:

        todo add "Buy groceries"

        todo add "Call dentist" -d "Schedule annual checkup"
    """
    try:
        task = _get_service().add(title, description)
        click.echo(f'Task {task.id} added: "{task.title}"')
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command("list")
def list_tasks() -> None:
    """List all tasks with their ID, status, title, and description.

    Tasks are displayed in order by ID (ascending). If no tasks exist,
    a helpful message is shown.

    Examples:

        todo list
    """
    tasks = _get_service().list_all()

    if not tasks:
        click.echo('No tasks found. Add a task with: todo add "Your task title"')
        return

    # Column headers
    click.echo(f"{'ID':<4} {'Status':<12} {'Title':<30} {'Description'}")
    click.echo(f"{'──':<4} {'──────────':<12} {'─' * 30} {'─' * 30}")

    for task in tasks:
        desc = task.description[:30] + "..." if len(task.description) > 30 else task.description
        click.echo(f"{task.id:<4} {task.status.value:<12} {task.title:<30} {desc}")


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task as complete by its ID.

    Examples:

        todo complete 1
    """
    try:
        _get_service().mark_complete(task_id)
        click.echo(f"Task {task_id} marked as complete")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("task_id", type=int)
def incomplete(task_id: int) -> None:
    """Mark a task as incomplete by its ID.

    Examples:

        todo incomplete 1
    """
    try:
        _get_service().mark_incomplete(task_id)
        click.echo(f"Task {task_id} marked as incomplete")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("task_id", type=int)
@click.option(
    "--title",
    "-t",
    default=None,
    help="New title for the task (1-500 characters).",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="New description for the task (max 2000 characters).",
)
def update(task_id: int, title: str | None, description: str | None) -> None:
    """Update a task's title and/or description by its ID.

    At least one of --title or --description must be provided.

    Examples:

        todo update 1 --title "Buy organic groceries"

        todo update 1 -d "From the farmers market"

        todo update 1 -t "New title" -d "New description"
    """
    if title is None and description is None:
        click.echo("Error: Provide --title and/or --description to update", err=True)
        sys.exit(1)

    try:
        _get_service().update(task_id, title=title, description=description)
        click.echo(f"Task {task_id} updated")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    """Delete a task by its ID.

    This action is permanent and cannot be undone.

    Examples:

        todo delete 1
    """
    try:
        _get_service().delete(task_id)
        click.echo(f"Task {task_id} deleted")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
