from dataclasses import dataclass

from header.models.nodes import Metadata, PlayerInfo, Hero


@dataclass
class RoeMetadata(Metadata):
    version: int
    any_players: bool
    size: int
    two_levels: bool
    name: str
    description: str
    difficulty: int
    max_level: int


class RoeReader:
    factions = ["castle",
                "rampart",
                "tower",
                "necropolis",
                "inferno",
                "dungeon",
                "stronghold",
                "fortress",
                "neutral"]

    def __init__(self, parser, version=14):
        self.version = version
        self.parser = parser

    def read(self):
        metadata = self._read_metadata()
        player_info = self._read_player_info()
        teams = self._read_teams()
        allowed_heroes = self._read_allowed_heroes()
        return metadata, player_info, teams, allowed_heroes

    def _read_metadata(self):
        any_players = self.parser.bool()
        height = self.parser.uint32()
        two_level = self.parser.bool()
        name = self.parser.string()
        desc = self.parser.string()
        diff = self.parser.uint8()
        max_level = self.parser.uint8()

        return RoeMetadata(self.version, any_players, height, two_level, name, desc, diff, max_level)

    def _read_player_info(self):
        players = []
        for player_num in range(0, 8):
            can_human_play = self.parser.bool()
            can_computer_play = self.parser.bool()
            if not (can_human_play or can_computer_play):
                self.parser.skip(6)
                continue

            ai_tactic = self.parser.uint8()
            allowed_factions = self._get_allowed_factions()
            is_faction_random = self.parser.bool()
            has_main_town = self.parser.bool()

            if has_main_town:
                self.parser.uint8()
                self.parser.uint8()
                self.parser.uint8()

            has_random_hero = self.parser.bool()
            main_custom_hero_id = self.parser.uint8()

            # TODO: Add proper handling for different ROE extensions:
            # https://github.com/potmdehex/homm3tools/blob/h3mlibhota/h3m/h3mlib/h3m_parsing/parse_players.c
            if has_main_town and main_custom_hero_id != 255:
                _id = self.parser.uint8()
            elif not has_main_town and main_custom_hero_id != 255:
                _id = self.parser.uint8()

            _heroes = []
            p7 = -1
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

        return players

    def _read_teams(self):
        pass

    def _read_allowed_heroes(self):
        pass

    def _get_allowed_factions(self):
        total = self.parser.uint8()
        allowed = max(total - 1, 0)
        return [faction for i, faction in enumerate(self.factions[:total]) if (allowed & (1 << i))]

