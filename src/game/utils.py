"""Game utils."""
import re

class ScreenLoadError(TimeoutError):
    """Raised when a game screen fails to load."""

    def __init__(self, screen_type: str) -> None:
        """Initialize the screen load error."""
        super().__init__(f"Failed to load {screen_type} screen")

def clean_terminal_output(ansi_output: str, *, remove_color: bool = False) -> str:
  """Remove ANSI escape codes from the output."""
  if remove_color:
    ansi_escape_color = re.compile(r"\x1b\[[0-9;]*m")
    ansi_output = re.sub(ansi_escape_color, "", ansi_output)
  return ansi_output.strip()

def sanitize_input(key_description: str) -> str:
  """Convert human-readable key descriptions into proper key strings for DCSS input.

  Sanitizes input by removing escape sequences and invalid characters.

  Args:
    key_description: Human readable key description (e.g., 'tab', 'enter', etc.)

  Returns:
      str: The actual key string to send to the game

  """
  # If the key description is a single character, return it
  if len(key_description) == 1:
    return key_description

  # First sanitize the input by removing any existing escape sequences
  sanitized = re.sub(r"[\x00-\x1f\x7f-\xff\\]", "", key_description)
  sanitized = sanitized.strip().lower()

  key_mapping = {
    "tab": "\t",
    "enter": "\r",
    "return": "\r",
    "escape": "\x1b",
    "esc": "\x1b",
    "up": "\x1b[A",
    "down": "\x1b[B",
    "right": "\x1b[C",
    "left": "\x1b[D",
    "backspace": "\x08",
    "ctrl+s": "\x13",
    "space": " ",
  }

  # Only allow single characters or known key names
  if sanitized in key_mapping:
    return key_mapping[sanitized]
  return ""
