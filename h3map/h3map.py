import glob
import gzip

import cli_ui
import click
from click import BadParameter, UsageError

from h3map.cli import ListDetailed, List
from h3map.filter import HeaderFilter
from h3map.parser import Parser
from h3map.header.versions import supported_versions


def parse(map_contents):
    parser = Parser(map_contents)
    version = parser.uint32()
    reader = supported_versions[version](parser)
    header = reader.read()
    return header


def load(files):
    maps = {}
    if not len(files):
        files = glob.glob("*.h3m")
    for i, map_file in enumerate(files):
        cli_ui.info_count(i, len(files), "maps loaded")
        map_contents = gzip.open(map_file, 'rb').read()
        try:
            header = parse(map_contents)
            maps[map_file] = header
        except Exception as e:
            print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

    return maps


@click.group()
def h3map():
    pass


@h3map.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--size', default=None)
@click.option('--teams', default=None)
@click.option('--team-players', nargs=1, default=None)
@click.option('--win', default=None)
@click.option('--loss', default=None)
@click.option('--detailed', is_flag=True)
def list_maps(files, size, teams, team_players, win, loss, detailed):
    maps = load(files)

    header_filter = HeaderFilter()
    if size is not None:
        header_filter.has_map_size(size)
    if teams is not None:
        header_filter.has_team_size(int(teams))
    if win is not None:
        header_filter.has_win_or_loss_condition(win)
    if loss is not None:
        header_filter.has_win_or_loss_condition(loss)
    if team_players is not None:
        if teams is None:
            raise UsageError("Cannot specify number of players per team without number of teams.")

        header_filter.team_has_players(int(team_players))

    filtered = header_filter.apply(maps.values())

    view = (ListDetailed() if detailed else List())
    view.show(filtered)

    cli_ui.info_1("\nFound {0} maps".format(len(filtered)))
