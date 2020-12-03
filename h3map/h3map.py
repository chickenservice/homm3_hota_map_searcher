import glob
import gzip
from tkinter import ttk, Grid

import cli_ui
import click
from click import UsageError
from ttkthemes import ThemedStyle

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
    cli_ui.info(cli_ui.bold, "Querying {0} maps".format((len(files))))
    print()
    for i, map_file in enumerate(files):
        map_contents = gzip.open(map_file, 'rb').read()
        try:
            header = parse(map_contents)
            maps[map_file] = header
        except Exception as e:
            print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

    return maps


@click.group(invoke_without_command=True)
@click.pass_context
def h3map(ctx):
    if not ctx.invoked_subcommand:
        import tkinter as tk
        from tkinter.filedialog import askopenfilenames

        class App(tk.Frame):
            def __init__(self, master=None):
                super().__init__(master)
                self.master = master
                self.pack(fill="both", expand=True)
                self.maps = {}
                self.create_widgets()
                self.header_filter = HeaderFilter()

            def create_widgets(self):
                Grid.columnconfigure(self, 0, weight=2)
                Grid.columnconfigure(self, 1, weight=2)
                Grid.rowconfigure(self, 0, weight=1)
                Grid.rowconfigure(self, 1, weight=15)

                self.load = tk.Button(self, text="Load maps", command=self._load)
                self.load.grid(row=0, column=0)

                self.var = tk.StringVar()
                self.var.set("XL")
                self.size = tk.OptionMenu(self, self.var, "XL", "L", "M", "S")
                self.size.grid(row=0, column=2)

                self.filter = tk.Button(self, text="Filter", command=self.filter_size)
                self.filter.grid(row=0, column=1)

                self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
                self.quit.grid(row=0, column=3)

                panes = tk.PanedWindow(self)
                panes.grid(row=1, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

                self.maps_view = tk.Listbox(panes)

                self.v = tk.StringVar()
                self.map_detail_view = tk.Text(panes, height=2)
                self.maps_view.bind('<<ListboxSelect>>', self.onclick)

                panes.add(self.maps_view, stretch="always")
                panes.add(self.map_detail_view, stretch="always")

            def _load(self):
                files = askopenfilenames()
                maps = load(files)
                for header in maps.values():
                    self.maps[header.metadata.description.name] = header
                    self.maps_view.insert(1, header.metadata.description.name)

                self.v.set(list(maps.values())[0])

            def filter_size(self):
                self.header_filter = HeaderFilter()
                self.header_filter.has_map_size(self.var.get())

                maps = self.header_filter.apply(self.maps.values())
                self.maps_view.delete(1, tk.END)
                for header in maps:
                    self.maps_view.insert(1, header.metadata.description.name)

            def onclick(self, event):
                w = event.widget
                selection = w.curselection()
                if len(selection):
                    idx = int(selection[0])
                    value = w.get(idx)
                    self.map_detail_view.config(state=tk.NORMAL)
                    self.map_detail_view.delete("1.0", tk.END)
                    self.map_detail_view.insert(tk.END, self.maps[value])
                    self.map_detail_view.config(state=tk.DISABLED)

        app = tk.Tk()
        app.title("h3map")
        style = ThemedStyle(app)
        style.set_theme("arc")
        frame = App(master=app)
        frame.mainloop()


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

    cli_ui.info(cli_ui.bold, cli_ui.green, "\nFound {0} matching maps".format(len(filtered)))
