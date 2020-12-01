import glob
import gzip
import sys

import click

from parser import Parser
from header.metadata import parse_header
from header.players import parse_player_info
from header.conditions import parse_victory_loss_condition
from header.teams import parse_team_info
from header.heroes import parse_allowed_heroes, heroes


def parse(map_contents):
    parser = Parser(map_contents)
    version, name = parse_header(parser)
    players = parse_player_info(parser, version)
    win, loss = parse_victory_loss_condition(parser)
    teams = parse_team_info(parser)
    allowed_heroes = parse_allowed_heroes(parser, False, len(heroes))

    return name


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def h3map(files):
    if not len(files):
        files = glob.glob("reference_maps/" + "*.h3m")
    for map_file in files:
        map_contents = gzip.open(map_file, 'rb').read()
        try:
            name = parse(map_contents)
            print(name)
        except Exception as e:
            print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

    print("Loaded {0} maps".format(len(files)))


if __name__ == "__main__":
    h3map()
