"""Main module."""
import time
from loguru import logger

from src.dcss_handler import DCSSHandler
from src.agents.state import StateAgent
from src.agents.skills import SkillsAgent

if __name__ == "__main__":
  game = DCSSHandler(dcss_path="dcss")
  state_agent = StateAgent(game_handler=game)
  skills_agent = SkillsAgent(game_handler=game)
  if game.start_game():
    time.sleep(1)
    try:
      game.send_key("tab")
      time.sleep(1)
      character_state = state_agent.get_character_state()
      logger.info(character_state)
      time.sleep(1)
      skills_plan = skills_agent.get_skills_plan(character_state)
      logger.info(skills_plan)
      time.sleep(1)


    except KeyboardInterrupt:
      logger.info("Game loop interrupted by user")
    finally:
      game.close(save=True)
