import gzip
import struct
import sys


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
        return struct.unpack('H', self.buffer[start:stop])[0]

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
        start, stop = self._next(size)
        pattern = self._get_format_string(size, 's')

        return struct.unpack(pattern, self.buffer[start:stop])[0]


def parse_header(parser):
    version = parser.uint32()
    any_players = parser.bool()
    height = parser.uint32()
    two_level = parser.bool()
    name = parser.string()
    desc = parser.string()
    diff = parser.uchar()
    max_level = parser.uchar()

    print("Version: ", version)
    print("any players: ", any_players)
    print("height: ", height)
    print("two level: ", two_level)
    print("name: ", name)
    print("description: ", desc)
    print("difficulty: ", diff)
    print("max hero level: ", max_level)


def parse_player_info(content):
    pass



def main(map_contents):
    parser = Parser(map_contents)
    parse_header(parser)
    #parse_player_info(remaining)
    #parse_victory_loss_conditions()
    #parseTeamInfo()
    #parseAllowedHeroes()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("No map provided")

    map_file = sys.argv[1]
    map_contents = gzip.open(map_file, 'rb').read()
    main(map_contents)
