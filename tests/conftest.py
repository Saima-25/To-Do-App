"""Shared test fixtures for the Todo CLI application."""

import pytest
from click.testing import CliRunner

from src.services.task_service import TaskService


@pytest.fixture
def task_service() -> TaskService:
    """Return a fresh TaskService instance for each test."""
    return TaskService()


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_task_data() -> dict:
    """Return sample task data for testing."""
    return {
        "title": "Buy groceries",
        "description": "From the farmers market",
    }
