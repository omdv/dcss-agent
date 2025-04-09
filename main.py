"""Main module."""
import time
import sys
from loguru import logger

from src.game.game_handler import GameHandler
from src.agents.basic import BasicAgent

logger.remove()
logger.add(sys.stdout, level="DEBUG")

if __name__ == "__main__":
  game = GameHandler(dcss_path="dcss")
  basic_agent = BasicAgent()

  if game.start_game():
    time.sleep(1)
    try:
      while True:
        game_state = game.get_game_state()
        action_history = game.get_action_history()

        basic_action = basic_agent.get_agent_action(game_state, action_history)
        game.write_action(basic_action)

        time.sleep(0.2)
    except KeyboardInterrupt:
      logger.info("Game loop interrupted by user")
    finally:
      game.close(save=True)
