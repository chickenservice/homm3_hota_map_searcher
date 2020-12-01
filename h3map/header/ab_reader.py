from h3map.header.map_reader import MapReader
from h3map.header.models import PlayerInfo, AiType


class AbReader(MapReader):
    def __init__(self, parser, version=21):
        self.version = version
        self.towns = factions
        super().__init__(parser)

    def read_player_infos(self):
        players = []
        for player_num in range(0, 8):
            who_can_play = self.read_who_can_play()
            if who_can_play.nobody:
                self.parser.skip(12)
                continue

            player = PlayerInfo(
                self.read_ai_type(),
                self.read_faction_info(),
                self.read_town_info(),
                self.read_hero_properties(),
                self.read_heroes_belonging_to_player()
            )

            players.append(player)

        return players

    def read_ai_type(self):
        ai_tactic = self.parser.uint8()
        return AiType(ai_tactic)

    def __repr__(self):
        return "Armageddon's Blade"


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

