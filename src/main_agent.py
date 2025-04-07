"""Agent handler."""
import json
from pydantic_ai import Agent
from loguru import logger

class MainAgent:
  """Handles the agent's actions."""

  def __init__(self) -> None:
    """Initialize the agent handler."""
    self.agent = Agent(
      "openai:gpt-4o",
      system_prompt="""
You are an agent that needs to win "dungeon crawl stone soup" game. \
You will get the screen and you will give interpretation of the game state and \
propose a next keyboard button to be pressed. When you get the initial screen - choose \
to continue the existing save game. If save game is not available - start a new game, \
pick a beginner friendly character. Be concise. Return result in JSON format. \
Use lowercase letters for keys. Example: {"key": "string", "reason": "string"}""",
    )

  def get_agent_action(self, game_state: str) -> str:
    """Get the agent's action."""
    result = self.agent.run_sync(game_state).data
    result = result.replace("```json", "").replace("```", "")

    result = json.loads(result)
    logger.debug(f"Sent key: {result['key']}")
    logger.debug(f"Reason: {result['reason']}")
    return result
