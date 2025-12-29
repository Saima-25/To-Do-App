"""Shared test fixtures for the Todo CLI application."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from src.services.task_service import TaskService


@pytest.fixture
def temp_storage_path(tmp_path: Path) -> Path:
    """Provide a unique temporary file path for each test.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        Path to a temporary JSON file for task storage
    """
    return tmp_path / "test_tasks.json"


@pytest.fixture
def task_service(temp_storage_path: Path) -> TaskService:
    """Return a fresh TaskService instance with temporary storage for each test.

    Args:
        temp_storage_path: Temporary storage path fixture

    Returns:
        TaskService instance configured with temporary storage
    """
    return TaskService(storage_path=temp_storage_path)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a Click CLI test runner.

    Returns:
        CliRunner instance for testing CLI commands
    """
    return CliRunner()


@pytest.fixture
def sample_task_data() -> dict:
    """Return sample task data for testing.

    Returns:
        Dictionary with sample title and description
    """
    return {
        "title": "Buy groceries",
        "description": "From the farmers market",
    }
