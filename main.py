"""Main module."""
import time
import loguru

from src.dcss_handler import DCSSHandler
from src.main_agent import MainAgent

logger = loguru.logger

if __name__ == "__main__":
  game = DCSSHandler(dcss_path="dcss")
  agent = MainAgent()

  if game.start_game():
    time.sleep(1)

    try:
      while game.is_game_running():
        game_state = game.read_output()
        if game_state:
          result = agent.get_agent_action(game_state)
          game.send_key(result["key"])
        time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Game loop interrupted by user")
    finally:
        game.close(save=True)
