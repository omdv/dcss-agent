"""Game state model."""
from pydantic import BaseModel
from src.models.character import DCSSCharacter
from src.game.game_handler import GameHandler

class GameState(BaseModel):
    """Game state model."""

    game: GameHandler
    character: DCSSCharacter | None = None

    model_config = {
        "arbitrary_types_allowed": True,
    }
