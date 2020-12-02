import glob
import gzip

import click

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
def h3map():
    pass


@h3map.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--size', default="XL")
def filter(files, size):
    sizes = {"XL": 144}
    maps = load(files)
    for i, j in maps.items():
        if j.metadata.properties.size == sizes[size]:
            print(i)


@h3map.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--detailed', is_flag=True)
def list_maps(files, detailed):
    maps = load(files)
    for i, j in maps.items():
        if detailed:
            print(j)
        else:
            print(j.metadata.description.name)

    print("Loaded {0} maps".format(len(maps)))
