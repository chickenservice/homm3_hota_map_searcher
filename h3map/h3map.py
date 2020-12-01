import glob
import gzip
import struct
import sys
from dataclasses import dataclass
from typing import List

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

conditions = {
    0: "ARTIFACT",
    1: "GATHERTROOP",
    2: "GATHERRESOURCE",
    3: "BUILDCITY",
    4: "BUILDGRAIL",
    5: "BEATHERO",
    6: "CAPTURECITY",
    7: "BEATMONSTER",
    8: "TAKEDWELLINGS",
    9: "TAKEMINES",
    10: "TRANSPORTITEM",
    255: "WINSTANDARD",
}


@dataclass
class Hero:
    id: int
    name: str


@dataclass
class PlayerInfo:
    can_human_play: bool
    can_computer_play: bool
    ai_tactic: int
    p7: int
    allowed_factions: List[str]
    is_faction_random: bool
    has_main_town: bool
    has_random_hero: bool
    heroes: List[Hero]


class Parser:
    def __init__(self, buffer):
        self.buffer = buffer
        self.current = 0

    def _next(self, size):
        start = self.current
        stop = start + size
        self.current = stop

        return start, stop

    def _get_format_string(self, repetitions, character):
        return str(repetitions) + character

    def uint8(self):
        start, stop = self._next(1)
        return struct.unpack('B', self.buffer[start:stop])[0]

    def uint16(self):
        start, stop = self._next(4)
        return struct.unpack('I', self.buffer[start:stop])[0]

    def uint32(self):
        start, stop = self._next(4)
        return struct.unpack('I', self.buffer[start:stop])[0]

    def bool(self):
        start, stop = self._next(1)
        return struct.unpack('?', self.buffer[start:stop])[0]

    def uchar(self):
        start, stop = self._next(1)
        return struct.unpack('B', self.buffer[start:stop])[0]

    def string(self):
        size = self.uint32()
        if size > 500000:
            raise ValueError("Size too big for string.")
        start, stop = self._next(size)
        pattern = self._get_format_string(size, 's')

        return struct.unpack(pattern, self.buffer[start:stop])[0]

    def skip(self, delta):
        self.current += min(len(self.buffer) - self.current, delta);


def parse_header(parser):
    version = parser.uint32()
    if 30 <= version <= 32:
        parser.uint32()
        parser.uint8()

    any_players = parser.bool()
    if 30 <= version <= 32:
        parser.uint8()

    height = parser.uint32()
    two_level = parser.bool()
    name = parser.string()
    desc = parser.string()
    diff = parser.uint8()
    max_level = parser.uint8()

    print("Version: ", version)
    print("name: ", name)

    return version


def get_allowed_factions(parser, version):
    factions = ["castle", "rampart", "tower", "necropolis", "inferno", "dungeon", "stronghold", "fortress", "conflux",
                "neutral"]
    total = parser.uint8()
    allowed = total
    if version != 14:
        allowed = total + parser.uint8() * 256
    else:
        total -= 1
    return [faction for i, faction in enumerate(factions[:total]) if (allowed & (1 << i))]


def parse_player_info(parser, version):
    # INVALID = 0,
    # // HEX
    # DEC
    # ROE = 0x0e, // 14
    # AB = 0x15, // 21
    # SOD = 0x1c, // 28
    #
    # // HOTA = 0x1e...
    # 0x20 // 28...
    # 30
    # WOG = 0x33, // 51
    # VCMI = 0xF0
    players = []
    for player_num in range(0, 8):
        can_human_play = parser.bool()
        can_computer_play = parser.bool()
        if not (can_human_play or can_computer_play):
            if 28 <= version <= 33:
                parser.skip(13)
            elif version == 21:
                parser.skip(12)
            elif version == 14:
                parser.skip(6)
            continue

        ai_tactic = parser.uint8()
        p7 = -1
        if 28 <= version <= 33:
            p7 = parser.uint8()
        allowed_factions = get_allowed_factions(parser, version)
        is_faction_random = parser.bool()
        has_main_town = parser.bool()

        if has_main_town:
            if version != 14:
                parser.bool()
                parser.bool()
            parser.uint8()
            parser.uint8()
            parser.uint8()

        has_random_hero = parser.bool()
        main_custom_hero_id = parser.uint8()

        if main_custom_hero_id != 255 and version != 14:
            _id = parser.uint8()
            name = parser.string()

        parser.uint8()
        hero_count = parser.uint8()
        parser.skip(3)

        _heroes = []
        if version != 14:
            for i in range(0, hero_count):
                _id = parser.uint8()
                name = parser.string()
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

    return players


def determine_loss_condition(parser):
    loss_conditions = [
        "LOSSCASTLE",
        "LOSSHERO",
        "TIMEEXPIRES",
        "LOSSSTANDARD",
    ]

    loss = parser.uint8()
    if 3 < loss <= 255:
        return loss_conditions[-1]

    if loss == 0 or loss == 1:
        parser.uint8()
        parser.uint8()
        parser.uint8()
    elif loss == 3:
        parser.uint16()
    elif loss > 3:
        raise ValueError("Loss condition not found: ", loss)

    return loss_conditions[loss]


def determine_winning_condition(parser):
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

    _condition = parser.uint8()
    if 10 < _condition <= 255:
        return _conditions[-1]

    allow_normal_victory = parser.bool()
    applies_to_ai = parser.bool()

    if _condition == 0:
        parser.uint8()
        parser.skip(1)
    elif _condition == 1:
        parser.uint8()
        parser.skip(1)
        parser.uint32()
    elif _condition == 2:
        parser.uint8()
        parser.uint32()
    elif _condition == 3:
        parser.uint8()
        parser.uint8()
        parser.uint8()
        parser.uint8()
        parser.uint8()
    elif (4 <= _condition <= 7) or _condition == 10:
        parser.uint8()
        parser.uint8()
        parser.uint8()
    elif _condition > 10:
        raise ValueError("Winning condition not found: ", _condition)

    return _conditions[_condition]


def parse_victory_loss_condition(parser):
    return determine_winning_condition(parser), determine_loss_condition(parser)


def parse_team_info(parser):
    number_of_teams = parser.uint8()
    teams = []
    if number_of_teams > 0:
        for player in range(0, 8):
            team_id = parser.uint8()
            teams.append(team_id)
    else:
        pass
        for player in range(0, 8):
            # TODO: Exclude single player teams if they can't be played
            # if can_computer_play or can_human_play:
            team_id = parser.uint8()
            teams.append(team_id)

    return teams


def parse_allowed_heroes(parser, negate, limit):
    allowed_heroes = [True] * limit
    for byte in range(0, 20):
        allowed = parser.uint8()
        for bit in range(0, 8):
            if byte * 8 + bit < limit:
                flag = allowed & (1 << bit)
                if (negate & flag) or ((not negate) & (not flag)):
                    allowed_heroes.insert(byte * 8 + bit, False)

    return [hero for i, hero in enumerate(heroes) if allowed_heroes[i]]


def main(map_contents):
    parser = Parser(map_contents)
    version = parse_header(parser)
    players = parse_player_info(parser, version)
    win, loss = parse_victory_loss_condition(parser)
    teams = parse_team_info(parser)
    allowed_heroes = parse_allowed_heroes(parser, False, len(heroes))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        map_files = glob.glob("reference_maps/*.h3m")
        for map_file in map_files:
            map_contents = gzip.open(map_file, 'rb').read()
            try:
                main(map_contents)
            except ValueError as e:
                print("Sorry map couldn't be loaded due to an error: ", e)
    else:
        map_file = sys.argv[1]
        map_contents = gzip.open(map_file, 'rb').read()
        main(map_contents)
