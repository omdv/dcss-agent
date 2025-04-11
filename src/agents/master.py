"""Master agent."""
import json
from pathlib import Path
from pydantic_ai import Agent, RunContext
from loguru import logger

from src.models.game_state import GameState
from src.agents.movement import movement_agent
from src.agents.fighting import fighting_agent
from src.agents.strategy import strategy_agent


agent = Agent(
  "openai:gpt-4o",
  system_prompt=Path("src/prompts/master.md").read_text(),
  deps_type=GameState,
)

@agent.tool
def call_strategy_agent(_: RunContext, game_screen: str) -> str:
  """Call the strategy agent."""
  return strategy_agent.run_sync(game_screen).data

@agent.tool
def call_movement_agent(_: RunContext, game_screen: str) -> str:
  """Call the movement agent."""
  return movement_agent.run_sync(game_screen).data

@agent.tool
def call_fighting_agent(_: RunContext, game_screen: str) -> str:
  """Call the fighting agent."""
  return fighting_agent.run_sync(game_screen).data

def run_master_agent(game_screen: str) -> str:
  """Run the agent."""
  logger.info(f"Game state:\n{game_screen}")
  result = agent.run_sync(game_screen)

  model_messages = result.all_messages()
  logger.debug(f"Model messages:\n{model_messages}")

  model_output = result.data
  parsed_result = model_output.replace("```json", "").replace("```", "")
  parsed_result = json.loads(parsed_result)
  logger.info(f"Proposed action: {parsed_result['key']}")
  logger.info(f"Reason: {parsed_result['reason']}")


  return parsed_result
