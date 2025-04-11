"""Agent handler."""
from pathlib import Path
from pydantic_ai import Agent

movement_agent = Agent(
  "openai:gpt-4o",
  system_prompt=Path("src/prompts/movement.md").read_text(),
)
