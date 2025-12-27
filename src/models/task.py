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
