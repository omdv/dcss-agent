"""Agent handler."""
import json
from pydantic_ai import Agent
from loguru import logger

class BasicAgent:
  """Handles the agent's actions."""

  def __init__(self) -> None:
    """Initialize the agent handler."""
    self.agent = Agent(
      "openai:gpt-4o",
      system_prompt="""
You are an agent that will play the "dungeon crawl stone soup" game.

Instructions:
1. You will get the screen of the game and the history of past 10 actions.
2. You will analyze the state of the game
3. You will propose a next keyboard button to be pressed
4. You will receive updated screen and repeat the process
5. Return only the result in JSON format with key and reason

json example: {"key": "string", "reason": "string"}

Additional instructions:
- If the game is new - pick a simple melee class
- If you repeat the same action - you may be stuck in a loop - try to avoid it
- To get the list of short keys - press '?', 'Esc' to return to the game
- To fire a weapon or wand - press 'f' and then select the target with movement keys
""",
    )

  def get_agent_action(self, game_state: str, action_history: list[dict]) -> str:
    """Get the agent's action."""
    logger.debug(f"Game state:\n{game_state}")
    result = self.agent.run_sync(
      f"Game state:\n{game_state}\nAction history:\n{action_history}").data
    result = result.replace("```json", "").replace("```", "")
    logger.debug(f"Agent action:\n{result}")
    return json.loads(result)
