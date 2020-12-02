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
class TeamSetup(ABC):
    number_of_teams: int
    teams: List[int]

    @property
    def alliance_possible(self):
        return self.number_of_teams > 0

    def __repr__(self):
        string = "Number of teams: {0}\n".format(self.number_of_teams)
        for team in self.teams:
            string += "Team {0}\n".format(team)

        return string


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
class Condition(ABC):
    pass


@dataclass
class LossCondition(Condition):
    pass


@dataclass()
class StandardLossCondition(LossCondition):
    number: int

    def __repr__(self):
        return "Standard loss condition"


@dataclass
class LoseSpecificTown(LossCondition):
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Lose a specific town"


@dataclass
class LoseSpecificHero(LossCondition):
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Lose a specific hero"


@dataclass()
class TimeExpires(LossCondition):
    days: int

    def __repr__(self):
        return "Lose on time"


@dataclass
class WinningCondition(Condition):
    allow_standard_win: bool
    can_ai_reach_artifact: bool


@dataclass
class StandardWinningCondition(WinningCondition):
    def __repr__(self):
        return "Standard winning condition"


@dataclass
class AcquireSpecificArtifact(WinningCondition):
    artifact_code: bool

    def __repr__(self):
        return "Acquire a specific artifact"


@dataclass
class AccumulateCreatures(WinningCondition):
    unit_code: int
    amount: int

    def __repr__(self):
        return "Accumulate creatures"


@dataclass
class AccumulateResources(WinningCondition):
    resource_code: int
    amount: int

    def __repr__(self):
        return "Accumulate resources"


@dataclass
class UpgradeSpecificTown(WinningCondition):
    x: int
    y: int
    z: int
    hall_level: int
    castle_level: int

    def __repr__(self):
        return "Upgrade a specific town"


@dataclass
class BuildGrailStructure(WinningCondition):
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Build the grail structure"


@dataclass
class DefeatSpecificHero(WinningCondition):
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Defeat specific hero"


@dataclass
class CaptureSpecificTown(WinningCondition):
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Capture a specific town"


@dataclass
class DefeatSpecificMonster(WinningCondition):
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Defeat specific monster"


@dataclass
class FlagAllCreatures(WinningCondition):
    def __repr__(self):
        return "Flag all creature dwellings"


@dataclass
class FlagAllMines(WinningCondition):
    def __repr__(self):
        return "Flag all mines"


@dataclass
class TransportSpecificArtifact(WinningCondition):
    artifact_code: int
    x: int
    y: int
    z: int

    def __repr__(self):
        return "Transport a specific item"


@dataclass
class Header(ABC):
    metadata: Metadata
    players_info: List[PlayerInfo]
    teams: TeamSetup
    allowed_heroes: List[str]
    conditions: List[Condition]

    def __repr__(self):
        string = "{0}\n".format(self.metadata)
        string += "{0}\n".format(self.teams)
        for condition in self.conditions:
            string += "Condition: {0}\n".format(condition)

        return string
