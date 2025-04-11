"""Main module."""
import time
import sys
from loguru import logger

from src.game.game_handler import GameHandler
from src.agents.master import run_master_agent

logger.remove()
logger.add(sys.stdout, level="DEBUG")

if __name__ == "__main__":
  game = GameHandler(dcss_path="dcss")

  if game.start_game():
    time.sleep(1)
    try:
      while True:
        game_state = game.get_game_state()
        action_history = game.get_action_history()

        master_action = run_master_agent(game_state)
        game.write_action(master_action)

        time.sleep(2)
    except KeyboardInterrupt:
      logger.info("Game loop interrupted by user")
    finally:
      game.close(save=True)
