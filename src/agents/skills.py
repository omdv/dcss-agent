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
Instructions:
1. You are an agent that supports the main agent playing "dungeon crawl stone soup" game
2. You will be given the character description in json format and the skills screen.
3. You will provide a training plan - what skills to focus on, what skills not to train.
4. You will need to select the manual mode and keep it selected.
5. You will need to select the skills you want to train by cycling with the skill button
6. You will provide a sequence of buttons to press to adjust the training plan.
7. You will receive a guide on how to train skills.
8. You will provide the response in the json format, nothing else:
  {
    "keys": "the comma separated keys to press",
    "reason": "the reasoning"
  }
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
