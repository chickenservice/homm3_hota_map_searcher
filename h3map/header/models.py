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
    factions: List[str]
    is_faction_random: bool


@dataclass
class TeamSetup(ABC):
    number_of_teams: int
    teams: List[int]

    @property
    def possible_teams(self):
        return map(self.teams, )

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
    thumbnail: str = "default.gif"

    def __repr__(self):
        return "Name: {0}\nVersion: {1}\n\nDescription: {2}\n" \
            .format(self.description.name.decode('latin-1'), self.version,
                    self.description.summary.decode('latin-1'))


@dataclass
class Hero(ABC):
    id: int
    name: str


@dataclass
class WhoCanPlay(ABC):
    can_human_play: bool
    can_computer_play: bool

    @property
    def nobody(self):
        return not (self.can_human_play or self.can_computer_play)


@dataclass
class PlayerInfo(ABC):
    id: int
    who_can_play: WhoCanPlay
    ai_type: AiType
    faction_info: FactionInfo
    town_info: TownInfo
    hero_properties: HeroInfo
    heroes: List[Hero]


@dataclass
class Condition(ABC):
    pass


@dataclass
class LossCondition(Condition):
    pass


@dataclass
class StandardLossCondition(LossCondition):
    number: int
    id: int = 0

    def __repr__(self):
        return "Standard loss condition"


@dataclass
class LoseSpecificTown(LossCondition):
    x: int
    y: int
    z: int
    id: int = 1

    def __repr__(self):
        return "Lose a specific town"


@dataclass
class LoseSpecificHero(LossCondition):
    x: int
    y: int
    z: int
    id: int = 2

    def __repr__(self):
        return "Lose a specific hero"


@dataclass
class TimeExpires(LossCondition):
    days: int
    id: int = 3

    def __repr__(self):
        return "Lose on time"


@dataclass
class WinningCondition(Condition):
    allow_standard_win: bool
    can_ai_reach_artifact: bool


@dataclass
class StandardWinningCondition(WinningCondition):
    id: int = 0

    def __repr__(self):
        return "Standard winning condition"


@dataclass
class AcquireSpecificArtifact(WinningCondition):
    artifact_code: bool
    id: int = 1

    def __repr__(self):
        return "Acquire a specific artifact"


@dataclass
class AccumulateCreatures(WinningCondition):
    unit_code: int
    amount: int
    id: int = 2

    def __repr__(self):
        return "Accumulate creatures"


@dataclass
class AccumulateResources(WinningCondition):
    resource_code: int
    amount: int
    id: int = 3

    def __repr__(self):
        return "Accumulate resources"


@dataclass
class UpgradeSpecificTown(WinningCondition):
    x: int
    y: int
    z: int
    hall_level: int
    castle_level: int
    id: int = 4

    def __repr__(self):
        return "Upgrade a specific town"


@dataclass
class BuildGrailStructure(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 5

    def __repr__(self):
        return "Build the grail structure"


@dataclass
class DefeatSpecificHero(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 6

    def __repr__(self):
        return "Defeat specific hero"


@dataclass
class CaptureSpecificTown(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 7

    def __repr__(self):
        return "Capture a specific town"


@dataclass
class DefeatSpecificMonster(WinningCondition):
    x: int
    y: int
    z: int
    id: int = 8

    def __repr__(self):
        return "Defeat specific monster"


@dataclass
class FlagAllCreatures(WinningCondition):
    id: int = 9

    def __repr__(self):
        return "Flag all creature dwellings"


@dataclass
class FlagAllMines(WinningCondition):
    id: int = 10

    def __repr__(self):
        return "Flag all mines"


@dataclass
class TransportSpecificArtifact(WinningCondition):
    artifact_code: int
    x: int
    y: int
    z: int
    id: int = 11

    def __repr__(self):
        return "Transport a specific item"


@dataclass
class Header(ABC):
    metadata: Metadata
    players_info: List[PlayerInfo]
    teams: TeamSetup
    allowed_heroes: List[str]
    conditions: List[Condition]
    file_path: str = ""

    def humans(self):
        return len([player for player in self.players_info if player.who_can_play.can_human_play])

    @property
    def winning_condition(self):
        return self.conditions[0].id

    @property
    def loss_condition(self):
        return self.conditions[1].id

    def __repr__(self):
        string = "{0}\n".format(self.metadata)
        string += "{0}\n".format(self.teams)
        for condition in self.conditions:
            string += "Condition: {0}\n".format(condition)

        return string
