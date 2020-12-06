import cli_ui
import click

from h3map.cli import ListDetailed, List
from h3map.controller import MainController
from h3map.gui import App


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if not ctx.invoked_subcommand:
        App.run()


@main.command(name="list")
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--size', default=None)
@click.option('--teams', default=None)
@click.option('--team-players', nargs=1, default=None)
@click.option('--win', default=None)
@click.option('--loss', default=None)
@click.option('--detailed', is_flag=True)
def list_maps(files, size, teams, team_players, win, loss, detailed):
    controller = MainController()

    cli_ui.info(cli_ui.bold, "Querying {0} maps".format((len(files))))

    maps = controller.load(files)
    filtered = controller.filter(maps.all(), size, teams, win, loss, team_players)

    view = ListDetailed(filtered) if detailed else List(filtered)
    view.show()

    cli_ui.info(cli_ui.bold, cli_ui.green, "\nFound {0} matching maps".format(len(filtered.all())))

if __name__ == "__main__":
    main(None)