"""Agent handler."""
import json
from loguru import logger
from pydantic_ai import Agent, RunContext
from src.models.character import DCSSCharacter
from src.models.game_state import GameState

class ValidationError(Exception):
  """Validation error."""

  def __init__(self, message: str) -> None:
    """Initialize the validation error."""
    self.message = message

class CharacterValidationError(Exception):
  """Raised when character validation fails after max retries."""

  def __init__(self, max_retries: int) -> None:
    """Initialize the character validation error."""
    self.max_retries = max_retries
    super().__init__(f"Failed to validate character data after {max_retries} attempts")

character_agent = Agent(
  "openai:gpt-4o",
  system_prompt=f"""
I have a character in Dungeon Crawl Stone Soup (DCSS) that I want to describe \
in a structured JSON format. Below is the Pydantic model's schema for the character:\

{DCSSCharacter.model_json_schema()}

Instructions:
1. Parse the provided game screen texts - character, inventory and abilities.
2. Extract relevant character information from the screens.
3. If you can't find the information, return None for that field.
4. Return the JSON object with the structure defined in the Pydantic model above
5. Create short strategy based on the character and add them to "strategy_notes" field
6. Return only the JSON object, nothing else.
""",
  deps_type=GameState,
)

def create_character_state(
    ctx: RunContext[GameState],
    retry_count: int = 0,
    max_retries: int = 3,
) -> None:
  """Create a strategy for the main agent to follow."""
  logger.info("Creating character state")
  game = ctx.deps.game

  character_screen = game.get_character_screen()
  ability_screen = game.get_abilities_screen()
  skills_screen = game.get_skills_screen()

  question = f"{character_screen}\n{ability_screen}\n{skills_screen}"
  logger.debug(f"Character agent question: {question}")
  result = character_agent.run_sync(question).data
  result = result.replace("```json", "").replace("```", "")
  logger.debug(f"Character agent result: {result}")

  character_data = json.loads(result)
  try:
    validated_data = DCSSCharacter.model_validate(character_data)
  except ValidationError as e:
    logger.error(f"Validation error (attempt {retry_count + 1}/{max_retries}): {e}")
    if retry_count < max_retries:
      validated_data = create_character_state(ctx, retry_count + 1, max_retries)
    else:
      raise CharacterValidationError(max_retries) from e

  # Refresh the character state
  logger.debug(f"Saving character state: {validated_data}")
  ctx.deps.character = validated_data
