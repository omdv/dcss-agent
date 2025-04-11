"""Game state model."""
from pathlib import Path
import json
from pydantic import BaseModel
from loguru import logger
from src.models.character import DCSSCharacter

class GameState(BaseModel):
    """Game state model."""

    strategy: str = ""
    current_screen: str = ""
    action_history: list[dict] = []
    character: DCSSCharacter

    @classmethod
    def load(cls, path: Path = Path("data/game_state.json")) -> "GameState":
        """Load game state from file."""
        try:
            if path.exists():
                return cls.model_validate(json.loads(path.read_text()))
            logger.info("No existing game state found, creating new")
            return cls()
        except Exception as e:
            logger.error(f"Error loading game state: {e}")
            return cls()

    def save(self, path: Path = Path("./data/game_state.json")) -> None:
        """Save game state to file."""
        try:
            logger.info(f"Saving game state to {path}")
            path.write_text(self.model_dump_json(indent=2))
        except Exception as e:
            logger.error(f"Error saving game state: {e}")
