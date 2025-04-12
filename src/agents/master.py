"""Master agent."""
import json
from pathlib import Path
from pydantic_ai import Agent, RunContext
from loguru import logger

from src.models.game_state import GameState
from src.agents.movement import movement_agent
from src.agents.fighting import fighting_agent
from src.agents.character import create_character_state

agent = Agent(
  "openai:gpt-4o",
  system_prompt=Path("src/prompts/master.md").read_text(),
  deps_type=GameState,
)

@agent.tool
def call_character_agent(ctx: RunContext[GameState]) -> None:
  """Call the character agent."""
  return create_character_state(ctx)

@agent.tool
def call_movement_agent(_: RunContext, game_screen: str) -> str:
  """Call the movement agent."""
  return movement_agent.run_sync(game_screen).data

@agent.tool
def call_fighting_agent(_: RunContext, game_screen: str) -> str:
  """Call the fighting agent."""
  return fighting_agent.run_sync(game_screen).data


def run_master_agent(game_state: GameState) -> str:
  """Run the agent."""
  # Form the question
  game_screen = game_state.game.get_game_screen()
  game_history = game_state.game.get_game_history()
  character = game_state.character

  question = f"Game screen:\n{game_screen}"
  question += f"\n\nActions history:\n{game_history}"
  question += f"\n\nCharacter:\n{character}"
  logger.debug(f"Question:\n{question}")

  # Run the agent
  result = agent.run_sync(question, deps=game_state)

  # Parse the result
  model_output = result.data
  parsed_result = model_output.replace("```json", "").replace("```", "")
  parsed_result = json.loads(parsed_result)
  logger.info(f"Proposed action: {parsed_result['key']}")
  logger.info(f"Reason: {parsed_result['reason']}")

  return parsed_result
