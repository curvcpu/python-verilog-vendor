"""Unit tests for shellutils module."""

import pytest
import tempfile
import os
from pathlib import Path
from utils.shellutils import Which
from utils.shellutils import get_console_width, get_console_height

class TestWhich:
    """Tests for the Which class."""

    def test_which_finds_python(self):
        """Test that Which can find a tool that exists in PATH (python3)."""
        which = Which("python3", on_missing_action=Which.OnMissingAction.QUIET)
        result = which()
        assert result is not None
        assert isinstance(result, Path)
        assert result.name in ["python3", "python3.exe"]

    def test_which_returns_none_for_nonexistent_tool(self):
        """Test that Which returns None for a tool that doesn't exist."""
        which = Which("nonexistent_tool_12345", on_missing_action=Which.OnMissingAction.QUIET)
        result = which()
        assert result is None

    def test_which_with_custom_path(self):
        """Test that Which can check a custom path to an executable."""
        # Create a temporary executable file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
            f.write("#!/bin/bash\necho 'test'\n")
            temp_path = f.name
        
        try:
            # Make it executable
            os.chmod(temp_path, 0o755)
            
            which = Which("test_tool", tool_bin_path=temp_path, on_missing_action=Which.OnMissingAction.QUIET)
            result = which()
            assert result is not None
            assert str(result) == temp_path
        finally:
            os.unlink(temp_path)

    def test_which_with_invalid_custom_path(self):
        """Test that Which returns None for an invalid custom path."""
        which = Which("test_tool", tool_bin_path="/nonexistent/path/tool", on_missing_action=Which.OnMissingAction.QUIET)
        result = which()
        assert result is None

    def test_which_raises_on_missing_when_configured(self):
        """Test that Which raises FileNotFoundError when tool is missing and ERROR_AND_RAISE is set."""
        which = Which("nonexistent_tool_12345", on_missing_action=Which.OnMissingAction.ERROR_AND_RAISE)
        with pytest.raises(FileNotFoundError):
            which()

    def test_which_normalizes_tool_name_to_lowercase(self):
        """Test that Which normalizes tool names to lowercase."""
        which = Which("PYTHON3", on_missing_action=Which.OnMissingAction.QUIET)
        assert which.tool_name == "python3"

    def test_which_on_missing_action_enum(self):
        """Test that OnMissingAction enum values are accessible."""
        assert Which.OnMissingAction.QUIET.value == "quiet"
        assert Which.OnMissingAction.ERROR.value == "error"
        assert Which.OnMissingAction.WARNING.value == "warning"
        assert Which.OnMissingAction.ERROR_AND_RAISE.value == "error_and_raise"

class TestConsole:
    """Tests for the console module."""

    def test_get_console_width(self):
        """Test that get_console_width returns the width of the console."""
        width = get_console_width()
        assert width > 0
        assert width <= 1_000_000

    def test_get_console_height(self):
        """Test that get_console_height returns the height of the console."""
        height = get_console_height()
        assert height > 0
        assert height <= 1_000_000