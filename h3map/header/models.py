from abc import ABC
from dataclasses import dataclass
from typing import List


versions = {
    14: "Restoration of Erathia",
    21: "Armageddon's Blade",
    28: "Shadow of Death",
    30: "Horn of the Abyss",
    31: "Horn of the Abyss",
    32: "Horn of the Abyss",
    51: "Wake of Gods",
}


@dataclass
class Version(ABC):
    version: int

    def __repr__(self):
        return "{0}".format(versions[self.version])


@dataclass
class MapProperties(ABC):
    size: int
    two_levels: True
    any_players: bool


@dataclass
class Description(ABC):
    name: str
    summary: str


@dataclass
class Difficulty(ABC):
    difficulty: int
    max_hero_level: int


@dataclass
class AiType(ABC):
    ai_type: int


@dataclass
class HeroInfo(ABC):
    has_random_hero: bool
    hero_type: int


@dataclass
class TownInfo(ABC):
    has_main_town: bool


@dataclass
class FactionInfo(ABC):
    is_faction_random: bool
    factions: List[str]


@dataclass
class Metadata(ABC):
    version: Version
    properties: MapProperties
    description: Description
    difficulty: Difficulty

    def __repr__(self):
        return "Name: {0}\nVersion: {1}\n\nDescription: {2}\n" \
            .format(self.description.name.decode('latin-1'), self.version,
                    self.description.summary.decode('latin-1'))


@dataclass
class Hero(ABC):
    id: int
    name: str


@dataclass
class PlayerInfo(ABC):
    ai_type: AiType
    faction_info: FactionInfo
    town_info: TownInfo
    hero_properties: HeroInfo
    heroes: List[Hero]


@dataclass
class WhoCanPlay(ABC):
    can_human_play: bool
    can_computer_play: bool

    @property
    def nobody(self):
        return not (self.can_human_play or self.can_computer_play)


@dataclass
class Header(ABC):
    metadata: Metadata
    players_info: List[PlayerInfo]
    teams: List[str]
    alliances: bool
    allowed_heroes: List[str]
    conditions: List[str]

    def __repr__(self):
        return "{0}\n".format(self.metadata)
