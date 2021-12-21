import abc

from h3map.header.map_reader import MapReader
from h3map.header.models import PlayerInfo

from h3map.header.models import AiType, FactionInfo
from h3map.header.models import HeroInfo, TownInfo


class HeroProperties(object):
    pass


class RoeReader(MapReader):
    def __init__(self, parser, version=14):
        self.version = version
        self.parser = parser
        self.towns = factions
        super().__init__(parser)

    def read_player_infos(self):
        players = []
        for player_num in range(0, 8):
            who_can_play = self.read_who_can_play()
            if who_can_play.nobody:
                self.parser.skip(6)
                continue

            ai = self.read_ai_type()
            faction = self.read_faction_info()
            hero = self.read_hero_properties()
            town = self.read_town_info()
            heroes = self.read_heroes_belonging_to_player(town, hero)

            player = PlayerInfo(player_num, who_can_play, ai, faction, town, hero, heroes)
            players.append(player)

        return players

    def read_ai_type(self):
        ai_tactic = self.parser.uint8()
        return AiType(ai_tactic)

    def read_faction_info(self):
        allowed_factions = self.get_allowed_factions()
        is_faction_random = self.parser.bool()
        return FactionInfo(allowed_factions, is_faction_random)

    def read_town_info(self):
        has_main_town = self.parser.bool()

        if has_main_town:
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()

        return TownInfo(has_main_town)

    def read_heroes_belonging_to_player(self, town_info, hero_type):
        if town_info and hero_type != 255:
            _id = self.parser.uint8()
        elif not town_info and hero_type != 255:
            _id = self.parser.uint8()

    def read_hero_properties(self):
        has_random_hero = self.parser.bool()
        hero_type = self.parser.uint8()
        return HeroInfo(has_random_hero, hero_type)

    def get_allowed_factions(self):
        total = self.parser.uint8()
        allowed = max(total - 1, 0)
        return [faction for i, faction in enumerate(self.towns[:total]) if (allowed & (1 << i))]

    def __repr__(self):
        return "Restoration of Erathia"


factions = ["castle",
            "rampart",
            "tower",
            "necropolis",
            "inferno",
            "dungeon",
            "stronghold",
            "fortress",
            "neutral"]

