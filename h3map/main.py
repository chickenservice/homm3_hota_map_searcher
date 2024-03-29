import sys

import cli_ui
import click

import h3map.rc

from h3map.show_my_maps.show_my_maps import ShowMyMapsView, ShowMyMaps


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if not ctx.invoked_subcommand:
        ShowMyMaps(ShowMyMapsView()).show()


@main.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--size', default=None)
@click.option('--teams', default=None)
@click.option('--team-players', nargs=1, default=None)
@click.option('--win', default=None)
@click.option('--loss', default=None)
@click.option('--detailed', is_flag=True)
def list_maps(files, size, teams, team_players, win, loss, detailed):
    controller = Library()

    cli_ui.info(cli_ui.bold, "Querying {0} maps".format((len(files))))

    maps = controller.load(files)
    filtered = controller.filter(maps.all(), size, teams, win, loss, team_players)

    view = ListDetailed(filtered) if detailed else List(filtered)
    view.show()

    cli_ui.info(cli_ui.bold, cli_ui.green, "\nFound {0} matching maps".format(len(filtered.all())))


if getattr(sys, "frozen", False):
    main(sys.argv[1:])


if __name__ == "__main__":
    ShowMyMaps(ShowMyMapsView()).show()
