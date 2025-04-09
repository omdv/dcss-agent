"""State agent."""
import json
from loguru import logger
from pydantic_ai import Agent
from src.models.character import DCSSCharacter
from game.game_handler import DCSSHandler

class ValidationError(Exception):
  """Validation error."""

  def __init__(self, message: str) -> None:
    """Initialize the validation error."""
    self.message = message

class StateAgent:
  """Handles the state agent."""

  def __init__(self, game_handler: DCSSHandler) -> None:
    """Initialize the skills agent."""
    self.game_handler = game_handler
    # Serialize the Pydantic model to JSON Schema
    dcss_schema = DCSSCharacter.model_json_schema()

    # Craft the prompt
    prompt = f"""
I have a character in Dungeon Crawl Stone Soup (DCSS) that I want to describe \
in a structured JSON format. Below is the Pydantic model's schema for the character:\

{dcss_schema}

Instructions:
1. Parse the provided game screen texts - character, inventory and abilities.
2. Extract relevant character information from the screens.
3. If you can't find the information, return None for that field.
4. Return the JSON object with the structure defined in the Pydantic model above
5. Return only the JSON object, nothing else.
"""

    self.agent = Agent(
      "openai:gpt-4o",
      system_prompt=prompt,
    )

  def get_character_state(self, retry_count: int = 0, max_retries: int = 3) -> DCSSCharacter:
    """Get the character state.

    Args:
        retry_count: Current number of retries (default: 0)
        max_retries: Maximum number of retries allowed (default: 3)

    Returns:
        DCSSCharacter: The parsed character state

    Raises:
        ValidationError: If validation fails after max retries

    """
    character_screen = self.game_handler.get_character_screen().strip()
    ability_screen = self.game_handler.get_abilities_screen().strip()
    skills_screen = self.game_handler.get_skills_screen().strip()

    game_state = f"{character_screen}\n{ability_screen}\n{skills_screen}"
    result = self.agent.run_sync(game_state).data
    result = result.replace("```json", "").replace("```", "")

    character_data = json.loads(result)
    try:
      validated_data = DCSSCharacter.model_validate(character_data)
    except ValidationError as e:
      logger.error(f"Validation error (attempt {retry_count + 1}/{max_retries}): {e}")
      if retry_count < max_retries:
        validated_data = self.get_character_state(retry_count + 1, max_retries)
      else:
        raise ValidationError(f"Failed to validate character data after {max_retries} attempts")
    return validated_data
