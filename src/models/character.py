"""Character model."""
from pydantic import BaseModel

class Resource(BaseModel):
  """Resource model."""

  current: int
  max: int


class Stats(BaseModel):
  """Stats model."""

  health: Resource
  magic: Resource
  ac: int
  ev: int
  sh: int
  strength: int
  intelligence: int
  dexterity: int
  xp_level: int
  xp_progress: str
  noise: str | None = None


class Location(BaseModel):
  """Location model."""

  branch: str
  level: int


class Equipment(BaseModel):
  """Equipment model."""

  weapon: str | None
  shield: str | None
  body: str | None
  helmet: str | None
  cloak: str | None
  gloves: str | None
  boots: str | None
  barding: str | None
  amulet: str | None
  ring_left: str | None
  ring_right: str | None

class Skill(BaseModel):
  """Skill model."""

  key: str
  training_flag: bool
  name: str
  level: int
  train_progress: int
  aptitude: int

class Resistances(BaseModel):
  """Resistances model."""

  rFire: int
  rCold: int
  rNeg: int
  rPois: int
  rElec: int
  rCorr: int
  SInv: int

class Status(BaseModel):
  """Status model."""

  will: int
  stealth: int
  hp_regen: float
  mp_regen: float
  passive_effects: list[str]
  status_effects: list[str]
  mutations: list[str]


class Spells(BaseModel):
  """Spells model."""

  slots_used: int
  slots_max: int
  known: list[str]


class DCSSCharacter(BaseModel):
  """DCSS character model."""

  name: str
  title: str
  species: str
  background: str
  turns: int
  time: str
  stats: Stats
  god: str | None
  gold: int
  abilities: list[str]
  skills: list[Skill]
  equipment: Equipment
  resistances: Resistances
  status: Status
  spells: Spells
  strategy_notes: str | None
