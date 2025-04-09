"""DCSS handler."""
import subprocess
import shutil
import time
from loguru import logger

from src.game.utils import clean_terminal_output, sanitize_input
from src.game.utils import ScreenLoadError

class GameHandler:
  """Game handler."""

  def __init__(self, dcss_path: str = "dcss") -> None:
    """Initialize the DCSS game handler."""
    self.dcss_path = shutil.which(dcss_path) or dcss_path
    self.process = None
    self.tmux_session_name = "dcss"
    self.action_history = []
    self.max_action_history = 10

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
        output = self.read_output()
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

  def get_game_state(self) -> str:
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

  def get_action_history(self) -> list[dict]:
    """Get the action history."""
    return self.action_history

  def write_action(self, action: dict) -> None:
    """Send a key to the DCSS process via tmux."""
    self.action_history.append(action)
    if len(self.action_history) > self.max_action_history:
      self.action_history.pop(0)
    try:
      actual_key = sanitize_input(action["key"])
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
        self.write_action({"key": "ctrl+s", "reason": "save game"})
        time.sleep(1)
        self.write_action({"key": "Esc", "reason": "exit"})
      subprocess.run(
        [shutil.which("tmux"), "kill-session", "-t", self.tmux_session_name],
        check=False,
      )
    except subprocess.SubprocessError as e:
      logger.error(f"Error cleaning up tmux session: {e}")

  def __del__(self) -> None:
    """Gracefully close the game."""
    self.close()
