from abc import ABC

import h3map
from h3map.header.conditions_readers.loss_conditions import loss_condition_readers, StandardLossConditionReader
from h3map.header.conditions_readers.winning_conditions import StandardWinningConditionReader, winning_condition_readers
from h3map.header.models import Header, Metadata, Version, MapProperties, Description, Difficulty, PlayerInfo, \
    WhoCanPlay, AiType, FactionInfo, Hero, TeamSetup

from h3map.header.constants import heroes
from h3map.parser import Parser


class MapReader(ABC):
    def __init__(self, parser):
        self.parser = parser
        self.heroes = []
        self.towns = []
        self.limit = len(heroes)

    @classmethod
    def parse(cls, map_contents):
        parser = Parser(map_contents)
        version = parser.uint32()
        reader = h3map.header.versions.supported_versions[version](parser)
        header = reader.read()
        return header

    def read(self):
        metadata = self.read_metadata()
        player_infos = self.read_player_infos()
        conditions = self.read_victory_loss_condition()
        team_setup = self.read_teams()
        allowed_heroes = self.read_allowed_heroes()
        return Header(metadata, player_infos, team_setup, allowed_heroes, conditions)

    def read_metadata(self):
        version = self.read_version()
        map_props = self.read_map_properties()
        description = self.read_description()
        difficulty = self.read_difficulty()
        return Metadata(version, map_props, description, difficulty)

    def read_version(self):
        return Version(self.version)

    def read_map_properties(self):
        any_players = self.parser.bool()
        height = self.parser.uint32()
        two_level = self.parser.bool()
        return MapProperties(height, two_level, any_players)

    def read_description(self):
        name = self.parser.string()
        desc = self.parser.string()
        return Description(name.decode("latin-1"), desc.decode("latin-1"))

    def read_difficulty(self):
        diff = self.parser.uint8()
        max_level = self.parser.uint8()
        return Difficulty(diff, max_level)

    def read_player_infos(self):
        players = []
        for player_num in range(0, 8):
            who_can_play = self.read_who_can_play()
            if who_can_play.nobody:
                self.parser.skip(13)
                continue

            player = PlayerInfo(
                who_can_play,
                self.read_ai_type(),
                self.read_faction_info(),
                self.read_town_info(),
                self.read_hero_properties(),
                self.read_heroes_belonging_to_player()
            )

            players.append(player)

        return players

    def read_who_can_play(self):
        can_human_play = self.parser.bool()
        can_computer_play = self.parser.bool()
        return WhoCanPlay(can_human_play, can_computer_play)

    def read_ai_type(self):
        ai_tactic = self.parser.uint8()
        _ = self.parser.uint8()
        return AiType(ai_tactic)

    def get_allowed_factions(self):
        total = self.parser.uint8()
        allowed = total + self.parser.uint8() * 256
        return [faction for i, faction in enumerate(self.towns[:total]) if (allowed & (1 << i))]

    def read_faction_info(self):
        allowed_factions = self.get_allowed_factions()
        is_faction_random = self.parser.bool()
        return FactionInfo(allowed_factions, is_faction_random)

    def read_town_info(self):
        has_main_town = self.parser.bool()

        if has_main_town:
            self.parser.bool()
            self.parser.bool()
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()

    def read_hero_properties(self):
        has_random_hero = self.parser.bool()
        main_custom_hero_id = self.parser.uint8()

        if main_custom_hero_id != 255:
            _id = self.parser.uint8()
            name = self.parser.string()

        return has_random_hero, main_custom_hero_id

    def read_heroes_belonging_to_player(self):
        _heroes = []
        self.parser.uint8()
        hero_count = self.parser.uint8()
        self.parser.skip(3)

        for i in range(0, hero_count):
            _id = self.parser.uint8()
            name = self.parser.string()
            _heroes.append(Hero(_id, name))

        return _heroes

    def read_teams(self):
        number_of_teams = self.parser.uint8()
        teams = []
        for player in range(0, 8):
            team_id = self.parser.uint8()
            teams.append(team_id)

        return TeamSetup(number_of_teams, teams)

    def read_allowed_heroes(self):
        negate = False
        allowed_heroes = [True] * self.limit
        for byte in range(0, 20):
            allowed = self.parser.uint8()
            for bit in range(0, 8):
                if byte * 8 + bit < self.limit:
                    flag = allowed & (1 << bit)
                    if (negate & flag) or ((not negate) & (not flag)):
                        allowed_heroes.insert(byte * 8 + bit, False)

        return [hero for i, hero in enumerate(self.heroes) if allowed_heroes[i]]

    def read_victory_loss_condition(self):
        return self.read_winning_condition(), self.read_loss_condition()

    def read_loss_condition(self):
        condition_reader = self._read_loss_condition()
        return condition_reader.read()

    def _read_loss_condition(self):
        condition = self.parser.uint8()
        if condition not in loss_condition_readers:
            return StandardLossConditionReader()
        return loss_condition_readers[condition](self.parser)

    def read_winning_condition(self):
        winning_reader = self._read_winning_condition()
        return winning_reader.read()

    def _read_winning_condition(self):
        condition = self.parser.uint8()
        if condition not in winning_condition_readers:
            return StandardWinningConditionReader(self.parser)

        return winning_condition_readers[condition](self.parser)

