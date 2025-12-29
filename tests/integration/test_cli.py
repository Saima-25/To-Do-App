"""Integration tests for the Todo CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from src.cli.main import cli


@pytest.fixture
def isolated_storage(tmp_path: Path, monkeypatch):
    """Provide isolated storage for each test via TODO_FILE environment variable."""
    storage_path = tmp_path / "test_tasks.json"
    monkeypatch.setenv("TODO_FILE", str(storage_path))
    return storage_path


@pytest.mark.usefixtures("isolated_storage")
class TestAddCommand:
    """Integration tests for the 'todo add' command."""

    def test_add_task_with_title_succeeds(self, cli_runner: CliRunner) -> None:
        """Test adding a task with title returns success."""
        result = cli_runner.invoke(cli, ["add", "Buy groceries"])

        assert result.exit_code == 0
        assert 'Task 1 added: "Buy groceries"' in result.output

    def test_add_task_with_description_succeeds(self, cli_runner: CliRunner) -> None:
        """Test adding a task with description returns success."""
        result = cli_runner.invoke(
            cli, ["add", "Call dentist", "-d", "Schedule annual checkup"]
        )

        assert result.exit_code == 0
        assert 'Task 1 added: "Call dentist"' in result.output

    def test_add_task_with_empty_title_fails(self, cli_runner: CliRunner) -> None:
        """Test adding a task with empty title returns error."""
        result = cli_runner.invoke(cli, ["add", ""])

        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_add_multiple_tasks_assigns_sequential_ids(
        self, cli_runner: CliRunner
    ) -> None:
        """Test that multiple tasks get sequential IDs."""
        result1 = cli_runner.invoke(cli, ["add", "Task 1"])
        result2 = cli_runner.invoke(cli, ["add", "Task 2"])

        assert "Task 1 added" in result1.output
        assert "Task 2 added" in result2.output


@pytest.mark.usefixtures("isolated_storage")
class TestListCommand:
    """Integration tests for the 'todo list' command."""

    def test_list_empty_shows_no_tasks_message(self, cli_runner: CliRunner) -> None:
        """Test listing when no tasks shows helpful message."""
        result = cli_runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_list_with_tasks_shows_all_tasks(self, cli_runner: CliRunner) -> None:
        """Test listing shows all tasks with details."""
        cli_runner.invoke(cli, ["add", "Buy groceries"])
        cli_runner.invoke(cli, ["add", "Call dentist", "-d", "Annual checkup"])

        result = cli_runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "Buy groceries" in result.output
        assert "Call dentist" in result.output
        assert "incomplete" in result.output

    def test_list_shows_status_for_each_task(self, cli_runner: CliRunner) -> None:
        """Test that list shows status clearly."""
        cli_runner.invoke(cli, ["add", "Task 1"])
        cli_runner.invoke(cli, ["add", "Task 2"])
        cli_runner.invoke(cli, ["complete", "1"])

        result = cli_runner.invoke(cli, ["list"])

        assert "complete" in result.output
        assert "incomplete" in result.output

    def test_list_shows_tasks_ordered_by_id(self, cli_runner: CliRunner) -> None:
        """Test that tasks are listed in ID order."""
        cli_runner.invoke(cli, ["add", "Task 1"])
        cli_runner.invoke(cli, ["add", "Task 2"])
        cli_runner.invoke(cli, ["add", "Task 3"])

        result = cli_runner.invoke(cli, ["list"])

        # Check order by finding positions in output
        pos1 = result.output.find("Task 1")
        pos2 = result.output.find("Task 2")
        pos3 = result.output.find("Task 3")
        assert pos1 < pos2 < pos3


@pytest.mark.usefixtures("isolated_storage")
class TestCompleteCommand:
    """Integration tests for the 'todo complete' command."""

    def test_complete_existing_task_succeeds(self, cli_runner: CliRunner) -> None:
        """Test marking existing task complete returns success."""
        cli_runner.invoke(cli, ["add", "Task 1"])

        result = cli_runner.invoke(cli, ["complete", "1"])

        assert result.exit_code == 0
        assert "Task 1 marked as complete" in result.output

    def test_complete_nonexistent_task_fails(self, cli_runner: CliRunner) -> None:
        """Test marking non-existent task returns error."""
        result = cli_runner.invoke(cli, ["complete", "99"])

        assert result.exit_code == 1
        assert "Error:" in result.output
        assert "not found" in result.output

    def test_complete_updates_status_in_list(self, cli_runner: CliRunner) -> None:
        """Test that completed task shows correct status in list."""
        cli_runner.invoke(cli, ["add", "Task 1"])
        cli_runner.invoke(cli, ["complete", "1"])

        result = cli_runner.invoke(cli, ["list"])

        # Find the line with Task 1 and check it shows complete
        lines = result.output.split("\n")
        task_line = [line for line in lines if "Task 1" in line][0]
        assert "complete" in task_line


@pytest.mark.usefixtures("isolated_storage")
class TestIncompleteCommand:
    """Integration tests for the 'todo incomplete' command."""

    def test_incomplete_existing_task_succeeds(self, cli_runner: CliRunner) -> None:
        """Test marking existing task incomplete returns success."""
        cli_runner.invoke(cli, ["add", "Task 1"])
        cli_runner.invoke(cli, ["complete", "1"])

        result = cli_runner.invoke(cli, ["incomplete", "1"])

        assert result.exit_code == 0
        assert "Task 1 marked as incomplete" in result.output

    def test_incomplete_nonexistent_task_fails(self, cli_runner: CliRunner) -> None:
        """Test marking non-existent task returns error."""
        result = cli_runner.invoke(cli, ["incomplete", "99"])

        assert result.exit_code == 1
        assert "Error:" in result.output


@pytest.mark.usefixtures("isolated_storage")
class TestUpdateCommand:
    """Integration tests for the 'todo update' command."""

    def test_update_title_succeeds(self, cli_runner: CliRunner) -> None:
        """Test updating title returns success."""
        cli_runner.invoke(cli, ["add", "Original title"])

        result = cli_runner.invoke(cli, ["update", "1", "--title", "New title"])

        assert result.exit_code == 0
        assert "Task 1 updated" in result.output

    def test_update_description_succeeds(self, cli_runner: CliRunner) -> None:
        """Test updating description returns success."""
        cli_runner.invoke(cli, ["add", "Task 1"])

        result = cli_runner.invoke(cli, ["update", "1", "-d", "New description"])

        assert result.exit_code == 0
        assert "Task 1 updated" in result.output

    def test_update_with_empty_title_fails(self, cli_runner: CliRunner) -> None:
        """Test updating with empty title returns error."""
        cli_runner.invoke(cli, ["add", "Original title"])

        result = cli_runner.invoke(cli, ["update", "1", "--title", ""])

        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_update_nonexistent_task_fails(self, cli_runner: CliRunner) -> None:
        """Test updating non-existent task returns error."""
        result = cli_runner.invoke(cli, ["update", "99", "--title", "New title"])

        assert result.exit_code == 1
        assert "Error:" in result.output
        assert "not found" in result.output

    def test_update_without_options_fails(self, cli_runner: CliRunner) -> None:
        """Test updating without title or description returns error."""
        cli_runner.invoke(cli, ["add", "Task 1"])

        result = cli_runner.invoke(cli, ["update", "1"])

        assert result.exit_code == 1
        assert "Error:" in result.output
        assert "Provide --title and/or --description" in result.output


@pytest.mark.usefixtures("isolated_storage")
class TestDeleteCommand:
    """Integration tests for the 'todo delete' command."""

    def test_delete_existing_task_succeeds(self, cli_runner: CliRunner) -> None:
        """Test deleting existing task returns success."""
        cli_runner.invoke(cli, ["add", "Task to delete"])

        result = cli_runner.invoke(cli, ["delete", "1"])

        assert result.exit_code == 0
        assert "Task 1 deleted" in result.output

    def test_delete_nonexistent_task_fails(self, cli_runner: CliRunner) -> None:
        """Test deleting non-existent task returns error."""
        result = cli_runner.invoke(cli, ["delete", "99"])

        assert result.exit_code == 1
        assert "Error:" in result.output
        assert "not found" in result.output

    def test_delete_removes_task_from_list(self, cli_runner: CliRunner) -> None:
        """Test that deleted task no longer appears in list."""
        cli_runner.invoke(cli, ["add", "Task 1"])
        cli_runner.invoke(cli, ["add", "Task 2"])
        cli_runner.invoke(cli, ["delete", "1"])

        result = cli_runner.invoke(cli, ["list"])

        assert "Task 1" not in result.output
        assert "Task 2" in result.output


@pytest.mark.usefixtures("isolated_storage")
class TestHelpCommand:
    """Integration tests for --help functionality."""

    def test_main_help_shows_all_commands(self, cli_runner: CliRunner) -> None:
        """Test that main --help shows all available commands."""
        result = cli_runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "add" in result.output
        assert "list" in result.output
        assert "complete" in result.output
        assert "incomplete" in result.output
        assert "update" in result.output
        assert "delete" in result.output

    def test_add_help_shows_usage(self, cli_runner: CliRunner) -> None:
        """Test that add --help shows usage information."""
        result = cli_runner.invoke(cli, ["add", "--help"])

        assert result.exit_code == 0
        assert "TITLE" in result.output
        assert "--description" in result.output


class TestCrossSessionPersistence:
    """Tests for task persistence across CLI sessions (User Story 1).

    Following TDD - these tests verify the critical requirement that tasks
    persist across CLI command invocations.
    """

    def test_add_task_persists_across_cli_invocations(self, cli_runner: CliRunner, temp_storage_path) -> None:
        """Test that tasks added in one CLI invocation appear in the next."""
        # First CLI invocation: add a task
        result1 = cli_runner.invoke(cli, ["add", "Buy groceries"], env={"TODO_FILE": str(temp_storage_path)})
        assert result1.exit_code == 0
        assert "Task 1 added" in result1.output

        # Second CLI invocation: list tasks (simulates new terminal session)
        result2 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result2.exit_code == 0
        assert "Buy groceries" in result2.output
        assert "incomplete" in result2.output

    def test_multiple_tasks_persist_with_correct_ids(self, cli_runner: CliRunner, temp_storage_path) -> None:
        """Test that multiple tasks persist with sequential IDs across sessions."""
        # Session 1: Add first task
        result1 = cli_runner.invoke(cli, ["add", "Task 1"], env={"TODO_FILE": str(temp_storage_path)})
        assert result1.exit_code == 0

        # Session 2: Add second task
        result2 = cli_runner.invoke(cli, ["add", "Task 2"], env={"TODO_FILE": str(temp_storage_path)})
        assert result2.exit_code == 0
        assert "Task 2 added" in result2.output

        # Session 3: List all tasks
        result3 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result3.exit_code == 0
        assert "Task 1" in result3.output
        assert "Task 2" in result3.output

    def test_status_changes_persist_across_sessions(self, cli_runner: CliRunner, temp_storage_path) -> None:
        """Test that marking task complete persists to next session."""
        # Session 1: Add task
        cli_runner.invoke(cli, ["add", "Buy groceries"], env={"TODO_FILE": str(temp_storage_path)})

        # Session 2: Mark complete
        result2 = cli_runner.invoke(cli, ["complete", "1"], env={"TODO_FILE": str(temp_storage_path)})
        assert result2.exit_code == 0

        # Session 3: Verify status persisted
        result3 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result3.exit_code == 0
        assert "Buy groceries" in result3.output
        assert "complete" in result3.output

    def test_tasks_persist_after_terminal_close_simulation(self, cli_runner: CliRunner, temp_storage_path) -> None:
        """Test complete workflow: add → close → list → complete → close → list."""
        # Step 1: Add task (first terminal session)
        result1 = cli_runner.invoke(cli, ["add", "Important task"], env={"TODO_FILE": str(temp_storage_path)})
        assert result1.exit_code == 0

        # Simulate closing terminal (no explicit action needed - just create new runner context)

        # Step 2: List tasks (new terminal session)
        result2 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result2.exit_code == 0
        assert "Important task" in result2.output
        assert "incomplete" in result2.output

        # Step 3: Mark complete (same or different session)
        result3 = cli_runner.invoke(cli, ["complete", "1"], env={"TODO_FILE": str(temp_storage_path)})
        assert result3.exit_code == 0

        # Simulate closing terminal again

        # Step 4: List again (yet another new terminal session)
        result4 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result4.exit_code == 0
        assert "Important task" in result4.output
        assert "complete" in result4.output

    def test_update_changes_persist_across_sessions(self, cli_runner: CliRunner, temp_storage_path) -> None:
        """Test that task updates persist to next session (User Story 3)."""
        # Session 1: Add task
        cli_runner.invoke(cli, ["add", "Buy groceries", "-d", "Original description"], env={"TODO_FILE": str(temp_storage_path)})

        # Session 2: Update title
        result2 = cli_runner.invoke(cli, ["update", "1", "-t", "Buy organic groceries"], env={"TODO_FILE": str(temp_storage_path)})
        assert result2.exit_code == 0

        # Session 3: Verify title update persisted
        result3 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result3.exit_code == 0
        assert "Buy organic groceries" in result3.output

        # Session 4: Update description
        result4 = cli_runner.invoke(cli, ["update", "1", "-d", "From the farmers market"], env={"TODO_FILE": str(temp_storage_path)})
        assert result4.exit_code == 0

        # Session 5: Verify both updates persisted
        result5 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result5.exit_code == 0
        assert "Buy organic groceries" in result5.output
        assert "From the farmers market" in result5.output

    def test_delete_persists_across_sessions(self, cli_runner: CliRunner, temp_storage_path) -> None:
        """Test that task deletion persists to next session (User Story 4)."""
        # Session 1: Add three tasks
        cli_runner.invoke(cli, ["add", "Task 1"], env={"TODO_FILE": str(temp_storage_path)})
        cli_runner.invoke(cli, ["add", "Task 2"], env={"TODO_FILE": str(temp_storage_path)})
        cli_runner.invoke(cli, ["add", "Task 3"], env={"TODO_FILE": str(temp_storage_path)})

        # Session 2: Delete middle task
        result2 = cli_runner.invoke(cli, ["delete", "2"], env={"TODO_FILE": str(temp_storage_path)})
        assert result2.exit_code == 0

        # Session 3: Verify deletion persisted and other tasks remain
        result3 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result3.exit_code == 0
        assert "Task 1" in result3.output
        assert "Task 2" not in result3.output
        assert "Task 3" in result3.output

        # Session 4: Delete first task
        result4 = cli_runner.invoke(cli, ["delete", "1"], env={"TODO_FILE": str(temp_storage_path)})
        assert result4.exit_code == 0

        # Session 5: Verify only Task 3 remains
        result5 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(temp_storage_path)})
        assert result5.exit_code == 0
        assert "Task 1" not in result5.output
        assert "Task 2" not in result5.output
        assert "Task 3" in result5.output


class TestStorageConfiguration:
    """Tests for custom storage location via TODO_FILE environment variable (User Story 5)."""

    def test_custom_storage_location_via_env_var(self, cli_runner: CliRunner, tmp_path) -> None:
        """Test that TODO_FILE environment variable sets custom storage location (User Story 5)."""
        # Create custom storage path
        custom_storage = tmp_path / "custom_location" / "my_tasks.json"

        # Add task with custom storage location
        result1 = cli_runner.invoke(cli, ["add", "Custom location task"], env={"TODO_FILE": str(custom_storage)})
        assert result1.exit_code == 0

        # Verify file was created at custom location
        assert custom_storage.exists(), f"Storage file not created at {custom_storage}"

        # Verify task is stored in custom location
        result2 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(custom_storage)})
        assert result2.exit_code == 0
        assert "Custom location task" in result2.output

        # Verify data is actually in the custom file
        import json
        with open(custom_storage) as f:
            data = json.load(f)
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Custom location task"

    def test_auto_creates_custom_storage_directory(self, cli_runner: CliRunner, tmp_path) -> None:
        """Test that nested directories are auto-created for custom storage path (User Story 5)."""
        # Create deeply nested custom storage path that doesn't exist yet
        custom_storage = tmp_path / "deeply" / "nested" / "custom" / "directory" / "tasks.json"

        # Verify directories don't exist yet
        assert not custom_storage.parent.exists()

        # Add task - should auto-create all parent directories
        result = cli_runner.invoke(cli, ["add", "Task in nested dir"], env={"TODO_FILE": str(custom_storage)})
        assert result.exit_code == 0

        # Verify all directories were created
        assert custom_storage.parent.exists()
        assert custom_storage.parent.is_dir()

        # Verify file was created
        assert custom_storage.exists()

        # Verify task was saved
        result2 = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(custom_storage)})
        assert result2.exit_code == 0
        assert "Task in nested dir" in result2.output


class TestPerformance:
    """Performance tests to verify scalability requirements."""

    def test_list_1000_tasks_under_2_seconds(self, cli_runner: CliRunner, tmp_path) -> None:
        """Test that listing 1000 tasks completes in under 2 seconds (SC-003)."""
        import time

        # Setup: Create storage with 1000 tasks
        storage_path = tmp_path / "perf_test.json"
        data = {
            "next_id": 1001,
            "tasks": [
                {
                    "id": i,
                    "title": f"Task {i}",
                    "description": f"Description for task {i}",
                    "status": "incomplete"
                }
                for i in range(1, 1001)
            ]
        }

        # Write directly to storage
        import json
        with open(storage_path, "w") as f:
            json.dump(data, f)

        # Measure list command performance
        start_time = time.time()
        result = cli_runner.invoke(cli, ["list"], env={"TODO_FILE": str(storage_path)})
        elapsed_time = time.time() - start_time

        # Assertions
        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 1000" in result.output
        assert elapsed_time < 2.0, f"List command took {elapsed_time:.2f}s, expected <2s"
