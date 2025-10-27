from enum import Enum
import os
from pathlib import Path
from typing import Optional
import shutil

# can be imported as part of the pyutils package or just as directory imports, so we handle both cases
try:
    from utils.colors import AnsiColorsTool
except ModuleNotFoundError:
    from ..colors.ansi import AnsiColorsTool

class Which:
    """
    Checks if a tool is available in the PATH (or a custom supplied path)and prints helpful message if it needs to be installed.
    """

    class OnMissingAction(Enum):
        QUIET = "quiet"
        ERROR = "error"
        WARNING = "warning"
        ERROR_AND_RAISE = "error_and_raise"

    def __init__(self, tool_name: str, tool_bin_path: Optional[str] = None, on_missing_action: OnMissingAction = OnMissingAction.ERROR_AND_RAISE):
        self.tool_name = tool_name.lower()
        self.tool_bin_path = tool_bin_path
        self.on_missing_action: self.OnMissingAction = on_missing_action

    def __call__(self) -> Optional[Path]:
        """
        Check if 'tool_name' binary is available in PATH and print helpful message if not.
        If tool_bin_path is provided, check that first.

        Returns path to the tool if it is found in PATH or in the tool_bin_path, None otherwise.
        """
        if self.tool_bin_path:
            if not os.path.exists(self.tool_bin_path) or not os.access(self.tool_bin_path, os.X_OK):
                if self.on_missing_action == self.OnMissingAction.ERROR or self.on_missing_action == self.OnMissingAction.ERROR_AND_RAISE:
                    self._print_error(f"error: {self.tool_bin_path} not found or not an executable program\n")
                    self._print_install_instructions(self.tool_name)
                    if self.on_missing_action == self.OnMissingAction.ERROR_AND_RAISE:
                        raise FileNotFoundError(f"{self.tool_bin_path} not found or not an executable program")
                elif self.on_missing_action == self.OnMissingAction.WARNING:
                    self._print_warning(f"warning: {self.tool_bin_path} not found or not an executable program\n")
                    self._print_install_instructions(self.tool_name)
                return None
            else:
                return Path(self.tool_bin_path)
        else:
            if shutil.which(self.tool_name) is None:
                if self.on_missing_action == self.OnMissingAction.ERROR or self.on_missing_action == self.OnMissingAction.ERROR_AND_RAISE:
                    self._print_error(f"error: {self.tool_name} not found in PATH\n")
                    self._print_install_instructions(self.tool_name)
                    if self.on_missing_action == self.OnMissingAction.ERROR_AND_RAISE:
                        raise FileNotFoundError(f"{self.tool_name} not found in PATH")
                elif self.on_missing_action == self.OnMissingAction.WARNING:
                    self._print_warning(f"warning:{self.tool_name} not found in PATH\n")
                    self._print_install_instructions(self.tool_name)
                return None
            else:
                return Path(shutil.which(self.tool_name))

    def _print_error(self, message: str):
        """Print error message in red."""
        ansi = AnsiColorsTool()
        print(ansi.bright_red(message), end='')

    def _print_warning(self, message: str):
        """Print warning message in yellow."""
        ansi = AnsiColorsTool()
        print(ansi.bright_yellow(message), end='')

    def _print_install_instructions(self, tool_name: str):
        """
        Print helpful instructions for installing a tool if it is not found in PATH.
        """
        ansi = AnsiColorsTool()
        if tool_name == 'delta':
            print(f"Please install {ansi.bold}delta{ansi.reset}:")
            print("  (macOS) brew install git-delta")
            print("  (Ubuntu/Debian) sudo apt install delta")
        elif tool_name == 'slang':
            print(f"Please install {ansi.bold}slang{ansi.reset}")
            print(f"""
Instructions to compile and install slang areavailable in {ansi.bright_blue}https://github.com/MikePopoloski/slang.git{ansi.reset} 
repo's README.md.  

Roughly, it will be something like this:

  {ansi.bold}git clone https://github.com/MikePopoloski/slang.git
  cd slang
  cmake -B build
  cmake --build build -j{ansi.reset}
""")
        else:
            # if we don't know how to install it, just print a generic message
            print(f"Please install {ansi.bold}{tool_name}{ansi.reset}.")

