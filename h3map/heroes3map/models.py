from dataclasses import dataclass
from typing import List

from h3map.heroes3map.loss_conditions import LossCondition
from h3map.heroes3map.winning_conditions import WinningCondition

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
class Hero:
    id: int
    name: str

@dataclass
class HotaMetadataV2:
    mirror: bool
    hota_arena: int
    terrain_count: int


@dataclass
class HotaMetadataV1:
    mirror: bool
    hota_arena: int


@dataclass
class HotaMetadata:
    additional: any
    size: int
    two_level: True
    any_players: bool
    name: str
    description: str
    difficulty: int
    max_hero_level: int = 4
    unknown: int = 0,
    unknown2: int = 0,
    minor: int = 0,
    patch: int = 0,


@dataclass
class Metadata:
    size: int
    two_level: True
    any_players: bool
    name: str
    description: str
    difficulty: int
    max_hero_level: int = 4
    unknown: int = 0,
    unknown2: int = 0,
    minor: int = 0,
    patch: int = 0,


@dataclass
class AiType:
    ai_type: int
    aggressiveness: int = -1


@dataclass
class HeroInfo:
    has_random_hero: bool
    hero_type: int
    some: int
    random: int


@dataclass
class CustomHeroInfo:
    has_random_hero: bool
    custom: Hero


@dataclass
class TownInfo:
    # has_main_town: bool
    x: int
    y: int
    z: int
    a: int = 0
    b: int = 0


@dataclass
class FactionInfo:
    factions: List[str]
    is_faction_random: bool


@dataclass
class TeamSetup:
    teams: List[int]
    number_of_teams: int

    @property
    def possible_teams(self):
        return map(self.teams, )

    @property
    def alliance_possible(self):
        return self.number_of_teams > 0


@dataclass
class PlayerInfo:
    can_human_play: bool
    can_computer_play: bool
    ai_type: AiType
    faction_info: FactionInfo
    town_info: TownInfo
    hero_properties: HeroInfo
    heroes: List[Hero] = None


@dataclass
class Header:
    metadata: Metadata
    player_infos: List[PlayerInfo]
    winning_condition: WinningCondition
    loss_condition: LossCondition
    teams: TeamSetup
    allowed_heroes: List[str]
    file_path: str = ""

    def humans(self):
        return len([player for player in self.player_infos if player.who_can_play.can_human_play])

    def __str__(self):
        string = f"{self.metadata}\n"
        string += "{}\n".format("\n".join(str(p) for p in self.player_infos))
        string += f"{self.teams}\n"
        string += f"Winning condition: {self.winning_condition}\n"
        string += f"Loss condition: {self.loss_condition}\n"
        string += f"Allowed heroes: {self.allowed_heroes}"

        return string


@dataclass
class H3map:
    version: int
    header: Header
