"""Main module."""
import time
import sys
from loguru import logger

from src.game.game_handler import GameHandler
from src.models.game_state import GameState
from src.agents.master import run_master_agent

logger.remove()
logger.add(sys.stdout, level="DEBUG")

if __name__ == "__main__":
  game = GameHandler(dcss_path="dcss")
  game_state = GameState(
    game=game,
  )

  if game.start_game():
    time.sleep(1)
    try:
      while True:
        agent_action = run_master_agent(game_state)
        game.write_action(agent_action)

        time.sleep(0.2)
    except KeyboardInterrupt:
      logger.info("Game loop interrupted by the user")
    finally:
      game.close(save=True)
