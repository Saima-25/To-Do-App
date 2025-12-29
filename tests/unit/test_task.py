"""Unit tests for Task model and TaskStatus enum.

Following TDD approach - these tests are written FIRST and should FAIL
until the implementation is complete.
"""


from src.models.task import Task, TaskStatus


class TestTaskDataclass:
    """Tests for Task dataclass creation."""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task = Task(
            id=1,
            title="Buy groceries",
            description="From farmers market",
            status=TaskStatus.COMPLETE,
        )

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "From farmers market"
        assert task.status == TaskStatus.COMPLETE

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_task_status_enum_values(self):
        """Test TaskStatus enum has correct values."""
        assert TaskStatus.INCOMPLETE.value == "incomplete"
        assert TaskStatus.COMPLETE.value == "complete"


class TestTaskSerialization:
    """Tests for Task JSON serialization (to_dict)."""

    def test_to_dict_complete_task(self):
        """Test serializing a complete task to dictionary."""
        task = Task(
            id=1,
            title="Buy groceries",
            description="From farmers market",
            status=TaskStatus.COMPLETE,
        )

        result = task.to_dict()

        assert result == {
            "id": 1,
            "title": "Buy groceries",
            "description": "From farmers market",
            "status": "complete",
        }

    def test_to_dict_incomplete_task(self):
        """Test serializing an incomplete task to dictionary."""
        task = Task(id=2, title="Call dentist", description="", status=TaskStatus.INCOMPLETE)

        result = task.to_dict()

        assert result == {
            "id": 2,
            "title": "Call dentist",
            "description": "",
            "status": "incomplete",
        }

    def test_to_dict_converts_enum_to_string(self):
        """Test that status enum is converted to string value."""
        task = Task(id=1, title="Test", status=TaskStatus.INCOMPLETE)
        result = task.to_dict()

        assert isinstance(result["status"], str)
        assert result["status"] == "incomplete"


class TestTaskDeserialization:
    """Tests for Task JSON deserialization (from_dict)."""

    def test_from_dict_complete_task(self):
        """Test deserializing a complete task from dictionary."""
        data = {
            "id": 1,
            "title": "Buy groceries",
            "description": "From farmers market",
            "status": "complete",
        }

        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "From farmers market"
        assert task.status == TaskStatus.COMPLETE

    def test_from_dict_incomplete_task(self):
        """Test deserializing an incomplete task from dictionary."""
        data = {
            "id": 2,
            "title": "Call dentist",
            "description": "",
            "status": "incomplete",
        }

        task = Task.from_dict(data)

        assert task.id == 2
        assert task.title == "Call dentist"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_from_dict_converts_string_to_enum(self):
        """Test that status string is converted to enum."""
        data = {"id": 1, "title": "Test", "description": "", "status": "incomplete"}

        task = Task.from_dict(data)

        assert isinstance(task.status, TaskStatus)
        assert task.status == TaskStatus.INCOMPLETE
