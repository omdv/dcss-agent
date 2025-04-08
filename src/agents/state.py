"""State agent."""
import json
from pydantic_ai import Agent
from src.models.character import DCSSCharacter
from src.dcss_handler import DCSSHandler

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

  def get_character_state(self) -> DCSSCharacter:
    """Get the character state.

    Args:
        game_handler: The game handler

    Returns:
        DCSSCharacter: The parsed character state

    """
    character_screen = self.game_handler.get_character_screen().strip()
    ability_screen = self.game_handler.get_abilities_screen().strip()
    skills_screen = self.game_handler.get_skills_screen().strip()

    game_state = f"{character_screen}\n{ability_screen}\n{skills_screen}"
    result = self.agent.run_sync(game_state).data
    result = result.replace("```json", "").replace("```", "")

    character_data = json.loads(result)

    return DCSSCharacter.model_validate(character_data)
