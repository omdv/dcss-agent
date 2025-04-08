"""DCSS handler."""
import re
import subprocess
import shutil
import time
from loguru import logger

class ScreenLoadError(TimeoutError):
    """Raised when a game screen fails to load."""

    def __init__(self, screen_type: str) -> None:
        """Initialize the screen load error."""
        super().__init__(f"Failed to load {screen_type} screen")

def clean_terminal_output(ansi_output: str) -> str:
  """Remove ANSI escape codes from the output."""
  ansi_escape_color = re.compile(r"\x1b\[[0-9;]*m")
  return re.sub(ansi_escape_color, "", ansi_output)

def sanitize_input(key_description: str) -> str:
  """Convert human-readable key descriptions into proper key strings for DCSS input.

  Sanitizes input by removing escape sequences and invalid characters.

  Args:
    key_description: Human readable key description (e.g., 'tab', 'enter', etc.)

  Returns:
      str: The actual key string to send to the game

  """
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
    "space": " ",
  }

  # Only allow single characters or known key names
  if sanitized in key_mapping:
    return key_mapping[sanitized]
  if len(sanitized) == 1:
    return sanitized
  return ""

class DCSSHandler:
  """DCSS game handler."""

  def __init__(self, dcss_path: str = "dcss") -> None:
    """Initialize the DCSS game handler."""
    self.dcss_path = shutil.which(dcss_path) or dcss_path
    self.process = None
    self.tmux_session_name = "dcss"

  def is_game_running(self) -> bool:
    """Check if the game is running."""
    try:
      # Check if tmux session exists
      subprocess.run(
        [shutil.which("tmux"), "has-session", "-t", self.tmux_session_name],
        check=False,
      )
    except subprocess.SubprocessError as e:
      logger.error(f"Error checking if game is running: {e}")
      return False
    return True

  def start_game(self) -> bool:
    """Launch DCSS in a tmux session."""
    logger.debug("Launching DCSS in tmux session")
    try:
      # Create new tmux session
      subprocess.run(
        [shutil.which("tmux"), "new-session", "-d", "-s", self.tmux_session_name],
        check=False,
      )

      # Start DCSS in the tmux session
      subprocess.run([
        shutil.which("tmux"),
        "send-keys",
        "-t",
        self.tmux_session_name,
        self.dcss_path,
        "Enter",
      ], check=False)

      logger.debug("DCSS launched successfully.")
    except subprocess.SubprocessError as e:
      logger.error(f"Failed to launch DCSS: {e}")
      return False
    return True

  def read_output(self) -> str:
    """Read the output from the tmux window."""
    try:
      result = subprocess.run(
        [shutil.which("tmux"), "capture-pane", "-p", "-t", self.tmux_session_name],
        capture_output=True,
        text=True,
        check=False,
      )
      return clean_terminal_output(result.stdout)
    except subprocess.SubprocessError as e:
      logger.error(f"Error reading output: {e}")
      return ""

  def send_key(self, key: str, *, sanitize: bool = True) -> None:
    """Send a key to the DCSS process via tmux."""
    try:
      actual_key = sanitize_input(key) if sanitize else key
      subprocess.run(
        [shutil.which("tmux"), "send-keys", "-t", self.tmux_session_name, actual_key],
        check=False,
      )
    except subprocess.SubprocessError as e:
      logger.error(f"Error sending key: {e}")

  def close(self, *, save: bool = False) -> None:
    """Close the DCSS process and clean up."""
    try:
      if save:
        logger.debug("Saving game")
        self.send_key("\x13", sanitize=False)
        time.sleep(1)
        self.send_key("Esc")
      subprocess.run(
        [shutil.which("tmux"), "kill-session", "-t", self.tmux_session_name],
        check=False,
      )
    except subprocess.SubprocessError as e:
      logger.error(f"Error cleaning up tmux session: {e}")

  def _get_specific_game_screen(
      self,
      key: str,
      screen_type: str,
      screen_search_terms: list[str],
  ) -> str:
    """Get a specific game screen.

    Args:
        key: The key to send to trigger the screen
        screen_type: The type of screen being requested (for error messages)
        screen_search_terms: List of strings to look for to confirm screen loaded

    Returns:
        str: The screen output text

    Raises:
        ScreenLoadError: If the screen doesn't load within the retry limit

    """
    self.send_key(key)
    max_retries = 10
    retry_interval = 0.01

    for _ in range(max_retries):
        output = self.read_output().strip()
        if any(term in output for term in screen_search_terms):
            self.send_key("escape")
            return output
        time.sleep(retry_interval)
    raise ScreenLoadError(screen_type)

  def get_character_screen(self) -> str:
    """Get the character screen."""
    return self._get_specific_game_screen(
        "%",
        "character",
        ["Turns:", "Time:"],
    )

  def get_abilities_screen(self) -> str:
    """Get the abilities screen."""
    return self._get_specific_game_screen(
        "A",
        "abilities",
        ["Innate Abilities"],
    )

  def get_skills_screen(self) -> str:
    """Get the skills screen."""
    return self._get_specific_game_screen(
        "m",
        "skills",
        ["Skill"],
    )
