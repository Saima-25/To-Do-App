"""Unit tests for validation functions.

Following TDD approach - these tests are written FIRST and should FAIL
until the implementation is complete.
"""

import pytest

from src.lib.validators import (
    MAX_DESCRIPTION_LENGTH,
    MAX_TITLE_LENGTH,
    validate_description,
    validate_title,
)


class TestValidateTitle:
    """Tests for validate_title function."""

    def test_validate_title_with_valid_input(self):
        """Test validation succeeds with valid title."""
        title = "Buy groceries"
        result = validate_title(title)
        assert result == "Buy groceries"

    def test_validate_title_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        title = "  Buy groceries  "
        result = validate_title(title)
        assert result == "Buy groceries"

    def test_validate_title_with_max_length(self):
        """Test validation succeeds with maximum length title."""
        title = "x" * MAX_TITLE_LENGTH
        result = validate_title(title)
        assert result == title
        assert len(result) == MAX_TITLE_LENGTH

    def test_validate_title_rejects_empty_string(self):
        """Test validation fails with empty string."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            validate_title("")

    def test_validate_title_rejects_whitespace_only(self):
        """Test validation fails with whitespace-only string."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            validate_title("   ")

    def test_validate_title_rejects_none(self):
        """Test validation fails with None."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            validate_title(None)

    def test_validate_title_rejects_too_long(self):
        """Test validation fails when title exceeds max length."""
        title = "x" * (MAX_TITLE_LENGTH + 1)
        with pytest.raises(ValueError, match=f"Title exceeds {MAX_TITLE_LENGTH} characters"):
            validate_title(title)

    def test_validate_title_with_special_characters(self):
        """Test validation allows special characters."""
        title = "Task #1: Review PR @user (urgent!)"
        result = validate_title(title)
        assert result == title

    def test_validate_title_with_unicode(self):
        """Test validation allows unicode characters."""
        title = "Acheter des légumes 🥕"
        result = validate_title(title)
        assert result == title


class TestValidateDescription:
    """Tests for validate_description function."""

    def test_validate_description_with_valid_input(self):
        """Test validation succeeds with valid description."""
        description = "From the farmers market"
        result = validate_description(description)
        assert result == "From the farmers market"

    def test_validate_description_allows_empty_string(self):
        """Test validation succeeds with empty string."""
        description = ""
        result = validate_description(description)
        assert result == ""

    def test_validate_description_with_none(self):
        """Test validation converts None to empty string."""
        result = validate_description(None)
        assert result == ""

    def test_validate_description_with_max_length(self):
        """Test validation succeeds with maximum length description."""
        description = "x" * MAX_DESCRIPTION_LENGTH
        result = validate_description(description)
        assert result == description
        assert len(result) == MAX_DESCRIPTION_LENGTH

    def test_validate_description_rejects_too_long(self):
        """Test validation fails when description exceeds max length."""
        description = "x" * (MAX_DESCRIPTION_LENGTH + 1)
        with pytest.raises(ValueError, match=f"Description exceeds {MAX_DESCRIPTION_LENGTH} characters"):
            validate_description(description)

    def test_validate_description_with_multiline(self):
        """Test validation allows multiline descriptions."""
        description = "Line 1\nLine 2\nLine 3"
        result = validate_description(description)
        assert result == description

    def test_validate_description_with_special_characters(self):
        """Test validation allows special characters."""
        description = "Details: @user #123 (urgent!) - see https://example.com"
        result = validate_description(description)
        assert result == description

    def test_validate_description_with_unicode(self):
        """Test validation allows unicode characters."""
        description = "Détails: légumes frais 🥕🥬"
        result = validate_description(description)
        assert result == description
