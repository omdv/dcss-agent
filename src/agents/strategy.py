"""Agent handler."""
import json
from pydantic_ai import Agent
from src.models.game_state import GameState

strategy_agent = Agent(
  "openai:gpt-4o",
  deps_type=GameState,
  system_prompt="""
You are the supporting agent playing the "dungeon crawl stone soup" game. \
You will receive the game screen with the character description and will return \
the strategy in raw text. You will also return "esc" key to close the character \
screen.

You will return the following JSON:
{
  "reason": "here you will describe the strategy in raw text",
  "key": "esc"
}
""",
)

def create_strategy(game_screen: str) -> None:
  """Create a strategy for the main agent to follow."""
  model_output = strategy_agent.run_sync(game_screen).data

  parsed_result = model_output.replace("```json", "").replace("```", "")
  parsed_result = json.loads(parsed_result)

  GameState(strategy=parsed_result["reason"])
  GameState.save()
  return json.loads(parsed_result)
