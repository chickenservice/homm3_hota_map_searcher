import glob
import gzip

import click

from parser import Parser
from header.metadata import parse_header
from header.players import parse_player_info
from header.conditions import parse_victory_loss_condition
from header.teams import parse_team_info
from header.heroes import parse_allowed_heroes, heroes


def parse(map_contents):
    parser = Parser(map_contents)
    version, name, size = parse_header(parser)
    players = parse_player_info(parser, version)
    win, loss = parse_victory_loss_condition(parser)
    teams = parse_team_info(parser)
    allowed_heroes = parse_allowed_heroes(parser, False, len(heroes))

    return name, size


def load(files):
    maps = {}
    if not len(files):
        files = glob.glob("reference_maps/" + "*.h3m")
    for map_file in files:
        map_contents = gzip.open(map_file, 'rb').read()
        try:
            name, size = parse(map_contents)
            maps[name] = size
        except Exception as e:
            print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

    print("Loaded {0} maps".format(len(files)))
    return maps


@click.group()
def h3map():
    pass


@h3map.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--size', default="XL")
def filter(files, size):
    sizes = {"XL": 144}
    maps = load(files)
    for i, j in maps.items():
        if j == sizes[size]:
            print(i)


@h3map.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
def list_maps(files):
    maps = load(files)
    for i, j in maps.items():
        print(i)


if __name__ == "__main__":
    h3map()
