import glob
import gzip
import os
from pathlib import Path

from h3map.filter import HeaderFilter
from h3map.header.map_reader import MapReader
from h3map.view.view import MapsView


class MainController:
    @classmethod
    def cache(cls, path, unzipped):
        with open(path, "wb") as file:
            file.write(unzipped)

    @staticmethod
    def scan_directory(directory):
        exp = str(Path(directory) / "*.h3m")
        return glob.glob(exp[8:])

    def load_map(self, file):
        try:
            map_contents = gzip.open(file, 'rb').read()
            return MapReader.parse(map_contents)
        except Exception as e:
            print("Sorry map couldn't be loaded for " + file + " due to an error: ", e)

    def load(self, files, observer=None):
        maps = {}
        if not len(files):
            files = glob.glob("*.h3m")
        for i, map_file in enumerate(files):
            map_contents = 0
            try:
                if os.path.isfile(".cache/" + os.path.basename(map_file)):
                    with open(".cache/" + os.path.basename(map_file), 'rb') as f:
                        map_contents = f.read()
                else:
                    map_contents = gzip.open(map_file, 'rb').read()
                header = MapReader.parse(map_contents)
                maps[map_file] = header
                """
                if not os.path.isdir(".cache"):
                    os.mkdir(".cache")
                if not os.path.isfile(".cache/" + os.path.basename(map_file)):
                    self.cache(".cache/" + os.path.basename(map_file), map_contents)
                """
            except Exception as e:
                print("Sorry map couldn't be loaded for " + map_file + " due to an error: ", e)

            if observer:
                observer.ntf(header)
        return MapsView(maps.values())

    def filter(self, maps, size=None, teams=None, win=None, loss=None, team_players=None):
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
                raise ValueError("Cannot specify number of players per team without number of teams.")

            header_filter.team_has_players(int(team_players))

        return MapsView(header_filter.apply(maps))
