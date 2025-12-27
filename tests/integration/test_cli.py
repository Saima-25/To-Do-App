"""Integration tests for the Todo CLI commands."""

import pytest
from click.testing import CliRunner

from src.cli.main import cli, _service


@pytest.fixture(autouse=True)
def reset_service() -> None:
    """Reset the global service before each test."""
    _service._tasks.clear()
    _service._next_id = 1


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
