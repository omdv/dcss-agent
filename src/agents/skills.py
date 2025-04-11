"""Skills agent."""
import json
from pathlib import Path
from pydantic_ai import Agent
from src.models.character import DCSSCharacter
from game.game_handler import DCSSHandler
from loguru import logger

class SkillsAgent:
  """Handles the skills agent."""

  def __init__(self, game_handler: DCSSHandler) -> None:
    """Initialize the skills agent."""
    # TODO: use rag to feed http://crawl.chaosforge.org/Skill
    self.game_handler = game_handler
    self.agent = Agent(
      "openai:gpt-4o",
      system_prompt="""

""",
    )

  def get_skills_plan(
      self,
      character_state: DCSSCharacter,
  ) -> str:
    """Get the skills plan."""
    with Path("data/raw/skill.md").open("r") as f:
      skills_guide = f.read()

    skills_screen = self.game_handler.get_skills_screen()
    game_state = f"{character_state.model_dump_json()}\n{skills_screen}\n{skills_guide}"
    logger.debug(f"Game state: {game_state}")

    result = self.agent.run_sync(game_state).data
    result = result.replace("```json", "").replace("```", "")
    keys = json.loads(result)["keys"].split(",")
    description = json.loads(result)["reason"]
    logger.debug(f"Keys: {keys}")
    logger.debug(f"Description: {description}")
    return keys
