import gzip
import struct
import sys
from dataclasses import dataclass
from typing import List


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
        assert size < 500000
        start, stop = self._next(size)
        pattern = self._get_format_string(size, 's')

        return struct.unpack(pattern, self.buffer[start:stop])[0]

    def skip(self, delta):
        self.current += min(len(self.buffer) - self.current, delta);


def parse_header(parser):
    version = parser.uint32()
    any_players = parser.bool()
    height = parser.uint32()
    two_level = parser.bool()
    name = parser.string()
    desc = parser.string()
    diff = parser.uint8()
    max_level = parser.uint8()

    print("Version: ", version)
    print("any players: ", any_players)
    print("height: ", height)
    print("two level: ", two_level)
    print("name: ", name)
    print("description: ", bytes.decode(desc, 'latin-1'))
    print("difficulty: ", diff)
    print("max hero level: ", max_level)


def get_allowed_factions(parser):
    factions = ["castle", "rampart", "tower", "necropolis", "inferno", "dungeon", "stronghold", "fortress", "conflux", "neutral"]
    allowed = parser.uint8() + parser.uint8()*256
    return [faction for i, faction in enumerate(factions) if (allowed & (1 << i))]


def parse_player_info(parser):
    players = []
    for player_num in range(0, 8):
        can_human_play = parser.bool()
        can_computer_play = parser.bool()
        if not (can_human_play or can_computer_play):
            parser.skip(13)
            continue

        ai_tactic = parser.uint8()
        p7 = parser.uint8()
        allowed_factions = get_allowed_factions(parser)
        is_faction_random = parser.bool()
        has_main_town = parser.bool()

        if has_main_town:
            parser.bool()
            parser.bool()
            parser.uint8()
            parser.uint8()
            parser.uint8()

        has_random_hero = parser.bool()
        main_custom_hero_id = parser.uint8()

        if main_custom_hero_id != 255:
            _id = parser.uint8()
            name = parser.string()

        parser.uint8()
        hero_count = parser.uint8()
        parser.skip(3)

        heroes = []
        for i in range(0, hero_count):
            _id = parser.uint8()
            name = parser.string()
            heroes.append(Hero(_id, name))

        player = PlayerInfo(
            can_human_play,
            can_computer_play,
            ai_tactic,
            allowed_factions,
            p7,
            is_faction_random,
            has_main_town,
            has_random_hero,
            heroes
        )

        players.append(player)

    return players

def parse_victory_loss_condition(parser):
    pass


def main(map_contents):
    parser = Parser(map_contents)
    parse_header(parser)
    players = parse_player_info(parser)
    print(players)
    parse_victory_loss_condition(parser)
    #parseTeamInfo()
    #parseAllowedHeroes()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("No map provided")

    map_file = sys.argv[1]
    map_contents = gzip.open(map_file, 'rb').read()
    main(map_contents)
