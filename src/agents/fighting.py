"""Agent handler."""
from pathlib import Path
from pydantic_ai import Agent

fighting_agent = Agent(
  "openai:gpt-4o",
  system_prompt=Path("src/prompts/fighting.md").read_text(),
)
