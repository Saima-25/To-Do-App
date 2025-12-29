"""Task service providing CRUD operations for tasks with JSON persistence."""

from pathlib import Path

from src.lib import storage
from src.lib.validators import validate_description, validate_title
from src.models.task import Task, TaskStatus


class TaskService:
    """Service for managing tasks with JSON file persistence.

    Provides CRUD operations for tasks with automatic ID generation,
    validation, and JSON file persistence. Tasks are loaded from file
    on initialization and saved after each mutation operation.
    """

    def __init__(self, storage_path: Path | None = None) -> None:
        """Initialize task service and load existing tasks from storage.

        Args:
            storage_path: Optional path to JSON storage file. If not provided,
                         uses TODO_FILE environment variable or default ~/.todo/tasks.json
        """
        self._storage_path = storage_path or storage.get_storage_path()
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load tasks from JSON storage file.

        Populates _tasks dict and _next_id from file. Handles missing
        and corrupted files gracefully per FR-011 and FR-012.
        """
        data = storage.load(self._storage_path)
        self._next_id = data["next_id"]

        # Deserialize tasks
        for task_data in data["tasks"]:
            task = Task.from_dict(task_data)
            self._tasks[task.id] = task

    def _save(self) -> None:
        """Save current tasks to JSON storage file.

        Serializes all tasks and next_id counter to JSON file per FR-009.
        """
        data = {
            "next_id": self._next_id,
            "tasks": [task.to_dict() for task in self._tasks.values()],
        }
        storage.save(self._storage_path, data)

    def _generate_id(self) -> int:
        """Generate the next unique task ID."""
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def add(self, title: str, description: str = "") -> Task:
        """Add a new task with the given title and optional description.

        Args:
            title: The task title (required, 1-500 characters).
            description: Optional task description (0-2000 characters).

        Returns:
            The created Task with assigned ID and default status.

        Raises:
            ValueError: If title is empty, whitespace-only, or exceeds limits.
        """
        validated_title = validate_title(title)
        validated_description = validate_description(description)

        task_id = self._generate_id()
        task = Task(
            id=task_id,
            title=validated_title,
            description=validated_description,
            status=TaskStatus.INCOMPLETE,
        )
        self._tasks[task_id] = task
        self._save()  # Persist immediately (FR-009)
        return task

    def get(self, task_id: int) -> Task | None:
        """Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def list_all(self) -> list[Task]:
        """List all tasks ordered by ID ascending.

        Returns:
            List of all tasks sorted by ID.
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task:
        """Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (optional, if provided must be valid).
            description: New description (optional).

        Returns:
            The updated Task.

        Raises:
            ValueError: If task not found or title validation fails.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        if title is not None:
            task.title = validate_title(title)

        if description is not None:
            task.description = validate_description(description)

        self._save()  # Persist immediately (FR-026)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if deletion was successful.

        Raises:
            ValueError: If task with given ID does not exist.
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found")

        del self._tasks[task_id]
        self._save()  # Persist immediately (FR-029)
        return True

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete.

        Returns:
            The updated Task.

        Raises:
            ValueError: If task with given ID does not exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        task.status = TaskStatus.COMPLETE
        self._save()  # Persist immediately (FR-021)
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete.

        Returns:
            The updated Task.

        Raises:
            ValueError: If task with given ID does not exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        task.status = TaskStatus.INCOMPLETE
        self._save()  # Persist immediately (FR-021)
        return task
