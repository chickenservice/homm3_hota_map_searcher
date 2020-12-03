import glob
import gzip

import click

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
        map_contents = gzip.open(map_file, 'rb').read()
        try:
            header = parse(map_contents)
            maps[map_file] = header
        except Exception as e:
            print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

    return maps


@click.group()
@click.option('--detailed', is_flag=True)
@click.pass_context
def h3map(ctx, detailed):

    ctx.obj = ListDetailed() if detailed is not None else List()


@h3map.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--size', default="XL")
@click.option('--teams', default=None)
@click.option('--win', default=None)
@click.option('--loss', default=None)
@click.option('--detailed', is_flag=True)
@click.pass_context
def filter(ctx, detailed, files, size, teams, win, loss):
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

    filtered = header_filter.apply(maps.values())

    ctx.obj.show(filtered)


@h3map.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--detailed', is_flag=True)
@click.pass_context
def list_maps(ctx, files, detailed):
    maps = load(files)
    ctx.obj.show(maps.values())

    print("Loaded {0} maps".format(len(maps)))
