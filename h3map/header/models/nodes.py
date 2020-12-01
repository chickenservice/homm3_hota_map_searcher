import abc
from dataclasses import dataclass
from typing import List


class Metadata(abc.ABC):
    pass


class PlayerInfo(abc.ABC):
    pass


@dataclass
class Hero:
    id: int
    name: str


@dataclass
class PlayerInfo:
    can_human_play: bool
    can_computer_play: bool
    ai_tactic: int
    p7: int
    allowed_factions: List[str]
    is_faction_random: bool
    has_main_town: bool
    has_random_hero: bool
    heroes: List[Hero]
