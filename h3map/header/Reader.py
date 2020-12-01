from dataclasses import dataclass
from typing import List

from header.RoeReader import RoeReader
from header.AbReader import AbReader
from header.SodReader import SodReader
from header.HotaReader import HotaReader
from header.WogReader import WogReader

from header.models.nodes import Metadata, PlayerInfo


@dataclass
class Header:
    metadata: Metadata
    players_info: List[PlayerInfo]
    teams: List[str]
    allowed_heroes: List[str]
    conditions: List[str]


class Reader:
    supported_versions = {
        14: RoeReader,
        21: AbReader,
        28: SodReader,
        30: HotaReader,
        31: HotaReader,
        32: HotaReader,
        51: WogReader,
    }

    def __init__(self, parser):
        self.limit = len(heroes)
        self.parser = parser

    def read(self):
        version = self.parser.uint32()
        reader = self._get_reader(version)

        metadata, player_info = reader.read()
        teams = self.read_teams()
        allowed_heroes = self.read_allowed_heroes()
        conditions = self.read_victory_loss_condition()

        return Header(metadata, player_info, teams, allowed_heroes, conditions)

    def read_teams(self):
        number_of_teams = self.parser.uint8()
        teams = []
        if number_of_teams > 0:
            for player in range(0, 8):
                team_id = self.parser.uint8()
                teams.append(team_id)
        else:
            pass
            for player in range(0, 8):
                # TODO: Exclude single player teams if they can't be played
                # if can_computer_play or can_human_play:
                team_id = self.parser.uint8()
                teams.append(team_id)

        return teams

    def read_allowed_heroes(self, negate=False):
        allowed_heroes = [True] * self.limit
        for byte in range(0, 20):
            allowed = self.parser.uint8()
            for bit in range(0, 8):
                if byte * 8 + bit < self.limit:
                    flag = allowed & (1 << bit)
                    if (negate & flag) or ((not negate) & (not flag)):
                        allowed_heroes.insert(byte * 8 + bit, False)

        return [hero for i, hero in enumerate(heroes) if allowed_heroes[i]]

    def _determine_loss_condition(self):
        loss_conditions = [
            "LOSSCASTLE",
            "LOSSHERO",
            "TIMEEXPIRES",
            "LOSSSTANDARD",
        ]

        loss = self.parser.uint8()
        if 3 < loss <= 255:
            return loss_conditions[-1]

        if loss == 0 or loss == 1:
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()
        elif loss == 3:
            self.parser.uint16()
        elif loss > 3:
            raise ValueError("Loss condition not found: ", loss)

        return loss_conditions[loss]

    def _determine_winning_condition(self):
        _conditions = [
            "ARTIFACT",
            "GATHERTROOP",
            "GATHERRESOURCE",
            "BUILDCITY",
            "BUILDGRAIL",
            "BEATHERO",
            "CAPTURECITY",
            "BEATMONSTER",
            "TAKEDWELLINGS",
            "TAKEMINES",
            "TRANSPORTITEM",
            "WINSTANDARD",
        ]

        _condition = self.parser.uint8()
        if 10 < _condition <= 255:
            return _conditions[-1]

        allow_normal_victory = self.parser.bool()
        applies_to_ai = self.parser.bool()

        if _condition == 0:
            self.parser.uint8()
            self.parser.skip(1)
        elif _condition == 1:
            self.parser.uint8()
            self.parser.skip(1)
            self.parser.uint32()
        elif _condition == 2:
            self.parser.uint8()
            self.parser.uint32()
        elif _condition == 3:
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()
        elif (4 <= _condition <= 7) or _condition == 10:
            self.parser.uint8()
            self.parser.uint8()
            self.parser.uint8()
        elif _condition > 10:
            raise ValueError("Winning condition not found: ", _condition)

        return _conditions[_condition]

    def read_victory_loss_condition(self):
        return self._determine_winning_condition(), self._determine_loss_condition()

    def _get_reader(self, version):
        return self.supported_versions[version](self.parser, version=version)


# TODO: Define all heroes
heroes = [
    "adela",
    "adelaide",
    "aenain",
    "aeris",
    "aine",
    "aislinn",
    "ajit",
    "alagar",
    "alamar",
    "alkin",
    "andra",
    "arlach",
    "ash",
    "astral",
    "axsis",
    "ayden",
    "brissa",
    "broghild",
    "bron",
    "caitlin",
    "calh",
    "calid",
    "charna",
    "christian",
    "ciele",
    "clancy",
    "clavius",
    "coronius",
    "cragHack",
    "cuthbert",
    "cyra",
    "dace",
    "damacon",
    "daremyth",
    "darkstorn",
    "deemer",
    "dessa",
    "drakon",
    "elleshar",
    "erdamon",
    "fafner",
    "fiona",
    "fiur",
    "galthran",
    "gelare",
    "gem",
    "geon",
    "gerwulf",
    "gird",
    "gretchin",
    "grindan",
    "gundula",
    "gunnar",
    "gurnisson",
    "halon",
    "ignatius",
    "ignissa",
    "inteus",
    "iona",
    "isra",
    "ivor",
    "jabarkas",
    "jaegar",
    "jeddite",
    "jenova",
    "josephine",
    "kalt",
    "korbac",
    "krellion",
    "kyrre",
    "labetha",
    "lacus",
    "lorelei",
    "loynis",
    "malcom",
    "malekith",
    "marius",
    "melodia",
    "mephala",
    "merist",
    "mirlanda",
    "moandor",
    "monere",
    "nagash",
    "neela",
    "nimbus",
    "nymus",
    "octavia",
    "olema",
    "oris",
    "pasis",
    "piquedram",
    "pyre",
    "rashka",
    "rion",
    "rissa",
    "rosic",
    "ryland",
    "sandro",
    "sanya",
    "saurug",
    "sephinroth",
    "septienna",
    "serena",
    "shakti",
    "shiva",
    "sirMullich",
    "solmyr",
    "straker",
    "styg",
    "sylvia",
    "synca",
    "tamika",
    "tazar",
    "terek",
    "thane",
    "thant",
    "theodorus",
    "thorgrim",
    "thunar",
    "tiva",
    "torosar ",
    "tyraxor",
    "tyris",
    "ufretin",
    "uland",
    "verdish",
    "vey",
    "vidomina",
    "vokial",
    "voy",
    "wystan",
    "xarfax",
    "xsi",
    "xyron",
    "yog",
    "zubin",
    "zydar"
]
