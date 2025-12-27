"""Unit tests for TaskService."""

import pytest

from src.models.task import TaskStatus
from src.services.task_service import TaskService


class TestTaskServiceAdd:
    """Tests for TaskService.add() method."""

    def test_add_task_with_title_only(self, task_service: TaskService) -> None:
        """Test adding a task with title only returns Task with ID and incomplete status."""
        task = task_service.add("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_add_task_with_title_and_description(
        self, task_service: TaskService
    ) -> None:
        """Test adding a task with both title and description stores both."""
        task = task_service.add("Call dentist", "Schedule annual checkup")

        assert task.id == 1
        assert task.title == "Call dentist"
        assert task.description == "Schedule annual checkup"
        assert task.status == TaskStatus.INCOMPLETE

    def test_add_multiple_tasks_assigns_unique_sequential_ids(
        self, task_service: TaskService
    ) -> None:
        """Test that multiple tasks get unique sequential IDs."""
        task1 = task_service.add("Task 1")
        task2 = task_service.add("Task 2")
        task3 = task_service.add("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_title_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that adding a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            task_service.add("")

    def test_add_task_with_whitespace_only_title_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that adding a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            task_service.add("   ")

    def test_add_task_with_title_exceeding_500_chars_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that adding a task with title > 500 chars raises ValueError."""
        long_title = "a" * 501
        with pytest.raises(ValueError, match="Title exceeds 500 characters"):
            task_service.add(long_title)

    def test_add_task_with_description_exceeding_2000_chars_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that adding a task with description > 2000 chars raises ValueError."""
        long_description = "a" * 2001
        with pytest.raises(ValueError, match="Description exceeds 2000 characters"):
            task_service.add("Valid title", long_description)

    def test_add_task_strips_whitespace_from_title(
        self, task_service: TaskService
    ) -> None:
        """Test that leading/trailing whitespace is stripped from title."""
        task = task_service.add("  Buy groceries  ")

        assert task.title == "Buy groceries"


class TestTaskServiceListAll:
    """Tests for TaskService.list_all() method."""

    def test_list_all_empty_service_returns_empty_list(
        self, task_service: TaskService
    ) -> None:
        """Test that list_all returns empty list when no tasks exist."""
        tasks = task_service.list_all()

        assert tasks == []

    def test_list_all_returns_all_tasks(self, task_service: TaskService) -> None:
        """Test that list_all returns all added tasks."""
        task_service.add("Task 1")
        task_service.add("Task 2")
        task_service.add("Task 3")

        tasks = task_service.list_all()

        assert len(tasks) == 3

    def test_list_all_returns_tasks_ordered_by_id_ascending(
        self, task_service: TaskService
    ) -> None:
        """Test that tasks are returned in ascending ID order."""
        task_service.add("Task 1")
        task_service.add("Task 2")
        task_service.add("Task 3")

        tasks = task_service.list_all()

        assert [t.id for t in tasks] == [1, 2, 3]


class TestTaskServiceMarkComplete:
    """Tests for TaskService.mark_complete() and mark_incomplete() methods."""

    def test_mark_complete_changes_status_to_complete(
        self, task_service: TaskService
    ) -> None:
        """Test that mark_complete changes task status to COMPLETE."""
        task_service.add("Task 1")

        task = task_service.mark_complete(1)

        assert task.status == TaskStatus.COMPLETE

    def test_mark_incomplete_changes_status_to_incomplete(
        self, task_service: TaskService
    ) -> None:
        """Test that mark_incomplete changes task status to INCOMPLETE."""
        task_service.add("Task 1")
        task_service.mark_complete(1)

        task = task_service.mark_incomplete(1)

        assert task.status == TaskStatus.INCOMPLETE

    def test_mark_complete_preserves_title_and_description(
        self, task_service: TaskService
    ) -> None:
        """Test that marking complete preserves other fields."""
        task_service.add("Original title", "Original description")

        task = task_service.mark_complete(1)

        assert task.title == "Original title"
        assert task.description == "Original description"

    def test_mark_complete_nonexistent_id_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that marking non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="Task with ID 99 not found"):
            task_service.mark_complete(99)

    def test_mark_incomplete_nonexistent_id_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that marking non-existent task incomplete raises ValueError."""
        with pytest.raises(ValueError, match="Task with ID 99 not found"):
            task_service.mark_incomplete(99)


class TestTaskServiceUpdate:
    """Tests for TaskService.update() method."""

    def test_update_title_only_changes_title(self, task_service: TaskService) -> None:
        """Test updating only title preserves other fields."""
        task_service.add("Original title", "Original description")

        task = task_service.update(1, title="New title")

        assert task.title == "New title"
        assert task.description == "Original description"
        assert task.status == TaskStatus.INCOMPLETE

    def test_update_description_only_changes_description(
        self, task_service: TaskService
    ) -> None:
        """Test updating only description preserves other fields."""
        task_service.add("Original title", "Original description")

        task = task_service.update(1, description="New description")

        assert task.title == "Original title"
        assert task.description == "New description"

    def test_update_both_title_and_description(
        self, task_service: TaskService
    ) -> None:
        """Test updating both title and description."""
        task_service.add("Original title", "Original description")

        task = task_service.update(1, title="New title", description="New description")

        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_with_empty_title_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that updating with empty title raises ValueError."""
        task_service.add("Original title")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            task_service.update(1, title="")

    def test_update_nonexistent_id_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that updating non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="Task with ID 99 not found"):
            task_service.update(99, title="New title")

    def test_update_preserves_task_id(self, task_service: TaskService) -> None:
        """Test that task ID cannot be changed through update."""
        task_service.add("Original title")

        task = task_service.update(1, title="New title")

        assert task.id == 1


class TestTaskServiceDelete:
    """Tests for TaskService.delete() method."""

    def test_delete_existing_task_returns_true(
        self, task_service: TaskService
    ) -> None:
        """Test that deleting existing task returns True."""
        task_service.add("Task to delete")

        result = task_service.delete(1)

        assert result is True

    def test_delete_removes_task_from_storage(
        self, task_service: TaskService
    ) -> None:
        """Test that deleted task is no longer retrievable."""
        task_service.add("Task to delete")
        task_service.delete(1)

        assert task_service.get(1) is None

    def test_delete_nonexistent_id_raises_error(
        self, task_service: TaskService
    ) -> None:
        """Test that deleting non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="Task with ID 99 not found"):
            task_service.delete(99)

    def test_delete_preserves_other_task_ids(
        self, task_service: TaskService
    ) -> None:
        """Test that deleting a task doesn't change other tasks' IDs."""
        task_service.add("Task 1")
        task_service.add("Task 2")
        task_service.add("Task 3")

        task_service.delete(2)

        tasks = task_service.list_all()
        assert [t.id for t in tasks] == [1, 3]

    def test_deleted_task_not_in_list_all(self, task_service: TaskService) -> None:
        """Test that deleted task doesn't appear in list_all."""
        task_service.add("Task 1")
        task_service.add("Task 2")
        task_service.delete(1)

        tasks = task_service.list_all()

        assert len(tasks) == 1
        assert tasks[0].id == 2


class TestTaskServiceGet:
    """Tests for TaskService.get() method."""

    def test_get_existing_task_returns_task(self, task_service: TaskService) -> None:
        """Test that get returns the task for existing ID."""
        task_service.add("Test task")

        task = task_service.get(1)

        assert task is not None
        assert task.id == 1
        assert task.title == "Test task"

    def test_get_nonexistent_task_returns_none(
        self, task_service: TaskService
    ) -> None:
        """Test that get returns None for non-existent ID."""
        task = task_service.get(99)

        assert task is None
