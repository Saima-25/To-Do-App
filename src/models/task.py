"""Task model and status enum for the Todo CLI application."""

from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique positive integer identifier (system-assigned, immutable).
        title: Short description of the task (required, 1-500 characters).
        description: Detailed information about the task (optional, 0-2000 characters).
        status: Current state of the task (default: incomplete).
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = field(default=TaskStatus.INCOMPLETE)

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"Task {self.id}: {self.title} [{self.status.value}]"

    def to_dict(self) -> dict:
        """Serialize task to JSON-compatible dictionary.

        Returns:
            Dictionary with id, title, description, and status (as string).
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,  # Convert enum to string
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize task from dictionary.

        Args:
            data: Dictionary containing task fields.

        Returns:
            Task instance created from dictionary data.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=TaskStatus(data["status"]),  # Convert string to enum
        )
