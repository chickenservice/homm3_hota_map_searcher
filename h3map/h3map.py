import glob
import gzip

import click

from parser import Parser
import header.Reader as Reader


def parse(map_contents):
    parser = Parser(map_contents)
    reader = Reader.Reader(parser)
    header = reader.read()

    return header.metadata.name, header.metadata.size


def load(files):
    maps = {}
    if not len(files):
        files = glob.glob("reference_maps/" + "*.h3m")
    for i, map_file in enumerate(files):
        map_contents = gzip.open(map_file, 'rb').read()
        try:
            name, size = parse(map_contents)
            maps[map_file] = size
            print(name)
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
        if j == sizes[size]:
            print(i)


@h3map.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
def list_maps(files):
    maps = load(files)
    for i, j in maps.items():
        print(i)

    print("Loaded {0} maps".format(len(maps)))


if __name__ == "__main__":
    h3map()
