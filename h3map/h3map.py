import glob
import gzip
import struct
import sys
from dataclasses import dataclass
from typing import List

from parser import Parser
from header.metadata import parse_header
from header.players import parse_player_info
from header.conditions import parse_victory_loss_condition
from header.teams import parse_team_info
from header.heroes import parse_allowed_heroes, heroes


def main(map_contents):
    parser = Parser(map_contents)
    version, name = parse_header(parser)
    players = parse_player_info(parser, version)
    win, loss = parse_victory_loss_condition(parser)
    teams = parse_team_info(parser)
    allowed_heroes = parse_allowed_heroes(parser, False, len(heroes))

    return name


if __name__ == "__main__":
    if len(sys.argv) < 2:
        map_files = glob.glob("reference_maps/*.h3m")
        for map_file in map_files:
            map_contents = gzip.open(map_file, 'rb').read()
            try:
                name = main(map_contents)
                print(name)
            except Exception as e:
                print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)
        print("Loaded {0} maps".format(len(map_files)))
    else:
        map_file = sys.argv[1]
        map_contents = gzip.open(map_file, 'rb').read()
        main(map_contents)
