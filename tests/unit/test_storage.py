"""Unit tests for storage layer (JSON file I/O).

Following TDD approach - these tests are written FIRST and should FAIL
until the implementation is complete.
"""

import json
from pathlib import Path

from src.lib import storage


class TestStorageSave:
    """Tests for storage.save() function."""

    def test_save_creates_file(self, temp_storage_path):
        """Test that save creates the storage file."""
        data = {"next_id": 1, "tasks": []}

        storage.save(temp_storage_path, data)

        assert temp_storage_path.exists()

    def test_save_creates_directory_if_needed(self, tmp_path):
        """Test that save creates parent directory if it doesn't exist."""
        storage_path = tmp_path / "subdir" / "tasks.json"
        data = {"next_id": 1, "tasks": []}

        storage.save(storage_path, data)

        assert storage_path.exists()
        assert storage_path.parent.exists()

    def test_save_writes_valid_json(self, temp_storage_path):
        """Test that save writes valid JSON format."""
        data = {
            "next_id": 2,
            "tasks": [
                {"id": 1, "title": "Test", "description": "", "status": "incomplete"}
            ],
        }

        storage.save(temp_storage_path, data)

        # Verify we can read it back as JSON
        with open(temp_storage_path) as f:
            loaded = json.load(f)

        assert loaded == data

    def test_save_overwrites_existing_file(self, temp_storage_path):
        """Test that save overwrites existing file content."""
        # Write initial data
        initial_data = {"next_id": 1, "tasks": []}
        storage.save(temp_storage_path, initial_data)

        # Overwrite with new data
        new_data = {
            "next_id": 2,
            "tasks": [
                {"id": 1, "title": "Test", "description": "", "status": "incomplete"}
            ],
        }
        storage.save(temp_storage_path, new_data)

        # Verify new data was written
        with open(temp_storage_path) as f:
            loaded = json.load(f)

        assert loaded == new_data
        assert loaded != initial_data


class TestStorageLoad:
    """Tests for storage.load() function."""

    def test_load_returns_empty_storage_when_file_missing(self, temp_storage_path):
        """Test that load returns empty storage when file doesn't exist."""
        result = storage.load(temp_storage_path)

        assert result == {"next_id": 1, "tasks": []}
        assert not temp_storage_path.exists()  # Should not create file

    def test_load_reads_valid_json(self, temp_storage_path):
        """Test that load reads valid JSON file."""
        data = {
            "next_id": 3,
            "tasks": [
                {"id": 1, "title": "Task 1", "description": "Desc 1", "status": "complete"},
                {"id": 2, "title": "Task 2", "description": "", "status": "incomplete"},
            ],
        }

        # Write test data
        with open(temp_storage_path, "w") as f:
            json.dump(data, f)

        # Load and verify
        result = storage.load(temp_storage_path)

        assert result == data

    def test_load_handles_corrupted_json_gracefully(self, temp_storage_path, capsys):
        """Test that load handles corrupted JSON and returns empty storage."""
        # Write invalid JSON
        with open(temp_storage_path, "w") as f:
            f.write("{invalid json content")

        result = storage.load(temp_storage_path)

        # Should return empty storage
        assert result == {"next_id": 1, "tasks": []}

        # Should log warning to stderr
        captured = capsys.readouterr()
        assert "corrupted" in captured.err.lower() or "warning" in captured.err.lower()

    def test_load_handles_missing_keys_gracefully(self, temp_storage_path, capsys):
        """Test that load handles JSON with missing required keys."""
        # Write JSON with missing keys
        with open(temp_storage_path, "w") as f:
            json.dump({"tasks": []}, f)  # Missing next_id

        result = storage.load(temp_storage_path)

        # Should return empty storage
        assert result == {"next_id": 1, "tasks": []}

    def test_load_handles_wrong_data_types(self, temp_storage_path, capsys):
        """Test that load handles JSON with wrong data types."""
        # Write JSON with wrong types
        with open(temp_storage_path, "w") as f:
            json.dump({"next_id": "not a number", "tasks": "not a list"}, f)

        result = storage.load(temp_storage_path)

        # Should return empty storage
        assert result == {"next_id": 1, "tasks": []}


class TestGetStoragePath:
    """Tests for get_storage_path() function."""

    def test_get_storage_path_returns_default(self, monkeypatch):
        """Test that get_storage_path returns default path when no env var."""
        monkeypatch.delenv("TODO_FILE", raising=False)

        result = storage.get_storage_path()

        assert result == Path.home() / ".todo" / "tasks.json"

    def test_get_storage_path_uses_env_var(self, monkeypatch, tmp_path):
        """Test that get_storage_path uses TODO_FILE environment variable."""
        custom_path = tmp_path / "custom" / "my_tasks.json"
        monkeypatch.setenv("TODO_FILE", str(custom_path))

        result = storage.get_storage_path()

        assert result == custom_path

    def test_get_storage_path_expands_tilde(self, monkeypatch):
        """Test that get_storage_path expands ~ in custom path."""
        monkeypatch.setenv("TODO_FILE", "~/my_todos/tasks.json")

        result = storage.get_storage_path()

        assert "~" not in str(result)
        assert result.is_absolute()
