from dataclasses import dataclass
from typing import List

from header.models.nodes import Metadata, Hero, PlayerInfo


@dataclass
class WogMetadata(Metadata):
    version: int
    any_players: bool
    size: int
    two_levels: bool
    name: str
    description: str
    difficulty: int
    max_level: int


@dataclass
class WogPlayers(Metadata):
    players_info: List[PlayerInfo]


class WogReader:
    factions = ["castle",
                "rampart",
                "tower",
                "necropolis",
                "inferno",
                "dungeon",
                "stronghold",
                "fortress",
                "conflux",
                "neutral"]

    def __init__(self, parser, version=51):
        self.version = version
        self.parser = parser

    def read(self):
        metadata = self._read_metadata()
        player_info = self._read_player_info()
        return metadata, player_info

    def _read_metadata(self):
        any_players = self.parser.bool()
        height = self.parser.uint32()
        two_level = self.parser.bool()
        name = self.parser.string()
        desc = self.parser.string()
        diff = self.parser.uint8()
        max_level = self.parser.uint8()

        return WogMetadata(self.version, any_players, height, two_level, name, desc, diff, max_level)

    def _read_player_info(self):
        players = []
        for player_num in range(0, 8):
            can_human_play = self.parser.bool()
            can_computer_play = self.parser.bool()
            if not (can_human_play or can_computer_play):
                self.parser.skip(13)
                continue

            ai_tactic = self.parser.uint8()
            p7 = self.parser.uint8()
            allowed_factions = self._get_allowed_factions()
            is_faction_random = self.parser.bool()
            has_main_town = self.parser.bool()

            if has_main_town:
                self.parser.bool()
                self.parser.bool()
                self.parser.uint8()
                self.parser.uint8()
                self.parser.uint8()

            has_random_hero = self.parser.bool()
            main_custom_hero_id = self.parser.uint8()

            if main_custom_hero_id != 255:
                _id = self.parser.uint8()
                name = self.parser.string()

            _heroes = []
            self.parser.uint8()
            hero_count = self.parser.uint8()
            self.parser.skip(3)

            for i in range(0, hero_count):
                _id = self.parser.uint8()
                name = self.parser.string()
                _heroes.append(Hero(_id, name))

            player = PlayerInfo(
                can_human_play,
                can_computer_play,
                ai_tactic,
                allowed_factions,
                p7,
                is_faction_random,
                has_main_town,
                has_random_hero,
                _heroes
            )

            players.append(player)

        return WogPlayers(players)

    def _read_teams(self):
        pass

    def _read_allowed_heroes(self):
        pass

    def _get_allowed_factions(self):
        total = self.parser.uint8()
        allowed = total + self.parser.uint8() * 256
        return [faction for i, faction in enumerate(self.factions[:total]) if (allowed & (1 << i))]